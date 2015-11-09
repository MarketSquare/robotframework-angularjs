from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs
from selenium.webdriver.support.ui import WebDriverWait
from Selenium2Library.locators import ElementFinder

import time

js_wait_for_angular = """
var el = document.querySelector('body');
try {
    angular.element(el).injector().get('$browser').notifyWhenNoOutstandingRequests();
} catch (e) {
    return true;
}

return false;
"""


class AngularJSLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.1'

    _s2l = BuiltIn().get_library_instance('Selenium2Library')

    def __init__(self):
        self._s2l.add_location_strategy('ng-binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('ng-model', self._find_by_model, persist=True)
        self._s2l.add_location_strategy('model', self._find_by_model, persist=True)


    def wait_for_angular(self, timeout=None, error=None):

        # Determine timeout and error
        timeout = timeout or self._s2l.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)
        error = error or 'Ext was not loaded before the specified timeout'

        WebDriverWait(self._s2l._current_browser(), timeout, 0.2)\
            .until(lambda x: self._s2l._current_browser().execute_script(js_wait_for_angular))
        #maxtime = time.time() + timeout
        #while self._exec_js():
        #    if time.time() > maxtime:
        #        raise AssertionError(error)
        #    time.sleep(0.2)

    # Locators

    def _find_by_binding(self, browser, criteria, tag, constrains):
        return browser.execute_script("""
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
        """ % criteria)

    def _find_by_model(self, browser, criteria, tag, constraints):
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:']
        for prefix in prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            elements = browser.execute_script("""return document.querySelectorAll('%s');""" % selector);
            if len(elements):
                return ElementFinder()._filter_elements(elements, tag, constraints)

    # Helper Methods

    def _exec_js(self, code):
            return self._s2l._current_browser().execute_script(code)
