AngularJSLibrary - robotframework-angularjs
===========================================
An AngularJS and Angular extension to Robotframework's SeleniumLibrary.
AngularJSLibrary primarily provides functionality to deal with **waiting** and
thus timing issue when testing Angular based websites. The library does this by
providing first an implicit wait and, subsequently, an explicit keyword for
waiting on angular.

About this library
------------------
The AngularJSLibrary, despite the name including JS, supports testing against
both Angular 2.0+ (known as simply Angular) and Angular 1.0 (also known as
Angular JS).

This library is considered mature and feature complete. Ongoing support is
provided through the Robot Framework community Slack. Thus it may appear
to be abandoned or neglected for which it is not.

**Please carefully read through this README in its entirety**. It covers how
to configure and import the library into your test scripts, use and understand
its key functionality, as well as troubleshooting and debugging information.

Installation
------------
To install **AngularJSLibrary**, run:

.. code:: bash

    pip install robotframework-angularjs


Alternatively, to install from source:

.. code:: bash

    python setup.py install


Identifying the Angular root element
------------------------------------
Prior to importing the library, one must identify the Angular root element or root
component. For more information about 

Here are a few examples of Angular sites and their corresponding root elements or
components. The first example is from the `AngularJS.org PhoneCat tutorial <http://angular.github.io/angular-phonecat/step-14/app>`_.
The base html code is

.. code::  html

    <html lang="en" ng-app="phonecatApp">
      <head>
        <!-- ... -->
      </head>
      <body>
    
        <div class="view-container">
          <div ng-view class="view-frame"></div>
        </div>
    
      </body>
    </html>

In the PhoneCat tutorial the html element with the ng-app attribute is the root
element. Thus for this website the root selector would be :code:`[ng-app]`. The
next example is the `Getting started with Angular tutorial <https://angular.io/start>`_
on angular.io site. It's main html looks like

.. code::  html

    <!DOCTYPE html>
    <html lang="en">
      <head>
        <!-- ... -->
      </head>
      <body>
        <app-root></app-root>
      </body>
    </html>

Here the root component is the app-root element and thus the root selector for
this website would be :code:`app-root`. The last example is the `example tab of
the Dialog UI component <https://material.angular.io/cdk/dialog/examples>`_
within the Angular.io Component Dev Kit (CDK).

.. code::  html

    <!DOCTYPE html><html lang="en-US"><head>
    <!-- ... -->
    </head>
    

    <body class="docs-app-background">
      <material-docs-app></material-docs-app>
      <!-- ... -->
    
    </body></html>

The root component for the Dialog component example page is the material-docs-app
element. The root selector will be :code:`material-docs-app`.

Now we will use the root selector when we import the library.

Importing the library
---------------------
The proper name for importing the library is :code:`AngularJSLibrary`. You will
need to include the SeleniumLibrary **before** you import the AngularJSLibrary.
The first of two library options is `root_selector`. So using our first example,
the PhoneCat tutorial from AngularJS.org above, our import may look like,

.. code::  robotframework

    *** Settings ***
    Library    SeleniumLibrary
    Library    AngularJSLibrary    root_selector=[ng-app]
    
    *** Test Cases ***
    Search Through The Phone Catalog For Samsung Phones
        Open Browser  http://angular.github.io/angular-phonecat/step-14/app  Chrome
        Input Text  //input  Samsung
        Click Link  Samsung Galaxy Tab™
        Element Text Should Be    css:phone-detail h1    Samsung Galaxy Tab™

As the default value for the root_selector argument is :code:`[ng-app]`, for
the PhoneCat tutorial we did not need to specify the root_selector and could
have written the Library import as

.. code::  robotframework

    *** Settings ***
    Library    SeleniumLibrary
    Library    AngularJSLibrary
    
    *** Test Cases ***
    Search Through The Phone Catalog For Samsung Phones
        Open Browser  http://angular.github.io/angular-phonecat/step-14/app  Chrome
        Input Text  //input  Samsung
        Click Link  Samsung Galaxy Tab™
        Element Text Should Be    css:phone-detail h1    Samsung Galaxy Tab™

*If you get an "Unable to find root selector ..." error* then you should re-check
your root_selector. Note that unlike locators used with the SeleniumLibrary the
root_selector **should not** contain the css locator prefix.

The second library option, ignore_implicit_angular_wait, is a flag which when
set to True the AngularJS Library will not wait for Angular $timeouts nor
$http calls to complete when finding elements by locator. The default value is
False.

*If the application under test starts on a non angular page,* for example a
login page that is not angular which leads into an angular app, then one should
start with the implicit angular wait turned off. For example,

.. code::  robotframework

    *** Settings ***
    Library    SeleniumLibrary
    Library    AngularJSLibrary    ignore_implicit_angular_wait=True
    
    *** Test Cases ***
    Login Into Non Angular Page
        # ...

Usage of the Waiting functionality
----------------------------------
The AngularJS Library provides two types of waiting: a built-in implicit wait
that automatically waits when using a locator strategy and then an explicit
keyword that one calls out or writes into their script. In the tutorial and
examples above the scripts there aren't any expicit wait calls. Here instead
the script is relying on the implicit wait which by default is turned on.
This means as soon as you import the library you will have waiting enabled.

This can be demostrated by importing the library with the implicit wait turned
off and using instead the library's explicit `Wait For Angular` keyword.

.. code::  robotframework

    *** Settings ***
    Library    SeleniumLibrary
    Library    AngularJSLibrary    ignore_implicit_angular_wait=True
    
    *** Test Cases ***
    Search Through The Phone Catalog For Samsung Phones
        Open Browser  http://angular.github.io/angular-phonecat/step-14/app  Chrome
        Wait For Angular
        Input Text  //input  Samsung
        Wait For Angular
        Click Link  Samsung Galaxy Tab™
        Wait For Angular
        Element Text Should Be    css:phone-detail h1    Samsung Galaxy Tab™

With the implicit wait functionality it is expected that most of the situations
where waiting is needed will be handled "automatically" by this "hidden" implicit
wait. Thus if one examined your test case they would not see many, if any,
`Wait For Angular` keywords but instead would see actions keywords with no
"waiting" keywords in between actions. There are times, though, when one needs to
explicitly call out to wait for angular. For example when using a SeleniumLibrary
keyword that does not use a locator strategy, like :code:`Alert Should Be Present`
and :code:`Page should contain`, or if you use webelement.

In addition to the option to turn off the implicit wait on library import, you
may turn it off using the :code:`Set Ignore Implicit Angular Wait` keyword with
an argument of :code:`${True}`. 


Understanding and verifying the angular waits
---------------------------------------------
Although the waits seem like "Magic" they are not. Let's look into how the
waits are implimented and work to gain insight as to how they work. The waits,
both the implicit and explicit, poll what I call the "angular queue".
Technically it is checking that angular has "finished rendering and has no
outstanding $http or $timeout calls". It does this by checking the
`notifyWhenNoOutstandingRequests` function for AngularJS applications. For
Angular applications the library is checking the `isStable` function on the
Angular Testibility service.

This can be seen within the log file by setting the loglevel to DEBUG or TRACE.
Rerunning the PhoneCat demo (:code:`robot --loglevel DEBUG demo_phonecat.robot`)
one should see in the log file

.. code::  robotframework

    20:01:04.658	INFO	Typing text 'Samsung' into text field '//input'.	
    20:01:04.658	DEBUG	POST http://localhost:50271/session/f75e7aaf5a00c717ae5e4af34a6ce516540611dae4b7f6079ce1a753c308cde2/execute/sync {"script": "...snip..."]}	
    20:01:04.661	DEBUG	http://localhost:50271 "POST /session/f75e7aaf5a00c717ae5e4af34a6ce516540611dae4b7f6079ce1a753c308cde2/execute/sync HTTP/1.1" 200 14	
    20:01:04.661	DEBUG	Remote response: status=200 | data={"value":true} | headers=HTTPHeaderDict({'Content-Length': '14', 'Content-Type': 'application/json; charset=utf-8', 'cache-control': 'no-cache'})	
    20:01:04.661	DEBUG	Finished Request	

For space reasons I snipped out the core script on the POST execute/sync line.
One should see these lines repeated several times over. This is the polling the
library is doing to see if the application is ready to test. It will repeat
this query till either it returns true or it will repeat till the "give up"
timeout. If it gives up, it will silently and gracefully fail continuing onto
the actions it was waiting to perform. It is important for the user of this
library to see and understand, at a basic level, this functionality. As the
primary usage are these implicit, and thus hidden, waits it is key to see how
to check the library is operating properly and when it is waiting.

*When using the AngularJS Library, if all waits timeout then the AngularJS
Library may not wait properly with that application under test.* This,
recalling all previously outlined information, is telling you that the
Angular app is constantly busy. This can happen depending on how the angular
application is designed. It may also affect only a portion of the application
so it is important to test out various parts of the application.

Further debugging techniques
----------------------------
In addition to using the AngularJS Library, one can use the Browser's DevTools
as a way to test out and demonstrate the core operation of the library against
an application. To be clear, this is not library code but similar Javascript
code which one uses outside of robot to exhibit, to a dev team for example,
what the library is seeing when it querys the application. When viewing the
application under test open the DevTools, preferably under Chrome, and on the
Console tab type the following,

If the application is built with AngularJS or Angular 1.x then the script is

.. code::  javascript

    var callback = function () {console.log('*')}
    var el = document.querySelector('[ng-app]');
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

For Angular v2+ then the script is

.. code::  javascript

    var callback = function () {console.log('*')}
    var el = document.querySelector('material-docs-app');
    var h = setInterval(function w4ng() {
        console.log('.');
        try {
            var readyToTest = window.getAngularTestability(el).isStable();
        } catch (err) {
          console.log(err.message);
          callback(err.message);
        }
        if (!readyToTest) {
          callback()
        } else {
          console.log('.');
        }
      }, 10);

This will display a :code:`.` when "stable". Otherwise it will show a :code:`*`
when "busy". To shut down the javascript interval and stop this script type on
the console prompt :code:`clearInterval(h);`. [Chrome Browser is preferred
because repeated output within its DevTools console will be displayed as a
single line with a count versus a new line for each output making it much
easier to see and read.] I have personally used this myself both in developing
this library as well as demonstrating to various Angular developers how a
design/implementation is blocking testability.

Usage of the Angular Specific Locator Strategies
-------------------------------------------------
The new locator strategies include

.. code::

    binding=
    model=
    repeater=


For example, you can look for an Angular ng-binding using

.. code::  robotframework

    Get Text  binding={{greeting}}


or by using partial match

.. code::  robotframework

    Get Text  binding=greet


or by simply using the binding {{…}} notation

.. code::  robotframework

    Get Text  {{greeting}}


One can also find elements  by model

.. code::  robotframework

    Input Text  model=aboutbox  Something else to write about

    
.. role:: rf(code)
   :language: robotframework

Finally there is the strategy of find by repeat. This takes the general form of :rf:`repeater=some ngRepeat directive@row[n]@column={{ngBinding}}`. Here we specify the directive as well as the row, an zero-based index, and the column, an ngBinding. Using this full format will return, if exists the element matching the directive, row and column binding.  One does not need to specify the row and column but can specify either both, one or the other or neither. In such cases the locator may return  list  of elements or even a list of list of elements. Also the ordering of row and column does not matter; using :rf:`repeater=baz in days@row[0]@column=b` is the same as :rf:`repeater=baz in days@column=b @row[0]`.


Getting Help
------------
If you need help with AngularJSLibrary, SeleniumLibrary, or Robot Framework usage, please reach out within the Robot Framework community `Slack <>`_ [`Invite to join community slack <https://rf-invite.herokuapp.com/>`_].

    
Keyword Documentation
---------------------
The keyword documentation can be found on the `Github project page <https://marketsquare.github.io/robotframework-angularjs/>`_.


Testing
-------
For information on how we test the AngularJSLibrary see the `Testing.rst <https://github.com/Selenium2Library/robotframework-angularjs/blob/master/TESTING.rst>`_ file.


References
----------

`SeleniumLibrary <https://github.com/robotframework/SeleniumLibrary>`_: Web testing library for Robot Framework

`Protractor <http://www.protractortest.org>`_: E2E test framework for Angular apps

`isStable reference <https://angular.io/api/core/ApplicationRef#is-stable-examples>`_

`Angular Testability service <https://angular.io/api/core/Testability>`_
