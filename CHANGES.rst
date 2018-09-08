Changelog
=========
0.0.9 (unreleased)
------------------
Fixes:

- Fixed issue when importing library into RIDE.
  [pekkaklarck][emanlove]

0.0.8 (2018-08-03)
------------------
Fixes:

- Fixed issue when no locator strategy was specified.
  [emanlove]

0.0.7 (2018-03-31)
------------------
Changes:

- Added support for SeleniumLibrary and dropped support for Selenium2Library.
  [emanlove]

Fixes:

- [Minor] Corrected error message.
  [emanlove]

0.0.6 (2017-06-12)
------------------
Changes:

- Allow for setting root selector when importing library.
  [emanlove]

0.0.5 (2017-06-09)
------------------
Changes:

- Added support for Angular 2 under `Wait For Angular` keyword.
  [emanlove]

- Updated documentation around Angular 2 development and testing.
  See TESTING.rst.
  [emanlove]
  
- Temporarily removed diagnostic call for retrieving pending HTTP
  requests when `Wait For Angular` keyword fails.
  [emanlove]

0.0.4 (2016-09-12)
------------------
Changes:

- Added implicit Wait on Angular when finding elements by locator.
  [emanlove]

- Added more documentation on testing the library and how the AngularJS
  Library is implementing the implicit wait for angular functionality.
  See TESTING.rst.
  [emanlove]

0.0.3 (2016-07-30)
------------------
Fixes:

- Fixed issue with binding locators when no stratergy specified, e.g.
    Click Element  {{example.binding}}

Changes:

- Removed interpolation brackets on Find By Binding criteria for
  AngularJS 1.3+ compatability.
  [emanlove]

- Changed the implementation of the `Wait For Angular` keyword.
  [emanlove]

- Added debug statements when `Wait For Angular` times out. Shows
  pending https requests only. The list of pending timeouts comes
  from functionality that Protractor adds. This has not yet be implemented
  in the AngularJSLibrary.
  [emanlove]

- Added documentation on testing the library. See TESTING.rst.
  [emanlove]

- Add library test cases.
  [Protractor Team][emanlove]

0.0.2 (2016-02-16)
------------------

Fixes:

- Updated documentation.
  [tisto][emanlove]

- Resolved issue when using implicit xpath and AngularJS Library.
  [emanlove]

0.0.1 (2016-02-06)
------------------

New:

- Initial Release
  [zephraph][emanlove]
