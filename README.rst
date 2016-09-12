AngularJSLibrary - robotframework-angularjs
===========================================
An AngularJS extension to Robotframework's Selenium2Library

What is included
----------------
AngularJSLibrary provides keywords for finding elements by binding, model, and repeater. The library also provides a keyword for waiting on angular.

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
In order to use the keywords you have to include AngularJSLibrary in the settings section of your test. Note will will need to include the Selenium2Library **before** you import the AngularJSLibrary.

.. code::  robotframework

    *** Settings ***
    Library         Selenium2Library
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
If you need help with AngularJSLibrary, Selenium2Library, or Robot Framework usage, please post to the `user group for Robot Framework <https://groups.google.com/forum/#!forum/robotframework-users>`_.

Testing
-------
For information on how we test the AngularJSLibrary see the `Testing.rst`_ file.

References
----------

`Selenium2Library <https://github.com/robotframework/Selenium2Library>`_: Web testing library for Robot Framework

`Protractor <http://www.protractortest.org>`_: E2E test framework for Angular apps
