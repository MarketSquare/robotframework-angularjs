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
