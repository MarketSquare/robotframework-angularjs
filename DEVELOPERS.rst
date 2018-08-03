Release procedures
------------------
These are the steps to build and push out a release of the AngularJS Library.

.. code::  bash

    virtualenv -p /usr/bin/python2.7 --no-site-packages release-python27-env
    
    source release-python27-env/bin/activate
    
    pip install -U pip
    pip install twine wheel
    
    python setup.py sdist bdist_egg bdist_wheel
    
    twine upload -r pypi dist/*

Alternatively one can specify the username to use on the public repository, in
this case PyPI, using

.. code::  bash

    twine upload -r pypi -u <username> dist/*

Finally to tag the repository use

.. code::  bash

    git tag -a v0.0.5 -m "0.0.5 release"
    git push --tags

Note if one forgets to tag a release and needs to do so after later commits have
been made, one can use

.. code::  bash

    git tag -a v0.0.5 -m "0.0.5 release" <commit>

to tag a specified commit.

Current Steps to Setup Development Environment and Run Tests
------------------------------------------------------------
Here are the current (as of Aug. 3, 2018, selenium==3.14.0, robotframework-seleniumlibrary==3.2.0.dev1, protractor==5.4.0) instructions for setting up the development environment and running the tests

.. code::  bash

    mkdir locator
    cd locator/
    git clone https://github.com/robotframework/SeleniumLibrary.git rf-sl
    git clone https://github.com/Selenium2Library/robotframework-angularjs.git rf-ng
    git clone https://github.com/angular/protractor.git ptor
    
    virtualenv -p /usr/bin/python2.7 --no-site-packages cl-py27-env
    source cl-py27-env/bin/activate
    pip install robotframework robotstatuschecker mockito selenium
    
    patch rf-sl/atest/resources/testserver/testserver.py rf-ng/AngularJSLibrary/testserver.py.patch 
    
    cp -R ptor/testapp rf-sl/atest/resources/.
    
    cp rf-ng/AngularJSLibrary/async.html rf-sl/atest/resources/testapp/ng1/async/.
    cp rf-ng/AngularJSLibrary/async.js rf-sl/atest/resources/testapp/ng1/async/.
    
    cp rf-ng/AngularJSLibrary/angular.robot rf-sl/atest/acceptance/locators/.
    cp rf-ng/AngularJSLibrary/angular_wait.robot rf-sl/atest/acceptance/keywords/.
    
    cd rf-sl
    python atest/run.py FF --suite angular --pythonpath ../rf-ng

