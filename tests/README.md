# BILLinois Code Testing Documentation

## General Information

**Testing Frameworks**
pytest-django
pytest-playwright

This documentation file is inspired by [that of the Spring 2024 New Arrivals project](https://github.com/uchicago-capp-30320/new-arrivals-chi/tree/main/tests).

## List of Tests

### Models Tests: test_models.py

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

  Test that a favorite can be pulled from a user ID and a bill ID

  Test the uniqueness constraint

- Topics model tests: test_get_specific_topic_from_id, test_get_all_topic_from_id

  Test getting a specific topic from the topics table for a bill

  Test getting all the topics from the table for a bill

- Updates table tests: test_update_created, test_get_update_from_id, test_updates_table_uniqueness

  Test that updates can be created as expected

  Test that an update can be searched for by bill and action IDs

  Test uniqueness constraint

### Views Tests: test_views.py

- Home view tests: test_home_status, test_home_content

  Test that the home page loads

  Test that the home page has the expected content

- Search view tests: test_create_search, test_search_content, test_create_search_real, test_search_content_real, test_create_search_by_state, test_search_content_by_state_real

  Test that searches worked, both for real and test queries and by state

  Test that the test query returned no results as expected

  Test that the real query returned the expected bills

  Test that a real query limited by state returned the expected bill

- Bill page view tests: test_create_bill_view_by_id, test_bill_view_by_id_content, test_create_bill_view_by_info, test_bill_view_by_info_content

  Test that a bill page can be created, both by bill ID and by state/session/bill number

  Test that the bill page loads the expected bill information, both when created by bill ID and when created by state/session/bill number

### Frontend/Website Tests: test_e2e.py

- test_playwright_working: test that playwright import works
