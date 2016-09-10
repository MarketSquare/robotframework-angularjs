import unittest
from selenium import webdriver

js_waiting_var="""
    var waiting = true;
    var callback = arguments[arguments.length - 1];
    var el = document.querySelector('#nested-ng-app');
    angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);      
    return waiting;
"""

js_return_callback="""
    var callback = arguments[arguments.length - 1];
    return callback;
"""

js_callback="""
    var callback = arguments[arguments.length - 1];
"""

js_timeout="""
    var h = setTimeout(console.log('.'),2000);
"""

js_async_with_callback="""
var callback = arguments[arguments.length - 1];
var rootSelector = '[ng-app]'
functions.waitForAngular = function(rootSelector, callback) {
  var el = document.querySelector(rootSelector);

  try {
    if (window.getAngularTestability) {
      window.getAngularTestability(el).whenStable(callback);
      return;
    }
    if (!window.angular) {
      throw new Error('window.angular is undefined.  This could be either ' +
          'because this is a non-angular page or because your test involves ' +
          'client-side navigation, which can interfere with Protractor\'s ' +
          'bootstrapping.  See http://git.io/v4gXM for details');
    }
    if (angular.getTestability) {
      angular.getTestability(el).whenStable(callback);
    } else {
      if (!angular.element(el).injector()) {
        throw new Error('root element (' + rootSelector + ') has no injector.' +
           ' this may mean it is not inside ng-app.');
      }
      angular.element(el).injector().get('$browser').
          notifyWhenNoOutstandingRequests(callback);
    }
  } catch (err) {
    callback(err.message);
  }
};
"""

js_tada="""
var done=arguments[0];
setTimeout(function() {
   done('tada');
  }, 10000);
"""

class ExecuteAsyncJavascriptWithCallback(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_script_timeout(30)

    def test_exe_javascript(self):
        driver = self.driver
        driver.get("http://localhost:7000/testapp/ng1/alt_root_index.html#/async")
#        waiting = driver.execute_script(js_tada)
#        print('%s' % waiting)

        try:
            while (True):
                #waiting = driver.execute_async_script(js_async_with_callback)
                #waiting = driver.execute_async_script(js_waiting_var)
                #waiting = driver.execute_async_script(js_callback,"print 'Hello World|'")
                #waiting = driver.execute_script(js_return_callback,"return false;")
                waiting = driver.execute_script(js_tada)
                if waiting != None:
                    print('%s' % waiting)
        except KeyboardInterrupt:
            pass

    def tearDown(self):
        # self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
