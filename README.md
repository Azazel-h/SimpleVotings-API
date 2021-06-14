## URLs
###Login and Logout still doesn't work properly
### Accounts
```
api/accounts/signup - Registration. POST request. - JSON Example: {"email": "example@example.com", "username": "example", "password": "TestPassword"}
api/accounts/login/ - Authentication. POST request. - JSON Example: {"username": "example", "password": "example"}
api/accounts/logout/ - Logout. POST request.
api/accounts/profile - Getting all votings created by current user. GET request.
```
### Votings
```
api/votings/ - Getting a list of votings. GET request.
api/votings/ - Create new VOTING. POST request. - JSON Example: {"title": "VotingTestTitle"}
api/votings/{ id } Getting a VOTING by id. GET request.
api/votings/{ id } Creating a CHOICE by id. PUT request. - JSON Example: {"text": "ChoiceText"}
api/votings/{ id } Creating a VOTE by id. POST request. - JSON Example: {"text": "ChoiceText"}
```
