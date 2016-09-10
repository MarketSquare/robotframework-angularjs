import unittest
from selenium import webdriver

js_show_outstanding="""
    var callback = function () {console.log('*')}
    var el = document.querySelector('#nested-ng-app');
    var h = setInterval(function w4ng() {
        console.log('.');
        try {
            angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);      
        } catch (err) {
          console.log(err.message);
          callback(err.message);
        }
      }, 10);
"""

js_return_bool="""
    var callback = function () {return false;}
    var el = document.querySelector('#nested-ng-app');
    angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);      
    angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);      
    return true;
"""

js_waiting_var="""
    var waiting = true;
    var callback = function () {waiting = false;}
    var el = document.querySelector('#nested-ng-app');
    angular.element(el).injector().get('$browser').
                notifyWhenNoOutstandingRequests(callback);      
    return waiting;
"""


class ExecuteWaitForAngularTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_exe_javascript(self):
        driver = self.driver
        driver.get("http://localhost:7000/testapp/ng1/alt_root_index.html#/async")
        try:
            while (True):
                waiting = driver.execute_script(js_waiting_var)
                print('%s' % waiting)
        except KeyboardInterrupt:
            pass

    def tearDown(self):
        # self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
