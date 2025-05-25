# BILLinois Code Testing Documentation

## Testing Process

Please follow the following steps to add unit tests for the analyses you are working on to this folder:

1. Create a file in the naming convention “test_COMPONENT.py” or “test_TYPE.py” to test a particular component of the project or to run a particular type of test. If this file already exists, add additional tests for the component in the same file, with a different name for each to avoid merge conflicts

   a. The QA team defers to all of you on what makes the most sense to split out into separate .py files vs. what makes sense to keep in one file. A placeholder list is included below for convenience, but please feel free to ignore this.

2. For a new file, add import pytest and any additional packages needed (e.g., playwright) at the top, then add the tests. For an existing file, please add at the bottom by default, or add where it makes the most sense in the flow of the tests.

3. If there are any fixtures (e.g., client or DB connections) or constants/utils (e.g., file paths) that will be used across multiple sets of tests, consider including those in a separate file in the tests folder and referencing them from within each set of tests that will use them.

4. Please update this file with a brief description of which tests are included in each file. As with all Git work, please be sure to only add to the sections you worked on to avoid merge conflicts on this file.

   a. You don’t necessarily need to document every single test you write in this file, but it would be helpful to have a general sense of what types of things we are testing for each aspect.

## General Notes

**Testing Frameworks**
pytest
Playwright

This documentation file is inspired by [that of last year’s New Arrivals project](https://github.com/uchicago-capp-30320/new-arrivals-chi/tree/main/tests). For more detailed notes on how each of last year’s teams set up their tests and what tools they use to potentially inform your choices, see the [“Notes on Prior Tests”](https://docs.google.com/document/d/1XJ0zdywhg9n6gdFrzgn_YjdU6KER-1qwdsTALVIPi1Q/edit?tab=t.0) file in the Google Drive.

The QA team will largely handle integration tests, please let us know if there are any that you think it would be particularly valuable to be sure to include, and if there are any that you have already completed.

## List of Tests

### API call Tests

test_XXX.py

### Data -> Backend Integration Tests

test_XXX.py

### Backend Tests

test_XXX.py

### Backend -> Frontend Integration Tests

test_XXX.py

### Frontend/Website Tests

test_e2e.py

- test_playwright_working: test that playwright import works
