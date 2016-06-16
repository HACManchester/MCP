Initial structure for Manchester Hackspace's automation system.

Contributing
------------

The following rules apply to adding code to this application:

- all aspects should be created as logically grouped modules
- code should be Pythonic and commented throughout **USE DOCSTRINGS**
- Any dependencies added must be added to the requirements file
- verbose commit messages are encouraged
- Ideally, commits within pull requests should be squashed into sensible, atomic commits.

Please remember to purge all sensitive data before committing.

Initial Setup
-------------

First, set up a venv to install all your dependencies.

```
virtualenv --no-system-packages venv
```

Activate it, then use pip to install the requirements

```
source venv/bin/activate
pip install -r requirements.txt
```
