# Simple API created with DjangoRestFramework</br>
> - Understandable and easy to change</br>
> - Feel free to use in your own purposes</br>
## Installation
```
git clone https://github.com/Azazel-h/SimpleVotings-API.git
cd SimpleVotings-API
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## URLs

> #### IMPORTANT: YOU WILL GET AN AUTHTOKEN AFTER LOGIN IN 
> Include it in your request's headers like this <br/> 
> - { Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b }


#### Accounts (Authtoken needed: PROFILE, LOGOUT)
```
api/accounts/signup/ - Registration. POST request. - JSON Example: {"email": "example@example.com", "username": "example", "password": "TestPassword", "password2": "TestPassword"}
api/accounts/login/ - Authentication. POST request. - JSON Example: {"username": "example", "password": "example"} - YOU WILL GET AN AUTHTOKEN AFTER LOGGING IN -
api/accounts/logout/ - Logout. POST request. - DELETE AUTHTOKEN -
api/accounts/profile/ - Getting all votings created by current user. GET request.
```
#### Votings (Authtoken needed)
```
api/votings/list/ - Getting a list of votings. GET request.
api/votings/list/ - Create new VOTING. POST request. - JSON Example: {"title": "VotingTestTitle", "type": 0-Can vote only for one choice || 1-Can vote for every choice}
api/votings/id/ - Getting a VOTING by id. GET request.
api/votings/id/ - Creating a CHOICE by id. PUT request. - JSON Example: {"text": "ChoiceText"}
api/votings/id/ - Creating a VOTE by id. POST request. - JSON Example: {"choice": choice_id}
```
