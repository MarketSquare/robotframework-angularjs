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
