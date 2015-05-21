from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs

import time

class AngularJSLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.1'

    def __init__(self):
        self._selenium().add_location_strategy('Angular.Binding', self._find_by_bindings)
        self._selenium().add_location_strategy('Angular.Model', self._find_by_model)


    def wait_for_angular(self, timeout=None, error=None):

        # Determine timeout and error
        timeout = timeout or self._selenium().get_selenium_timeout()
        timeout = timestr_to_secs(timeout)
        error = error or 'Ext was not loaded before the specified timeout'

        maxtime = time.time() + timeout
        while self._exec_js("""
            var el = document.querySelector('body');
            try {
                angular
                    .element(el)
                    .injector()
                    .get('$browser')
                    .notifyWhenNoOutstandingRequests();
            } catch (e) {
                return true;
            }

            return false;
        """):
            if time.time() > maxtime:
                raise AssertionError(error)
            time.sleep(0.2)

        # Locators

        def _find_by_bindings(self, browser, criteria, tag, constrains):
            return self._exec_js("""
                var binding = '%s';
                var bindings = document.getElementsByClassName('ng-binding');
                var matches = [];

                for (var i = 0; i < bindings.length; ++i) {
                    var dataBinding = angular.element(bindings[i]).data('$binding');

                    if(dataBinding) {
                        var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;

                        if (bindingName.indexOf(binding) != -1) {
                            matches.push(bindings[i]);
                        }
                    }
                }
                return matches;
            """) % criteria

        def _find_by_model(self, browser, criteria, tag, constraints):
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:']
        for prefix in prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            elements = browser.execute_script("""return document.querySelectorAll('%s');""" % selector);
            if len(elements):
                return self._filter_elements(elements, tag, constraints)

        # Helper Methods

        def _selenium(self):
            return BuiltIn().get_library_instance('Selenium2Library')

        def _exec_js(self, code):
            return self._selenium().execute_javascript(code)
