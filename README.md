# BILLinois

A friendly civic engagement tool that notifies users about their favorite bills. BILLinois allows users to search bills by topic, view additional information about each bill, and login to add bills of interest and sign up for notifications about those bills of interest.

BILLinois's initial focus is on the Illinois General Assembly, but a long-term goal of the project is to expand either to additional states or to additional levels of government.


## Contributing

This project uses uv to manage dependencies.

To install and use uv, please take the following steps:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run `uv sync` to sync your local `.venv` with the requirements in `pyprojects.toml`
3. Run `uv tool install ruff` to install the [Ruff](https://github.com/astral-sh/ruff) linter
4. Run `uv add --dev pytest` to get setup with testing (this is a development package not included in the requirements)
5. Before pushing commits, run `ruff format` and `ruff check` to ensure you don't get shamed by Ruff

## Repository Layout

* `project`: includes main app script (frontend and backend)
* `data`: contains data files used in project
* `tests`: contains all tests related to the project


## Development

This project was created by University of Chicago MSCAPP students as a class project for [Software Engineering for Civic Tech](https://capp30320.jpt.sh/), taught by Professor [James Turk](https://www.jpt.sh/).

Development Team

    Livia Mucciolo
    
    Echo Nattinger 
    
    Joaquin Pinto 
    
    Caitlin Pratt 
    
    David Steffen
    
    Suchi Tailor
    
    Karen Yi