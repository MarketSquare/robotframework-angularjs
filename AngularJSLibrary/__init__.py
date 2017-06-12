from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from Selenium2Library.locators import ElementFinder

import time

js_wait_for_angularjs = """
    var waiting = true;
    var callback = function () {waiting = false;}
    var el = document.querySelector('[ng-app]');
    if (typeof angular.element(el).injector() == "undefined") {
        throw new Error('root element ([ng-app]) has no injector.' +
               ' this may mean it is not inside ng-app.');
    }
    angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);
    return waiting;
"""

js_wait_for_angular = """
    var waiting = true;
    var callback = function () {waiting = false;}
    var el = document.querySelector(arguments[0]);
    if (window.angular && !(window.angular.version &&
          window.angular.version.major > 1)) {
      /* ng1 */
      angular.element(el).injector().get('$browser').
          notifyWhenNoOutstandingRequests(callback);
    } else if (window.getAngularTestability) {
      return !window.getAngularTestability(el).isStable(callback);
    } else if (window.getAllAngularTestabilities) {
      throw new Error('AngularJSLibrary does not currently handle ' +
          'window.getAllAngularTestabilities. It does work on sites supporting ' +
          'window.getAngularTestability. If you require this functionality, please ' +
          'the library authors or reach out to the Robot Framework Users Group.');
    } else if (!window.angular) {
      throw new Error('window.angular is undefined.  This could be either ' +
          'because this is a non-angular page or because your test involves ' +
          'client-side navigation. Currently the AngularJS Library is not ' +
          'designed to wait in such situations. Instead you should explicitly ' +
          'call the "Wait For Angular" keyword.');
    } else if (window.angular.version >= 2) {
      throw new Error('You appear to be using angular, but window.' +
          'getAngularTestability was never set.  This may be due to bad ' +
          'obfuscation.');
    } else {
      throw new Error('Cannot get testability API for unknown angular ' +
          'version "' + window.angular.version + '"');
    }
    return waiting;
"""


js_get_pending_http_requests="""
var el = document.querySelector('[ng-app]');
var $injector = angular.element(el).injector();
var $http = $injector.get('$http');
return $http.pendingRequests;
"""

js_repeater_min = """
var rootSelector=null;function byRepeaterInner(b){var a="by."+(b?"exactR":"r")+"epeater";return function(c){return{getElements:function(d){return findAllRepeaterRows(c,b,d)},row:function(d){return{getElements:function(e){return findRepeaterRows(c,b,d,e)},column:function(e){return{getElements:function(f){return findRepeaterElement(c,b,d,e,f,rootSelector)}}}}},column:function(d){return{getElements:function(e){return findRepeaterColumn(c,b,d,e,rootSelector)},row:function(e){return{getElements:function(f){return findRepeaterElement(c,b,e,d,f,rootSelector)}}}}}}}}repeater=byRepeaterInner(false);exactRepeater=byRepeaterInner(true);function repeaterMatch(a,b,c){if(c){return a.split(" track by ")[0].split(" as ")[0].split("|")[0].split("=")[0].trim()==b}else{return a.indexOf(b)!=-1}}function findRepeaterRows(k,e,g,l){l=l||document;var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]];var o=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){o.push(n[c])}}}var f=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat-start";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){var b=n[c];var m=[];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,k)){if(b.nodeType==1){m.push(b)}b=b.nextSibling}f.push(m)}}}var m=o[g]||[],j=f[g]||[];return[].concat(m,j)}function findAllRepeaterRows(g,e,h){h=h||document;var k=[];var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var a=0;a<d.length;++a){var f=d[a]+"repeat";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){k.push(j[c])}}}for(var a=0;a<d.length;++a){var f=d[a]+"repeat-start";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){var b=j[c];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,g)){if(b.nodeType==1){k.push(b)}b=b.nextSibling}}}}return k}function findRepeaterElement(a,b,g,r,q,w){var c=[];var t=document.querySelector(w||"body");q=q||document;var l=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var n=0;n<x.length;++n){var s=x[n]+"repeat";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){l.push(o[v])}}}var m=[];for(var n=0;n<x.length;++n){var s=x[n]+"repeat-start";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){var y=o[v];var f=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){f.push(y)}y=y.nextSibling}m.push(f)}}}var f=l[g];var z=m[g];var A=[];if(f){if(f.className.indexOf("ng-binding")!=-1){A.push(f)}var k=f.getElementsByClassName("ng-binding");for(var v=0;v<k.length;++v){A.push(k[v])}}if(z){for(var v=0;v<z.length;++v){var e=z[v];if(e.className.indexOf("ng-binding")!=-1){A.push(e)}var k=e.getElementsByClassName("ng-binding");for(var u=0;u<k.length;++u){A.push(k[u])}}}for(var v=0;v<A.length;++v){var h=angular.element(A[v]).data("$binding");if(h){var d=h.exp||h[0].exp||h;if(d.indexOf(r)!=-1){c.push(A[v])}}}return c}function findRepeaterColumn(a,b,q,o,w){var c=[];var s=document.querySelector(w||"body");o=o||document;var h=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var m=0;m<x.length;++m){var r=x[m]+"repeat";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){h.push(n[v])}}}var l=[];for(var m=0;m<x.length;++m){var r=x[m]+"repeat-start";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){var y=n[v];var e=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){e.push(y)}y=y.nextSibling}l.push(e)}}}var z=[];for(var v=0;v<h.length;++v){if(h[v].className.indexOf("ng-binding")!=-1){z.push(h[v])}var g=h[v].getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}for(var v=0;v<l.length;++v){for(var u=0;u<l[v].length;++u){var y=l[v][u];if(y.className.indexOf("ng-binding")!=-1){z.push(y)}var g=y.getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}}for(var u=0;u<z.length;++u){var f=angular.element(z[u]).data("$binding");if(f){var d=f.exp||f[0].exp||f;if(d.indexOf(q)!=-1){c.push(z[u])}}}return c};"""

arg0="/\\/g,\"\""
arg1="ng\\:"

def stripcurly(binding):
    """ Starting with AngularJS 1.3 the interpolation brackets are not allowed
    in the binding description string. As such the AngularJSLibrary strips them
    out before calling the _find_by_binding method.

    See http://www.protractortest.org/#/api?view=ProtractorBy.prototype.binding
    """
    if binding.startswith('{{'):
        binding = binding[2:]

    if binding.endswith('}}'):
        binding = binding[:-2]

    return binding

def is_boolean(item):
    return isinstance(item,bool)

class ngElementFinder(ElementFinder):
    def __init__(self, root_selector, ignore_implicit_angular_wait=False):
        super(ngElementFinder, self).__init__()
        self.root_selector = root_selector
        self.ignore_implicit_angular_wait = ignore_implicit_angular_wait

    def find(self, browser, locator, tag=None):
        timeout = self._s2l.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)

        if not self.ignore_implicit_angular_wait:
            try:
                WebDriverWait(self._s2l._current_browser(), timeout, 0.2)\
                    .until_not(lambda x: self._s2l._current_browser().execute_script(js_wait_for_angular, self.root_selector))
            except TimeoutException:
                pass
        strategy = ElementFinder.find(self, browser, locator, tag=None)
        return strategy

    def _find_by_default(self, browser, criteria, tag, constraints):
        if criteria.startswith('//'):
            return self._s2l._element_finder._find_by_xpath(browser, criteria, tag, constraints)
        elif criteria.startswith('{{'):
            criteria = stripcurly(criteria)
            return self._find_by_binding(browser, criteria, tag, constraints)
        return self._find_by_key_attrs(browser, criteria, tag, constraints)

    def _find_by_binding(self, browser, criteria, tag, constraints):
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

    @property
    def _s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

class AngularJSLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.6'

    def __init__(self,
                 root_selector=None,
                 implicit_angular_wait=30.0,
                 ignore_implicit_angular_wait=False
    ):
        """AngularJSLibrary can be imported with optional arguments.

        `root_selector` is the locator of the root angular object. If none is given it defaults to `[ng-app]`.
        For more information please refer to the following documentation:
           $rootElement - AngularJS API documentation - https://docs.angularjs.org/api/ng/service/$rootElement
           ngApp - AngularJS API documentation - https://docs.angularjs.org/api/ng/directive/ngApp

        Not Yet Implemented - `implicit_angular_wait` is the implicit timeout that AngularJS library
                             waits for angular to finish rendering and waits for any outstanding $http calls.

        `ignore_implicit_angular_wait` is a flag which when set to True the AngularJS Library will not wait
        for Angular $timeouts nor $http calls to complete when finding elements by locator. As noted in the
        Protractor documentation "this should be used only when necessary, such as when a page continuously
        polls an API using $timeout." The default value is False.

        Examples:
        | Library `|` AngularJSLibrary `|` ignore_implicit_angular_wait=${true}   | # Will not wait for angular syncronization

        """

        self.ignore_implicit_angular_wait = ignore_implicit_angular_wait

        if not root_selector:
            self.root_selector = '[ng-app]'
        else:
            self.root_selector = root_selector
            
        # Override default locators to include binding {{ }}
        self._s2l._element_finder = ngElementFinder(self.root_selector, ignore_implicit_angular_wait)

        # Add Angular specific locator strategies
        self._s2l.add_location_strategy('ng-binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('ng-model', self._find_by_model, persist=True)
        self._s2l.add_location_strategy('model', self._find_by_model, persist=True)
        self._s2l.add_location_strategy('ng-repeater', self._find_by_ng_repeater, persist=True)
        self._s2l.add_location_strategy('repeater', self._find_by_ng_repeater, persist=True)

        self.trackOutstandingTimeouts = True

    # Wait For Angular

    def wait_for_angular(self, timeout=None, error=None):

        # Determine timeout and error
        timeout = timeout or self._s2l.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)
        error = error or ('Timed out waiting for Protractor to synchronize with ' +
                         'the page after specified timeout.')

        try:
            WebDriverWait(self._s2l._current_browser(), timeout, 0.2)\
                .until_not(lambda x: self._s2l._current_browser().execute_script(js_wait_for_angular, self.root_selector))
        except TimeoutException:
            pass
            #if self.trackOutstandingTimeouts:
            #    timeouts = self._exec_js('return window.NG_PENDING_TIMEOUTS')
            #    logger.debug(timeouts)
            #pendingHttps = self._exec_js(js_get_pending_http_requests)
            #logger.debug(pendingHttps)
            #raise TimeoutException(error)

    def set_ignore_implicit_angular_wait(self, ignore):
        if not is_boolean(ignore):
            raise TypeError("Ignore must be boolean, got %s."
                            % type_name(ignore))

        self._s2l._element_finder.ignore_implicit_angular_wait = ignore

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
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-']#, 'ng\\:']
        for prefix in prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            elements = browser.execute_script("""return document.querySelectorAll('%s');""" % selector);
            if len(elements):
                return ElementFinder()._filter_elements(elements, tag, constraints)
        raise ValueError("Element locator '" + criteria + "' did not match any elements.")

    def _find_by_ng_repeater(self, browser, criteria, tag, constraints):
        repeater_row_col = self._parse_ng_repeat_locator(criteria)

        js_repeater_str = self._reconstruct_js_locator(repeater_row_col)
        elements = browser.execute_script(
            js_repeater_min +
            """var ng_repeat = new byRepeaterInner(true);""" +
            """return ng_repeat%s.getElements();""" % (js_repeater_str),
            arg0, arg1
        );
        if len(elements):
            return ElementFinder()._filter_elements(elements, tag, constraints)
        else:
            raise ValueError("Element locator '" + criteria + "' did not match any elements.")


    # Helper Methods

    def _exec_js(self, code):
            return self._s2l._current_browser().execute_script(code)

    def _parse_ng_repeat_locator(self, criteria):
        def _startswith(str,sep):
            parts = str.lower().partition(sep)
            if parts[1]==sep and parts[0]=='':
                return parts[2]
            else:
                return None


        def _parse_arrayRE(str):
            import re
            match = re.search(r"(?<=^\[).+([0-9]*).+(?=\]$)",str)
            if match:
                return match.group()
            else:
                return None

        def _parse_array(str):
            if str[0]=='[' and str[-1]==']':
                return int(str[1:-1])
            else:
                return None

        rrc = criteria.rsplit('@')
        extractElem = {'repeater': None, 'row_index': None, 'col_binding': None}
        if len(rrc)==1:
            #is only repeater
            extractElem['repeater']=rrc[0]
            return extractElem
        else:
            # for index in reversed(rrc):
            while 1 < len(rrc):
                index = rrc.pop()
                row = _startswith(index,'row')
                column = _startswith(index,'column')
                if row:
                    array = _parse_array(row)
                    rlocator = _startswith(row,'=')
                    if array is not None:
                        extractElem['row_index'] = array
                    elif rlocator:
                        # row should be an list index and not binding locator
                        raise ValueError("AngularJS ng-repeat locator with row as binding is not supported")
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                elif column:
                    array = _parse_array(column)
                    clocator = _startswith(column,'=')
                    if array is not None:
                        # col should be an binding locator and not list index
                        raise ValueError("AngularJS ng-repeat locator with column as index is not supported")
                    elif clocator:
                        extractElem['col_binding'] = clocator
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                else:
                    # stray @ not releated to row/column seperator
                    rrc[-1] = rrc[-1] + '@' + index
        extractElem['repeater']=rrc[0]
        return extractElem

    def _reconstruct_js_locator(self, loc_dict):
        js_locator = "(\"%s\")" % loc_dict['repeater']

        if loc_dict['row_index']:
            js_locator = js_locator + ".row(%s)" % loc_dict['row_index']

        if loc_dict['col_binding']:
            #js_locator = js_locator + """.column('""" + loc_dict['col_binding'] + """')"""
            js_locator = js_locator + ".column(\"%s\")"  % loc_dict['col_binding']

        #js_locator = js_locator + """.getElements()"""

        return js_locator

    @property
    def _s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')
