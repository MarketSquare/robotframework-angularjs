AngularJSLibrary - robotframework-angularjs
===========================================
An AngularJS and Angular extension to Robotframework's SeleniumLibrary

What is included
----------------
AngularJSLibrary provides keywords for finding elements by binding, model, and repeater. The library also provides both an explicit keyword for waiting on angular and an implicit wait.

About the support for various Angular and Selenium Library versions
-------------------------------------------------------------------
As of AngularJSLibrary version 0.0.7 (31 March, 2018 release) only the SeleniumLibrary is supported (despite the name of the GITHUB group hosting the library).

The AngularJSLibrary, despite the name including JS, supports both Angular 2.0+ (known as simply Angular) and Angular 1.0 (also known as Angular JS).

Installation
------------
To install **AngularJSLibrary**, run:

.. code:: bash

    pip install robotframework-angularjs


Alternatively, to install from source:

.. code:: bash

    python setup.py install

    

Keyword Usage
-------------
In order to use the keywords you have to include AngularJSLibrary in the settings section of your test. Note will will need to include the SeleniumLibrary **before** you import the AngularJSLibrary.

.. code::  robotframework

    *** Settings ***
    Library         SeleniumLibrary
    Library         AngularJSLibrary
    ...
    
    *** Test Cases ***
    Go To  localhost:8080
    Wait for Angular
    ...


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
