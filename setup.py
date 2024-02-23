"""An AngularJS/Angular extension to Robotframework's SeleniumLibrary

See:
http://robotframework.org/
https://github.com/MarketSquare/robotframework-angularjs
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
    version='1.0.0',
    description="""An AngularJS/Angular extension to Robotframework's SeleniumLibrary""",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/MarketSquare/robotframework-angularjs',
    author='Zephraph, Ed Manlove',
    author_email='emanlove@verizon.net',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Framework :: Robot Framework',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ],
    keywords='robotframework testing testautomation angular selenium webdriver',
    packages=find_packages(exclude=['docs']),
    install_requires=['robotframework', 'robotframework-seleniumlibrary'],
)
