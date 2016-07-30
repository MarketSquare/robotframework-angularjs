Changelog
=========

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
