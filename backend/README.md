# Init
pipenv shell
set FLASK_APP=application
set FLASK_DEBUG=True
flask run


# Response Codes
101 -- invalid token
102 -- unauthorised access
200 -- successful
201 -- show error
401 -- invalid request (app tampered)


deta update -e .env
pip freeze > requirements.txt