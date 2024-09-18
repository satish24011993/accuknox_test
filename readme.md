create env - environment variables

virtualenv env

activate env:

source env/bin/activate

install packages:
pip install django
pip install django-restframeworks

clone the project:
git clone 'link from git'

Testing the API's:

1. Signup
Endpoint: POST /signup/

Description: Register a new user with email, username, and password.

Request:

curl -X POST http://localhost:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "securepassword123"
      }'

Response(201 Created):

{
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com"
}

2. Login
Endpoint: POST /login/

Description: Authenticate a user and receive an authentication token.

Request:

curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "password": "securepassword123"
      }'

Response (200 OK):

{
    "token": "auth_token_here"
}

3. Search Users
Endpoint: GET /search/?q=keyword&page=1

Description: Search for users by email or name.

Headers:

Authorization: Token your_auth_token_here

Request:

curl -X GET "http://localhost:8000/search/?q=john" \
  -H "Authorization: Token your_auth_token_here"


Response (200 OK):

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        }
    ]
}


Example: Search by Exact Email

curl -X GET "http://localhost:8000/search/?q=john.doe@example.com" \
  -H "Authorization: Token your_auth_token_here"


Response:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        }
    ]
}

4. Send Friend Request
Endpoint: POST /send-friend-request/<user_id>/

Description: Send a friend request to another user.

mention in Headers:

Authorization: Token your_auth_token_here
Content-Type: application/json

Request:

Suppose you want to send a friend request to a user with id=2.

curl -X POST http://localhost:8000/send-friend-request/2/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"


Response (200 OK):

{
    "status": "Friend request sent."
}

Note: If you send more than 3 friend requests within a minute, you will receive a throttling error.

Throttling Error Response (429 Too Many Requests):

{
    "detail": "Request was throttled. Expected available in 60 seconds."
}

5. Respond to Friend Request
Endpoint: POST /respond-friend-request/<request_id>/

Description: Accept or reject a friend request.

Headers:

Authorization: Token recipient_auth_token_here
Content-Type: application/json


Request:

Assuming the friend request has an id=1 and you want to accept it.

curl -X POST http://localhost:8000/respond-friend-request/1/ \
  -H "Authorization: Token recipient_auth_token_here" \
  -H "Content-Type: application/json" \
  -d '{
        "action": "accept"
      }'


Response (200 OK):

{
    "status": "Friend request accepted."
}

To Reject the Friend Request:

Change the action to "reject".


6. List Friends
Endpoint: GET /friends/

Description: Retrieve a list of friends.

Headers:

Authorization: Token your_auth_token_here
Request:

curl -X GET http://localhost:8000/friends/ \
  -H "Authorization: Token your_auth_token_here"
Response (200 OK):

[
    {
        "id": 2,
        "username": "janedoe",
        "email": "jane.doe@example.com",
        "first_name": "",
        "last_name": ""
    }
]
7. List Pending Friend Requests
Endpoint: GET /friend-requests/

Description: List incoming friend requests that are pending.

Headers:

Authorization: Token your_auth_token_here
Request:

curl -X GET http://localhost:8000/friend-requests/ \
  -H "Authorization: Token your_auth_token_here"
Response (200 OK):

[
    {
        "id": 3,
        "from_user": {
            "id": 3,
            "username": "bobsmith",
            "email": "bob.smith@example.com",
            "first_name": "",
            "last_name": ""
        },
        "to_user": {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        },
        "status": "pending",
        "timestamp": "2023-10-01T12:34:56Z"
    }
]

8. Throttling Friend Requests
Description: Users cannot send more than 3 friend requests within a minute.

Test Case:

Action: Attempt to send 4 friend requests within one minute.
Expected Outcome: The fourth request should be throttled.
Example:


# Send first friend request
curl -X POST http://localhost:8000/send-friend-request/2/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send second friend request
curl -X POST http://localhost:8000/send-friend-request/3/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send third friend request
curl -X POST http://localhost:8000/send-friend-request/4/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send fourth friend request (should be throttled)
curl -X POST http://localhost:8000/send-friend-request/5/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"


Fourth Request Response (429 Too Many Requests):

{
    "detail": "Request was throttled. Expected available in 60 seconds."
}


9. Pagination in Search
Description: The search results are paginated with 10 records per page.

Request:

curl -X GET "http://localhost:8000/search/?q=j&page=2" \
  -H "Authorization: Token your_auth_token_here"
Response:

{
    "count": 25,
    "next": "http://localhost:8000/search/?q=j&page=3",
    "previous": "http://localhost:8000/search/?q=j&page=1",
    "results": [
        // List of users 11-20 matching the search query
    ]
}

10. Error Handling Examples
Invalid Credentials on Login:

curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "password": "wrongpassword"
      }'
Response (400 Bad Request):

{
    "error": "Invalid Credentials"
}
Sending Friend Request to Non-existent User:

curl -X POST http://localhost:8000/send-friend-request/9999/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"
Response (404 Not Found):

{
    "detail": "Not found."
}
Attempting to Send Duplicate Friend Request:

If you try to send a friend request to a user you've already sent a request to:

Response (400 Bad Request):

{
    "error": "Friend request already sent."
}

11. Authentication
Description: All API endpoints (except signup and login) require authentication.

Headers:

Include the Authorization header in the format:

Authorization: Token your_auth_token_here
Example:

curl -X GET http://localhost:8000/friends/ \
  -H "Authorization: Token your_auth_token_here"
Unauthorized Request Example:

If you omit the Authorization header:

Response (401 Unauthorized):

{
    "detail": "Authentication credentials were not provided."
}

12. Using Postman
If you prefer to use Postman, here's how you can set up requests:

Set the Base URL: http://localhost:8000/
Headers:
For authenticated requests, add a header Authorization with value Token your_auth_token_here.
For JSON data, set Content-Type to application/json.
Body:
Use the raw option and select JSON for the body content.
Method:
Choose the appropriate HTTP method: GET, POST, etc.
13. Additional Notes
Creating Multiple Users for Testing: To fully test the friend request functionality, create multiple user accounts using the signup endpoint.
Retrieving Friend Request IDs: When you send or receive friend requests, the API may not return the request ID directly. Use the pending friend requests endpoint to list them and retrieve their IDs for accepting or rejecting.
Date and Time Format: The timestamp in friend requests is in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).



Thought for 32 seconds

Certainly! Below are examples of how to test the APIs you have set up, including sample requests and expected responses. We'll use curl commands for demonstration, but you can use tools like Postman or any REST client of your choice.

Prerequisites
Base URL: Assume the API is hosted at http://localhost:8000/.
Headers: For authenticated requests, include the Authorization header with the token received from the login endpoint.
1. Signup
Endpoint: POST /signup/

Description: Register a new user with email, username, and password.

Request:

bash
Copy code
curl -X POST http://localhost:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "securepassword123"
      }'
Response (201 Created):

json
Copy code
{
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com"
}
2. Login
Endpoint: POST /login/

Description: Authenticate a user and receive an authentication token.

Request:

bash
Copy code
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "password": "securepassword123"
      }'
Response (200 OK):

json
Copy code
{
    "token": "your_auth_token_here"
}
3. Search Users
Endpoint: GET /search/?q=keyword&page=1

Description: Search for users by email or name.

Headers:

http
Copy code
Authorization: Token your_auth_token_here
Request:

bash
Copy code
curl -X GET "http://localhost:8000/search/?q=john" \
  -H "Authorization: Token your_auth_token_here"
Response (200 OK):

json
Copy code
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        }
    ]
}
Example: Search by Exact Email

bash
Copy code
curl -X GET "http://localhost:8000/search/?q=john.doe@example.com" \
  -H "Authorization: Token your_auth_token_here"
Response:

json
Copy code
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        }
    ]
}
4. Send Friend Request
Endpoint: POST /send-friend-request/<user_id>/

Description: Send a friend request to another user.

Headers:

http
Copy code
Authorization: Token your_auth_token_here
Content-Type: application/json
Request:

Suppose you want to send a friend request to a user with id=2.

bash
Copy code
curl -X POST http://localhost:8000/send-friend-request/2/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"
Response (200 OK):

json
Copy code
{
    "status": "Friend request sent."
}
Note: If you send more than 3 friend requests within a minute, you will receive a throttling error.

Throttling Error Response (429 Too Many Requests):

json
Copy code
{
    "detail": "Request was throttled. Expected available in 60 seconds."
}
5. Respond to Friend Request
Endpoint: POST /respond-friend-request/<request_id>/

Description: Accept or reject a friend request.

Headers:

http
Copy code
Authorization: Token recipient_auth_token_here
Content-Type: application/json
Request:

Assuming the friend request has an id=1 and you want to accept it.

bash
Copy code
curl -X POST http://localhost:8000/respond-friend-request/1/ \
  -H "Authorization: Token recipient_auth_token_here" \
  -H "Content-Type: application/json" \
  -d '{
        "action": "accept"
      }'
Response (200 OK):

json
Copy code
{
    "status": "Friend request accepted."
}
To Reject the Friend Request:

Change the action to "reject".

6. List Friends
Endpoint: GET /friends/

Description: Retrieve a list of friends.

Headers:

http
Copy code
Authorization: Token your_auth_token_here
Request:

bash
Copy code
curl -X GET http://localhost:8000/friends/ \
  -H "Authorization: Token your_auth_token_here"
Response (200 OK):

json
Copy code
[
    {
        "id": 2,
        "username": "janedoe",
        "email": "jane.doe@example.com",
        "first_name": "",
        "last_name": ""
    }
]
7. List Pending Friend Requests
Endpoint: GET /friend-requests/

Description: List incoming friend requests that are pending.

Headers:

http
Copy code
Authorization: Token your_auth_token_here
Request:

bash
Copy code
curl -X GET http://localhost:8000/friend-requests/ \
  -H "Authorization: Token your_auth_token_here"
Response (200 OK):

json
Copy code
[
    {
        "id": 3,
        "from_user": {
            "id": 3,
            "username": "bobsmith",
            "email": "bob.smith@example.com",
            "first_name": "",
            "last_name": ""
        },
        "to_user": {
            "id": 1,
            "username": "johndoe",
            "email": "john.doe@example.com",
            "first_name": "",
            "last_name": ""
        },
        "status": "pending",
        "timestamp": "2023-10-01T12:34:56Z"
    }
]
8. Throttling Friend Requests
Description: Users cannot send more than 3 friend requests within a minute.

Test Case:

Action: Attempt to send 4 friend requests within one minute.
Expected Outcome: The fourth request should be throttled.
Example:

bash
Copy code
# Send first friend request
curl -X POST http://localhost:8000/send-friend-request/2/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send second friend request
curl -X POST http://localhost:8000/send-friend-request/3/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send third friend request
curl -X POST http://localhost:8000/send-friend-request/4/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"

# Send fourth friend request (should be throttled)
curl -X POST http://localhost:8000/send-friend-request/5/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"
Fourth Request Response (429 Too Many Requests):

json
Copy code
{
    "detail": "Request was throttled. Expected available in 60 seconds."
}
9. Pagination in Search
Description: The search results are paginated with 10 records per page.

Request:

bash
Copy code
curl -X GET "http://localhost:8000/search/?q=j&page=2" \
  -H "Authorization: Token your_auth_token_here"
Response:

json
Copy code
{
    "count": 25,
    "next": "http://localhost:8000/search/?q=j&page=3",
    "previous": "http://localhost:8000/search/?q=j&page=1",
    "results": [
        // List of users 11-20 matching the search query
    ]
}
10. Error Handling Examples
Invalid Credentials on Login:

bash
Copy code
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "password": "wrongpassword"
      }'
Response (400 Bad Request):

json
Copy code
{
    "error": "Invalid Credentials"
}
Sending Friend Request to Non-existent User:

bash
Copy code
curl -X POST http://localhost:8000/send-friend-request/9999/ \
  -H "Authorization: Token your_auth_token_here" \
  -H "Content-Type: application/json"
Response (404 Not Found):

json
Copy code
{
    "detail": "Not found."
}
Attempting to Send Duplicate Friend Request:

If you try to send a friend request to a user you've already sent a request to:

Response (400 Bad Request):

json
Copy code
{
    "error": "Friend request already sent."
}
11. Authentication
Description: All API endpoints (except signup and login) require authentication.

Headers:

Include the Authorization header in the format:

http
Copy code
Authorization: Token your_auth_token_here
Example:

bash
Copy code
curl -X GET http://localhost:8000/friends/ \
  -H "Authorization: Token your_auth_token_here"
Unauthorized Request Example:

If you omit the Authorization header:

Response (401 Unauthorized):

json
Copy code
{
    "detail": "Authentication credentials were not provided."
}
12. Using Postman
If you prefer to use Postman, here's how you can set up requests:

Set the Base URL: http://localhost:8000/
Headers:
For authenticated requests, add a header Authorization with value Token your_auth_token_here.
For JSON data, set Content-Type to application/json.
Body:
Use the raw option and select JSON for the body content.
Method:
Choose the appropriate HTTP method: GET, POST, etc.
13. Additional Notes
Creating Multiple Users for Testing: To fully test the friend request functionality, create multiple user accounts using the signup endpoint.
Retrieving Friend Request IDs: When you send or receive friend requests, the API may not return the request ID directly. Use the pending friend requests endpoint to list them and retrieve their IDs for accepting or rejecting.
Date and Time Format: The timestamp in friend requests is in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).

14. Testing Summary
Signup and Login: Create accounts and obtain tokens.
Authentication: Use the token in the Authorization header for subsequent requests.
Search Users: Test searching by email and name fragments.
Friend Requests: Send, accept, and reject friend requests.
Friend List: Verify that friends appear in the friends list after accepting requests.
Pending Requests: Check that incoming friend requests appear in the pending list.
Throttling: Test rate limiting by attempting to send multiple friend requests quickly.
Pagination: Verify that search results are correctly paginated.



To run the test on the test scripts:
python manage.py test social_media_app.tests