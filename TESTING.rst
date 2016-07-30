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

Modifying the test server of Selenium2Library, rf-s2l\test\resources\testserver\testserver.py, add the following method, do_GET, to the StoppableHttpRequestHandler class.

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
    
And if we activate our virtual Python instance we should see

.. code:: bash
	  
    # pip list
    decorator (4.0.10)
    docutils (0.12)
    pip (8.1.2)
    robotframework (3.0)
    selenium (2.53.6)
    setuptools (8.2.1)

Starting the modified testserver
--------------------------------

Open a new bash terminal from which we will run the test sever

.. code:: bash

    cd ng

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

It is important to understand what is going on in the underlying library and there are many reasons for that. For one as I continue to develop this library I realize some assumptions and thus implementations are simply wrong. I also have very narrow focus as my daily work focuses on a single (and usually older) version of AngularJS. So there could be issues I am not seeing and thus not addressing. These and many more reasons support the argument thats as a library user we should all be well informed as to how the library works and what is Protractor / AngularJS doing in the functions we are mimicing.

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

[You'll see here I am using the angular1 portion of testapp. Also I am using the alt_root_index so I can hardode which version of Angular1.x I'll want.] With the site running open the developers tools (F12) and in the console editor paste the following code, but before you run it let's tear it apart.

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

You will see a continual series of dots then stars printed to the console. Now on the async test page click the button label $timeout. Only dots are printed to the console for some time. Then only stars. What is happening at this time? When only the dots are outputed we are waiting for angular. And when just the stars are print, its all those callbacks returning while we were waiting for angular to complete. God ahead and some of the other asyncrouous actions on the async page and see what the output is.

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

I went through a couple interations before settling on the above. Let me go through the syncronous javascript script. First, I like the simplicity of it. One iteration had a couple of calls to notifyWhenNoOutstandingRequests()
