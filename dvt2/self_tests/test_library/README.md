# Test Library for Linux Embedded Environmental
---


## Unit Tests
The unit tests are located inside of `tests`.

To Be Run:
- `cd qa/test_library`
- `pytest tests/`

## Test Suites
There are already Test Suites that the Pengiun Team created. You can use it as
a starting point for other Test Suites.

The Test Suite folder is `../robot_tests`.

## Documentation
Every method is documented inside of the code.
If you want to export the documentation in a single HTML file, please do:

`pydoc -w test_library.module`. e.g. `pydoc -w test_library.helper`

It will create a module.html file in the working folder.
