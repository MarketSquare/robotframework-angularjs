Testing AngularJS Library
=========================

These are instructions for pulling in all the parts and testing the AngularJS Library for Robot Framework

Setup Environment
-----------------

We will have both a base set of pythons packages as well as the source for the AngularJSLibrary and the Selenium2Library all of which will will want to keep isolated from your system python and its packages. As such we will use Python's virtual environment. Let's start by creating a a root folder for testing.

.. code::  bash

	   mkdir test-ng
	   cd test-ng

Within this root folder we will create the virtualenv and clone source repositories

.. code::  bash

	   virtualenv -p /usr/bin/python2.7 --no-site-packages clean-python27-env
	   source clean-python27-env/bin/activate
	   pip install decorator docutils robotframework selenium
	   
	   git clone git@github.com:Selenium2Library/robotframework-angularjs.git rf-ng
	   git clone git@github.com:robotframework/Selenium2Library.git rf-s2l
	   
We will also clone the protractor repository. From Protractor we will use their test site, testapp, but not their test server. For the test server we will use the Selenium2Library test server with some modifications.

.. code::  bash

	   git clone git@github.com:angular/protractor.git ptor
           cp -R ptor/testapp rf-s2l/test/resources/.

I modified the async testapp page so that the implicit wait for angular functionality can be tested. The modified version of async.html and async.js can be moved over to the testapp directory under rf-s2l directory.

.. code:: bash

    cp rf-ng/AngularJSLibrary/async.html rf-s2l/test/resources/testapp/ng1/async/.
    cp rf-ng/AngularJSLibrary/async.js rf-s2l/test/resources/testapp/ng1/async/.

Modifying the test server of Selenium2Library, rf-s2l\\test\\resources\\testserver\\testserver.py, add the following method, do_GET, to the StoppableHttpRequestHandler class.

.. code:: python

    def do_GET(self):
        """Response pages for Angular tests.

        Added by Edward Manlove - June 5, 2014
        """
        if self.path.endswith('/fastcall'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('done')
        elif self.path.endswith('/slowcall'):
            sleep(2)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('finally done')
        elif self.path.endswith('/fastTemplateUrl'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('fast template contents')
        elif self.path.endswith('/slowTemplateUrl'):
            sleep(2)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('slow template contents')
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Don't forget with the added sleep statements you need to include the time package

.. code:: python

    from time import sleep

otherwise several tests will fail.

Finally, let's move the test files over to the Selenium2Library test directory. Although this may not be necessary I do it to keep all the test files together. Ultimately I would like to see the Selenium2Library test directory moved into the src directory so the tests get distributed and then allow the test scripts for AngularJSLibrary be abe to be run from its own test directory. But for now we will combine them.

.. code:: bash

    cp rf-ng/AngularJSLibrary/angular.robot rf-s2l/test/acceptance/locators/.
    cp rf-ng/AngularJSLibrary/angular_wait.robot rf-s2l/test/acceptance/keywords/.
	   
Directory Structure
-------------------

So taking a step back and looking at the whole structure we should see the following directories

rf-s2l/
    The source code for Robot Framework Selenium2Library.
    
rf-ng/
    The source code for Robot Framework AngularJSLibrary.

ptor/
    The source code for Robot Framework Seleniu2Library.

Within those directories we should see some modifications

rf-s2l/test/resources/testserver/testserver.py
    A modified version of the test server containing the additional do_GET() method.

rf-s2l/test/acceptance/locators/angular.robot
    AngularJSLibrary acceptance tests testing locators.

rf-s2l/test/acceptance/keywords/angular_wait.robot
    AngularJSLibrary acceptance tests testing wait for angular functionality.

rf-s2l/test/resources/testapp/ng/async/async.html
rf-s2l/test/resources/testapp/ng/async/async.js
    A modified version of the async testapp page containing buttons which appear after the
    angular $timeouts and $http requests are completed.

And if we activate our virtual Python instance we should see

.. code:: bash
	  
    # pip list
    decorator (4.0.10)
    docutils (0.12)
    pip (8.1.2)
    robotframework (3.0)
    selenium (2.53.6)
    setuptools (8.2.1)

Note your versions may be different then mine listed here but key is you have installed robotframework and selenium packages and have **not** installed selenium2library as we will use the source code instead.

Starting the modified testserver
--------------------------------

Open a new bash terminal from which we will run the test sever

.. code:: bash

    cd test-ng

    source clean-python27-env/bin/activate
    
    cd rf-s2l
    
    python test/resources/testserver/testserver.py start

You can test the server by navigating in a browser to

.. code::
   
   http://localhost:7000/testapp

Running the test scripts
------------------------

In another terminal we will run the test scripts

.. code:: bash

    cd ng

    source clean-python27-env/bin/activate
    
    cd rf-s2l
    
    python test/run_tests.py python FF --suite acceptance.locators.angular --pythonpath ../rf-ng

    python test/run_tests.py python FF --suite acceptance.keywords.angular_wait --pythonpath ../rf-ng

Note there is currently an issue with the Selenium2Library test runner script where if you specify a specific suite the output log and report files will not be created automatically. To get those files you can type

.. code:: bash

    rebot -d test/results/ test/results/output.xml

Understanding how AngularJSLibrary works
----------------------------------------

It is important for you, the end user, to understand what is going on in the underlying library and there are many reasons for that. For one as I continue to develop this library I realize some initial assumptions and thus original implementations were simply wrong. I also have very narrow focus as my daily work focuses on a single (and usually older) version of AngularJS. So there could be issues I am not seeing and thus not addressing. These and many more reasons support the argument that as a library user we should all be well informed as to how the library works and what is Protractor / AngularJS doing in the functions we are mimicing.

Let's start off by examining the waitForAngular functionality in Protractor. At the core is this function (with some code removed) in ptor/lib/clientsidescripts.js

.. code :: javascript

    /**
     * Wait until Angular has finished rendering and has
     * no outstanding $http calls before continuing. The specific Angular app
     * is determined by the rootSelector.
     *
     * Asynchronous.
     *
     * @param {string} rootSelector The selector housing an ng-app
     * @param {function(string)} callback callback. If a failure occurs, it will
     *     be passed as a parameter.
     */
    functions.waitForAngular = function(rootSelector, callback) {
      var el = document.querySelector(rootSelector);
    
      try {
        /* [SNIP] Newer vesions (which ones? not sure) there is a function for waiting. This
	one is off the window object. For now we will ignore this method and look at the original
	method for waiting...
	*/
	/* [SNIP] Check to make sure we're on an angular page. */
        if (angular.getTestability) {
          /* [SNIP] Another function for waiting that comes from angular's testability api. */
        } else {
	  /* Another check to verify we are within the ng-app. */

          angular.element(el).injector().get('$browser').
              notifyWhenNoOutstandingRequests(callback);
	      
        }
      } catch (err) {
        callback(err.message);
      }
    };

So striping out a lot of the code (see [SNIP]s above), the core is simply this

.. code :: javascript

    angular.element(el).injector().get('$browser').
        notifyWhenNoOutstandingRequests(callback);

a method which sounds like will give notification when there are no more outstanding requests or angular "actions". But what does callback do? What exactly does this method look like and how does one thus use it information? To answer what this looks like in practice we can use the testapp above. Start up the test server

.. code::  bash

    cd ng

    source clean-python27-env/bin/activate
    
    cd rf-s2l
    
    python test/resources/testserver/testserver.py start

In a browser navigate to

.. code::
   
   http://localhost:7000/testapp/ng1/alt_root_index.html#/async

[You'll see here I am using the angular1 portion of testapp. Also I am using the alt_root_index so I can hardcode which version of Angular1.x I'll want.] With the site running open the developers tools (F12) and in the console editor paste the following code, but before you run it let's tear it apart.

.. code ::  javascript

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

You should see it is basically a call to setInterval which will continually call the function with a 10 ms delay each time till the interval is cleared. The function it is calling basically outputs a dot, '.', and calls the notifyWhenNoOutstandingRequests function from the waitForAngular passing along the callback. That callback will print out a star, '*', to the console. Want to take a guess as to what will happen when you run this code?

You will see a continual series of dots then stars printed to the console. Now on the async test page click the button label $timeout. Only dots are printed to the console for some time. Then only stars. What is happening at this time? When only the dots are outputed we are waiting for angular. More so, the callback that would print stars has not returned. And when just the stars are print, its all those callbacks returning while we were waiting for angular to complete. Go ahead and click on some of the other asyncrouous actions on the async page and see what the output is.

Note when you want to stop the output type the following line into the console to stop the continious interval call.

.. code ::  javascript

    clearInterval(h);

So we can visualize the waiting for angular within javascript and from within the browser. We want, though, to not be in javascript (otherise we would just use Protrator and WebDriverJS) but in python.  So let's do something similar with a simple python unittest.

.. code ::  python

    import unittest
    from selenium import webdriver
    
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
            self.driver.close()
    
    if __name__ == "__main__":
        unittest.main()

I went through a couple interations before settling on the above. Let me go through the syncronous javascript script. First, I like the simplicity of it. One iteration had a couple of calls to notifyWhenNoOutstandingRequests() with the (incorrect) thinking that I needed to ask twice to force the javascript execution stack to push through, if you will, the callback function. Remember, having the callback function return (with false) is the indication we are not waiting. But it turns out this not necessary as the function notifyWhenNoOutstandingRequests immediately calls the callback function if the outstanding request count is zero and thus sets the waiting flag to false. Summarizing, the javascript code sets the waiting flag to true stating we are waiting, calls notifyWhenNoOutstandingRequests and if not waiting sets the flag to false then returns the flag. So with a syncronous call we get back an immediate answers of the state of angular.

The use of a syncronous call by the AngularJSLibrary differs from other non-WebDriverJS ports of protractor. Almost all other ports use asyncronous javascript call. For this I don't understand [1]_. I understand why I choose a syncronious call but I don't see why asynchronous. So just as above I broke it down I tried to make an asycronous call to do the same. No luck. Then I did the second option, Google. [Note, this is the correct order. I tried something first and then tried Google. This is the best approach because it helps you to really think about the problem and not be trapped by the first answer that comes up.] So I tired Google and ... no luck. Some good resources but nothing worked as expected. Then I had the ah ha moment (which was really a duh moment) - Selenium test code!

The javascript tests can be found under py/test/selenium/webdriver/common/executing_async_javascript_tests.py. These async tests make more sense (to me at least) but don't give much depth to asyncronous javascript calls.

...[I think I need to finish this thought]...

Implicit Wait for Angular
-------------------------
As advertised on Protractor's homepage, Protractor "can automatically execute the next step in your test the moment the webpage finishes pending tasks, so you don’t have to worry about waiting for your test and webpage to sync." This implicit wait for angular functionality is implemented at couple points. First, as found in the ElementArrayFinder, "the first time [Protractor is] looking for an element". Second, as noted in protractor/lib/plugins.ts, "[b]etween every webdriver action, Protractor calls browser.waitForAngular() to make sure that Angular has no outstanding $http or $timeout calls."  So whenever Protractor looks for an element [2]_ or whenever it makes a Selenium WebDriverJS library call it waits for angular thus fufilling the claim that you no longer need explicit waits. For the AngularJSLibrary then we will also want to wait when looking for an element or when calling a selenium method.

Interestingly enough, for the Selenium2Library when one makes a selenium call one is also looking for an element. This leads to a really slick (IMHO) solution for the Angular2Library. `Here it is<https://github.com/Selenium2Library/robotframework-angularjs/blob/master/AngularJSLibrary/__init__.py#L69>`_...

.. code ::  python

    class ngElementFinder(ElementFinder):
        def __init__(self, ignore_implicit_angular_wait=False):
            super(ngElementFinder, self).__init__()
            self.ignore_implicit_angular_wait = ignore_implicit_angular_wait
    
        def find(self, browser, locator, tag=None):
            timeout = self._s2l.get_selenium_timeout()
            timeout = timestr_to_secs(timeout)
    
            if not self.ignore_implicit_angular_wait:
                try:
                    WebDriverWait(self._s2l._current_browser(), timeout, 0.2)\
                        .until_not(lambda x: self._s2l._current_browser().execute_script(js_waiting_var))
                except TimeoutException:
                    pass
            strategy = ElementFinder.find(self, browser, locator, tag=None)
            return strategy

Essentially we override the find method of Selenium2Library. So whenever you pass a locator to one of the Selenium2Library keywords you are calling, implicitly, wait for angular. One can see this in the Robot Framework log file when you have set loglevel to ``DEBUG``. Here is the log file output when we click an element

.. code ::

    KEYWORD Selenium2Library . Click Element model=show
    Documentation: 	
    
    Click element identified by `locator`.
    Start / End / Elapsed: 	20161112 11:45:37.794 / 20161112 11:45:37.917 / 00:00:00.123
    11:45:37.794 	INFO 	Clicking element 'model=show'. 	
    11:45:37.795 	DEBUG 	POST http://127.0.0.1:54972/hub/session/2d75d46c-de31-4a23-85d5-665234b73eb9/execute {"sessionId": "2d75d46c-de31-4a23-85d5-665234b73eb9", "args": [], "script": "\n var waiting = true;\n var callback = function () {waiting = false;}\n var el = document.querySelector('[ng-app]');\n if (typeof angular.element(el).injector() == \"undefined\") {\n throw new Error('root element ([ng-app]) has no injector.' +\n ' this may mean it is not inside ng-app.');\n }\n angular.element(el).injector().get('$browser').\n notifyWhenNoOutstandingRequests(callback);\n return waiting;\n"} 	
    11:45:37.804 	DEBUG 	Finished Request 	
    11:45:37.805 	DEBUG 	POST http://127.0.0.1:54972/hub/session/2d75d46c-de31-4a23-85d5-665234b73eb9/execute {"sessionId": "2d75d46c-de31-4a23-85d5-665234b73eb9", "args": [], "script": "return document.querySelectorAll('[ng-model=\"show\"]');"} 	
    11:45:37.813 	DEBUG 	Finished Request 	
    11:45:37.814 	DEBUG 	POST http://127.0.0.1:54972/hub/session/2d75d46c-de31-4a23-85d5-665234b73eb9/element/{087ef768-948b-4a41-ad41-422b49d3a143}/click {"sessionId": "2d75d46c-de31-4a23-85d5-665234b73eb9", "id": "{087ef768-948b-4a41-ad41-422b49d3a143}"} 	
    11:45:37.916 	DEBUG 	Finished Request

The first POST is an execute javascript call where the javascript function is the internal wait for angular script. In this case Angular was not waiting and thus the next POST was a call to the find element; in this case a ng-model and another javascript call. One would see a similar call to the implicit wait for angular even if the locator strategy was an id, css, xpath or any other standard locator strategy. As compared to the above example here is the (truncated) output when there is a stack of unfufilled promises

.. code ::

    KEYWORD Selenium2Library . Click Button css=[ng-click="slowAngularTimeoutHideButton()"]
    Documentation: 	
    
    Clicks a button identified by `locator`.
    Start / End / Elapsed: 	20161112 11:53:41.863 / 20161112 11:53:47.127 / 00:00:05.264
    11:53:41.864 	INFO 	Clicking button 'css=[ng-click="slowAngularTimeoutHideButton()"]'. 	
    11:53:41.865 	DEBUG 	POST http://127.0.0.1:59197/hub/session/2b715259-07c2-41d4-90a8-0fa97e271447/execute {"sessionId": "2b715259-07c2-41d4-90a8-0fa97e271447", "args": [], "script": "\n var waiting = true;\n var callback = function () {waiting = false;}\n var el = document.querySelector('[ng-app]');\n if (typeof angular.element(el).injector() == \"undefined\") {\n throw new Error('root element ([ng-app]) has no injector.' +\n ' this may mean it is not inside ng-app.');\n }\n angular.element(el).injector().get('$browser').\n notifyWhenNoOutstandingRequests(callback);\n return waiting;\n"} 	
    11:53:41.879 	DEBUG 	Finished Request 	
    11:53:42.080 	DEBUG 	POST http://127.0.0.1:59197/hub/session/2b715259-07c2-41d4-90a8-0fa97e271447/execute {"sessionId": "2b715259-07c2-41d4-90a8-0fa97e271447", "args": [], "script": "\n var waiting = true;\n var callback = function () {waiting = false;}\n var el = document.querySelector('[ng-app]');\n if (typeof angular.element(el).injector() == \"undefined\") {\n throw new Error('root element ([ng-app]) has no injector.' +\n ' this may mean it is not inside ng-app.');\n }\n angular.element(el).injector().get('$browser').\n notifyWhenNoOutstandingRequests(callback);\n return waiting;\n"} 	
    11:53:42.096 	DEBUG 	Finished Request
    
    ...                 ...     ...
    
    11:53:47.037 	DEBUG 	POST http://127.0.0.1:59197/hub/session/2b715259-07c2-41d4-90a8-0fa97e271447/execute {"sessionId": "2b715259-07c2-41d4-90a8-0fa97e271447", "args": [], "script": "\n var waiting = true;\n var callback = function () {waiting = false;}\n var el = document.querySelector('[ng-app]');\n if (typeof angular.element(el).injector() == \"undefined\") {\n throw new Error('root element ([ng-app]) has no injector.' +\n ' this may mean it is not inside ng-app.');\n }\n angular.element(el).injector().get('$browser').\n notifyWhenNoOutstandingRequests(callback);\n return waiting;\n"} 	
    11:53:47.052 	DEBUG 	Finished Request 	
    11:53:47.053 	DEBUG 	POST http://127.0.0.1:59197/hub/session/2b715259-07c2-41d4-90a8-0fa97e271447/elements {"using": "css selector", "sessionId": "2b715259-07c2-41d4-90a8-0fa97e271447", "value": "[ng-click=\"slowAngularTimeoutHideButton()\"]"} 	
    11:53:47.058 	DEBUG 	Finished Request 	
    11:53:47.059 	DEBUG 	POST http://127.0.0.1:59197/hub/session/2b715259-07c2-41d4-90a8-0fa97e271447/element/{e9c1e40c-74c7-44a8-801e-45151329fadc}/click {"sessionId": "2b715259-07c2-41d4-90a8-0fa97e271447", "id": "{e9c1e40c-74c7-44a8-801e-45151329fadc}"} 	
    11:53:47.127 	DEBUG 	Finished Request

Note the time before and after the (...); about five seconds has passed. Here I truncated, so this printout is not so long, all the javascript calls asking angular if it has any outstanding promises. Eventually the promise have been fufilled and the script looks for an element and clicks it.

This DEBUG output comes from the internal AngularJSLibrary acceptance tests

.. code :: RobotFramework

    Implicit Wait For Angular On Timeout
        Wait For Angular
    
        Click Button  css=[ng-click="slowAngularTimeout()"]
    
        Click Button  css=[ng-click="slowAngularTimeoutHideButton()"]
    
    Implicit Wait For Angular On Timeout With Promise
        Wait For Angular
    
        Click Button  css=[ng-click="slowAngularTimeoutPromise()"]
    
        Click Button  css=[ng-click="slowAngularTimeoutPromiseHideButton()"]

To the Protractor testapp, I added some buttons

.. code :: html

    <li>
      <button ng-click="slowAngularTimeout()">$timeout</button>
      <span ng-bind="slowAngularTimeoutStatus"></span>
      <button ng-show="slowAngularTimeoutCompleted" ng-click="slowAngularTimeoutHideButton()">Hide</button>
    </li>
    <li>
      <button ng-click="slowAngularTimeoutPromise()">$timeout promise</button>
      <span ng-bind="slowAngularTimeoutPromiseStatus"></span>
      <button ng-show="slowAngularTimeoutPromiseCompleted" ng-click="slowAngularTimeoutPromiseHideButton()">Hide</button>
    </li>
    <li>
      <button ng-click="slowHttpPromise()">http promise</button>
      <span ng-bind="slowHttpPromiseStatus"></span>
      <button ng-show="slowHttpPromiseCompleted" ng-click="slowHttpPromiseHideButton()">Hide</button>
    </li>

that will become visible when the "timeouts" are completed. As shown in the test above, the script clicks both buttons in succession without any explicit delay in the script. This provides us a good test suite to validate the implicit wait for angular. I also added a function to re-hide the button so the tests can be reset. One more test allows us the ability to validate this click the two buttons without delay will fail if we ignore the implicit wait for angular

.. code :: robotframework

    Toggle Implicit Wait For Angular Flag
        Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]
    
        Set Ignore Implicit Angular Wait  ${true}
    
        Click Button  css=[ng-click="slowAngularTimeout()"]
    
        Run Keyword And Expect Error  *  Click Button  css=[ng-click="slowAngularTimeoutHideButton()"]
    
        Wait For Angular
        Element Should Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]
        Click Element  css=[ng-click="slowAngularTimeoutHideButton()"]
        Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]
    
        Set Ignore Implicit Angular Wait  ${false}
    
        Click Button  css=[ng-click="slowAngularTimeout()"]
    
        Click Button  css=[ng-click="slowAngularTimeoutHideButton()"]
    
        Element Should Not Be Visible  css=[ng-click="slowAngularTimeoutHideButton()"]

Angular 2
---------
Looking at filling in the gap of Angular 2 support. Taking a look at the the current state of Protractor the `waitForAngular function<https://github.com/angular/protractor/blob/33393cad633e6cb5ce64b3fc8fa5e8a9cae64edd/lib/clientsidescripts.js#L135>`_ has some code to handle both Angular 1 and Angular 2+ code. Taking this Protractor code and combining it with test javascript code above (where we tested tthe core check printing out only '.' while Angular is busy) we have some asemblance of the Angular 1 and Angular 2+ support.

.. code ::  javascript

    var callback = function () {console.log('*')};
    var el = document.querySelector('[ng-app]');
    var h = setInterval(function w4ng() {
        console.log('.');
        try {
            if (window.angular && !(window.angular.version &&
                  window.angular.version.major > 1)) {
              /* ng1 */
              angular.element(el).injector().get('$browser').
                  notifyWhenNoOutstandingRequests(callback);      
            } else if (window.angular.getTestability) {
              window.angular.getTestability(el).whenStable(callback);
            }
        } catch (err) {
          console.log(err.message);
          callback(err.message);
        }
      }, 10);

Some important notes on running this script. Since I wrote the above portions of this write-up Firebug has ceased development and it has been combined with Firefox's developer tools. Under Firefox 53 (my current version) console.log when used within the console prompt no longer outputs to the console. [Yes it returns 'undefined' which is well explained out there and is perfectly valid but not very user friendly]. Chrome on the other hand does. So for now you will need to run the above code in the console within Chrome's dev tools. The other issue is a matter of the getTestibility function and its parent object. It appears that with the Angular development this method has been moved in the object tree and renamed. Under Protractor this function is now window.getAngularTestability. While investigating I was using several test sites. The testapp within Protractor does has a Angular 2 version although greatly simplified over the Angular 1 version. Due to some complications of Chrome, running on a VM, limited RAM, building the ng2 testapp with node, etc. I simplified my investigation by using other test sites. I tried angular.io's `tutorial example<https://angular.io/resources/live-examples/toh-6/ts/eplnkr.html >`_ but was slightly problimatic. It also is Angular ver 1.6.3 ?!? which isn't very helpful. I settled upon simply the angular.io site - although ... I am realizing many of these Angular site are still Angular 1.

Ok, this may explain the difference between window.angular.getTestability and window.getAngularTestability. The prior was introduced and available a while back and back in the Angular 1. I was simply lazy in that for my work the notifyWhenNoOutstandingRequests was sufficient. It could be that window.getAngularTestability is purely Angular 2+. ... [Researching] ... Ok form a very brief look, ok one site, it looks like this is the case. Let me put forth what I am thinking

.. code ::  javascript

    var callback = function () {console.log('*')};
    var el = document.querySelector('[ng-app]');
    var h = setInterval(function w4ng() {
        console.log('.');
        try {
            if (window.angular && !(window.angular.version &&
                  window.angular.version.major > 1)) {
              /* ng1 */
              angular.element(el).injector().get('$browser').
                  notifyWhenNoOutstandingRequests(callback);      
            } else if (window.getAngularTestability) {
              window.getAngularTestability(el).whenStable(callback);
            } else if (window.getAllAngularTestabilities) {
              var testabilities = window.getAllAngularTestabilities();
              var count = testabilities.length;
              var decrement = function() {
                count--;
                if (count === 0) {
                  callback();
                }
              };
              testabilities.forEach(function(testability) {
                testability.whenStable(decrement);
              });
            } else if (!window.angular) {
              throw new Error('window.angular is undefined.  This could be either ' +
                  'because this is a non-angular page or because your test involves ' +
                  'client-side navigation. Currently the AngularJS Library is not ' +
                  'designed to wait in such situations. Instead you should explicitly ' +
                  'call the \'Wait For Angular\' keyword.');
            } else if (window.angular.version >= 2) {
              throw new Error('You appear to be using angular, but window.' +
                  'getAngularTestability was never set.  This may be due to bad ' +
                  'obfuscation.');
            } else {
              throw new Error('Cannot get testability API for unknown angular ' +
                  'version "' + window.angular.version + '"');
            }
        } catch (err) {
          console.log(err.message);
          callback(err.message);
        }
      }, 10);

which one could compared with the full Protractor code

.. code ::  javascript

    if (window.angular && !(window.angular.version &&
          window.angular.version.major > 1)) {
      /* ng1 */
      var hooks = getNg1Hooks(rootSelector);
      if (hooks.$$testability) {
        hooks.$$testability.whenStable(callback);
      } else if (hooks.$injector) {
        hooks.$injector.get('$browser').
            notifyWhenNoOutstandingRequests(callback);
      } else if (!!rootSelector) {
        throw new Error('Could not automatically find injector on page: "' +
            window.location.toString() + '".  Consider using config.rootEl');
      } else {
        throw new Error('root element (' + rootSelector + ') has no injector.' +
           ' this may mean it is not inside ng-app.');
      }
    } else if (rootSelector && window.getAngularTestability) {
      var el = document.querySelector(rootSelector);
      window.getAngularTestability(el).whenStable(callback);
    } else if (window.getAllAngularTestabilities) {
      var testabilities = window.getAllAngularTestabilities();
      var count = testabilities.length;
      var decrement = function() {
        count--;
        if (count === 0) {
          callback();
        }
      };
      testabilities.forEach(function(testability) {
        testability.whenStable(decrement);
      });
    } else if (!window.angular) {
      throw new Error('window.angular is undefined.  This could be either ' +
          'because this is a non-angular page or because your test involves ' +
          'client-side navigation, which can interfere with Protractor\'s ' +
          'bootstrapping.  See http://git.io/v4gXM for details');
    } else if (window.angular.version >= 2) {
      throw new Error('You appear to be using angular, but window.' +
          'getAngularTestability was never set.  This may be due to bad ' +
          'obfuscation.');
    } else {
      throw new Error('Cannot get testability API for unknown angular ' +
          'version "' + window.angular.version + '"');
    }

The biggest difference is the simplification of the Angular 1 code. I could simply add the window.angular.getTestability check. For now I am going to move forward with this and then we can revisit this code.

Footnotes
---------

[1] Ok, not entirely true. I understand WebDriverJS and Protractor is asycronious javascript and thus when one makes a call to a function you may get the response back in some unknown amount of time or asycronously. Fine. But that is not what I want here. I want an answer back now telling me whether or not the current (now) state of Angular has any outstanding promises or whether or not it is waiting, right now. Don't delay. Thus I am making, conscientiously, a syncronous javascript call and then "waiting" or polling within the AngularJSlibrary.

[2] The statement that "whenever Protractor looks for an element" may not be entitrely true. If you read the code the waitForAngular call is when you are looking for "all" elements, as in ``element.all(by.id('notPresentElementID'))``. [See `protractor/lib/element.ts<https://github.com/angular/protractor/blob/6b7b6fb751f574056cb80b7238f62c77ef78497e/lib/element.ts#L168>`_]. It is unclear, to me without spending a lot more time tracing through the code atleast, that a call to say ``element(by.binding('username'))``, for example, would go through element.all and thus be invoking the implicit wait for angular.
