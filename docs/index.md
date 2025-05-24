# BILLinois Documentation

To view these docs in the local server, run `mkdocs serve localhost:8080`

## Directory structure

For new contributors to get familiarized with the repository.

```bash
+---apps # main app scripts
▒   +---accounts # django accounts and permissions
▒   ▒   +---migrations # django databases
▒   +---core # django app, including models and views
▒   ▒   +---migrations # django databases
+---config # setup and read in .env
+---docs # documentation on API, databases, and architecture
▒   +---endpoints # API endpoint documentation
+---project # to remove
▒   +---data # move to top level directory
▒   ▒   +---samples # test data for development
▒   +---frontend # move to templates
+---static # non-variable frontend files (CSS, images)
▒   +---css
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
.env # (local-only!) passwords
manage.py # runs django server
pyproject.toml # uv dependencies and requirements
mkdocs.yml # configurations for documentation generator
README.md
LICENSE.md
Justfile
```
