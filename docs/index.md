# BILLinois Documentation

## Directory structure

For new contributors to get familiarized with the repository.

```bash
+---apps # main app scripts
▒   +---accounts # django accounts and permissions
▒   ▒   +---migrations # django databases
▒   +---core # django app, including models and views
▒   ▒   +---migrations # django databases
+---config # setup and (local-only!) passwords
+---docs # documentation on API, databases, and architecture
▒   +---endpoints # API endpoints
+---project # to remove
▒   +---data # move to top level directory
▒   ▒   +---samples
▒   +---frontend # to remove, move to templates
+---static # to remove? move to templates
▒   +---bill_page
▒   +---css
▒   +---home_page
▒   +---root
+---templates # HTML pages
▒   +---account
▒       +---email
▒       +---messages
▒       +---snippets
+---tests # scripts to test app
+---_logs # output related to debugging
```