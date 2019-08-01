"""An AngularJS extension to Robotframework's Selenium2Library

See:
http://robotframework.org/
https://github.com/Selenium2Library/robotframework-angularjs
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='robotframework-angularjs',
    version='0.0.10',
    description="""An AngularJS extension to Robotframework's Selenium2Library""",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Selenium2Library/robotframework-angularjs',
    author='Zephraph, Ed Manlove',
    author_email='zephraph@gmail.com, devPyPlTw@verizon.net',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    keywords='robotframework testing testautomation angular selenium webdriver',
    packages=find_packages(exclude=['docs']),
    install_requires=['robotframework', 'robotframework-seleniumlibrary'],
)
