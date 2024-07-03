# Social Networking API

A Django Rest Framework-based social networking API with user authentication, friend request functionality, and search capabilities.

## Features

- User Signup/Login
- Search users by email and name
- Send/Accept/Reject friend requests
- List friends
- List pending friend requests
- Rate limiting on friend requests (max 3 per minute)

## Requirements

- Python 3.11
- Django 5.0.6
- Django Rest Framework
- SQLite (default database)

## Installation

1. **Clone the repository:**
   
   `git clone https://github.com/kharishgit/AccuKnox.git`
   `cd social_network`


 **DOCKER SETUP - Run this application using Docker**

2. **Build and start the containers**

    `docker-compose up`

3. **Database**
    
    The default database  sqlite(db.sqlite) is also included in the repository along with migrations.You Don't have to run migration commands.It comes with sample data inputs. The superuser name  is `admin@gmail.com` and password is `admin`
    It also contains other users `harish@gmail.com` and password `harish` , `kumari@gmail.com` and   password `kumari` ,`haridass@gmail.com` and password `haridass` etc.
    
    The new users can be created using `/social/signup` The username,email and password is to be given.The email is case insensitive while username is case sensitive.

    You can login with the email and password thorough this `/social/login/`

    All the endpoints other than login and signup are Authenticated.Token Authentication is enabled. In the headeradd Authorization as key and the value  `Token ` followed by the token obtained.





## Postman Collection

    https://elements.getpostman.com/redirect?entityId=22783304-c2acca3c-749f-410c-a11f-4e1854bd16c6&entityType=collection

## API Endpoints

    Signup: /social/signup/ [POST]
    Login: /social/login/ [POST]
    Search Users: /social/search/ [GET] In params (key='query' value="String to search")
    Send Friend Request: /social/friend-request/send/ [POST]
    Accept Friend Request: /social/friend-request/accept/{request_id}/ [POST]
    Reject Friend Request: /social/friend-request/reject/{request_id}/ [POST]
    List Friends: /social/friends/ [GET]
    List Pending Friend Requests: /social/friend-requests/pending/ [GET]


