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
▒   ▒   +---samples # test data for development
▒   +---frontend # move to templates
+---static # non-variable frontend files (CSS, images)
▒   +---bill_page # move to templates
▒   +---css
▒   +---home_page # move to templates
▒   +---root
▒       +---robots.txt # defines policies for web scrapers
+---templates # HTML pages
▒   +---account
▒       +---email # emails sent to users
▒       +---messages # popups ?
▒       +---snippets # partial pages
+---tests # scripts to test app
+---_logs # output related to debugging
.pre-commit-config.yaml # automated hooks such as linting and formatting
manage.py # runs django server
pyproject.toml # uv dependencies and requirements
README.md
LICENSE.md
Justfile
```