AngularJSLibrary - robotframework-angularjs
===========================================
An AngularJS and Angular extension to Robotframework's SeleniumLibrary

About the support for various Angular and Selenium Library versions
-------------------------------------------------------------------
As of AngularJSLibrary version 0.0.7 (31 March, 2018 release) only the SeleniumLibrary is supported (despite the name of the GITHUB group hosting the library).

The AngularJSLibrary, despite the name including JS, supports both Angular 2.0+ (known as simply Angular) and Angular 1.0 (also known as Angular JS).


What is included
----------------
AngularJSLibrary provides functionality in two key areas: angular specific **locator strategies** and **waiting**. Just as there are strategies provide by the SeleniumLibrary for locating elements by ID, CSS, or xPath, this library adds startegies for finding elements by binding, model, and repeater. The library also provides both an explicit keyword for waiting on angular and an implicit wait.


Installation
------------
To install **AngularJSLibrary**, run:

.. code:: bash

    pip install robotframework-angularjs


Alternatively, to install from source:

.. code:: bash

    python setup.py install

    
Keyword Documentation
---------------------
The keyword documentation can be found on the `Github project page <http://selenium2library.github.io/robotframework-angularjs/>`_.


Importing the library
---------------------
In order to use the keywords you have to include AngularJSLibrary in the settings section of your test or test suite. Note will will need to include the SeleniumLibrary **before** you import the AngularJSLibrary.

.. code::  robotframework

    *** Settings ***
    Library         SeleniumLibrary
    Library         AngularJSLibrary
    ...
    
    *** Test Cases ***
    Go To  localhost:8080
    Wait for Angular
    ...

There are currently two library options: root_selector, ignore_implicit_angular_wait. root_selector allows the user to set the Angular root element (AngularJS) or root component (Angular). The default value is :code:`[ng-app]` and is a CSS selector; more specifically an attribute selector looking for an element with the attribute :code:`ng-app`. Starting in AngularJSLibrary version 0.0.10 if the root selector query fails an error is thrown noting the library is "[u]nable to find root selector ...". To resolve this issue one must discover the root element or component within the Angular appliction under test.

ignore_implicit_angular_wait is a flag which when set to True the AngularJS Library will not wait for Angular $timeouts nor $http calls to complete when finding elements by locator. As noted in the Protractor documentation "this should be used only when necessary, such as when a page continuously polls an API using $timeout." The default value is False.


Usage of the Waiting functionality
----------------------------------
The AngularJS Library provides two types of waiting; a explicit keyword that one calls out or writes into their script and then an built-in implicit wait that automatically waits when using a locator strategy. Note currently the implicit wait is not invoked when using a web element as the locator. By default the implicit is turned on. This means as soon as you import the library you will have waiting enabled.

You may turn off the implicit wait by either using the :code:`Set Ignore Implicit Angular Wait` keyword with an argument of :code:`${True}` or when importing the library. For some testing situations, for example the initial login page is non-angular, one may want to start without the implicit waiting enabled.

With the implicit wait functionality it is expected that most of the situations where waiting is needed will be handled "automatically" by this "hidden" implicit wait. Thus if one examined your test case they would not see many, if any, `Wait For Angular` keywords but instead would see actions keywords with no "waiting" keywords in between actions. There are though times when one needs to explicitly call out to wait for angular. For example when using a SeleniumLibrary keyword that does not use a locator strategy, like :code:`Alert Should Be Present` and :code:`Page should contain ...`, or if you use webelement.


Usage of the Angular Specific Locator Stratergies
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
If you need help with AngularJSLibrary, SeleniumLibrary, or Robot Framework usage, please post to the `user group for Robot Framework <https://groups.google.com/forum/#!forum/robotframework-users>`_.


Testing
-------
For information on how we test the AngularJSLibrary see the `Testing.rst <https://github.com/Selenium2Library/robotframework-angularjs/blob/master/TESTING.rst>`_ file.


References
----------

`SeleniumLibrary <https://github.com/robotframework/SeleniumLibrary>`_: Web testing library for Robot Framework

`Protractor <http://www.protractortest.org>`_: E2E test framework for Angular apps
