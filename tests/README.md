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
pytest-django
pytest-playwright

This documentation file is inspired by [that of the Spring 2024 New Arrivals project](https://github.com/uchicago-capp-30320/new-arrivals-chi/tree/main/tests).

## List of Tests

### Models Tests

test_models.py

- Bill model tests: test_bill_created, test_get_bill_from_number

   Test that bills can be created with the correct fields

   Test that a bill can be searched for by number

- Action model tests: test_action_created, test_action_from_id

   Test that actions can be created with the correct ID and fields

   Test pulling an action from a bill ID and action ID

- User model tests: test_user_name, test_get_full_name, test_get_short_name, test_clean_email

   Test that users can be created with the correct fields

   Test fields of user name and short name

   Test the cleaning function for user email inputs

- Favorites model tests: test_get_favorite_from_user_and_bill, test_favorites_table_uniqueness

- 

### Views Tests

test_views.py

### Frontend/Website Tests

test_e2e.py

- test_playwright_working: test that playwright import works
