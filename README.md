Flask Polling App API
This repository contains the backend for a simple, yet robust polling application built with Python and Flask. It provides a RESTful API for creating polls, casting votes, and viewing poll results. The application is designed to be lightweight and easy to set up.

Features
Create Polls: Dynamically create new polls by providing a question and a set of options.

Vote: Cast votes for specific options within a poll.

View Results: Retrieve the current vote count for any poll.

In-Memory Data: Utilizes an in-memory data store for simplicity and speed (Note: data will reset on server restart).

Technologies Used
Backend: Python

Framework: Flask

Dependencies: None, apart from Flask itself.

Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Make sure you have Python 3 and pip installed on your system.

Installation & Running
Clone the repository:

git clone https://github.com/your_username/your_repository_name.git

Navigate to the project directory:

cd your_repository_name

Install Flask:

pip install Flask

Run the application:

python main.py

The server will start on http://127.0.0.1:5000.

API Endpoints
The following are the available endpoints to interact with the API.

1. Create a New Poll
URL: /poll

Method: POST

Body (raw JSON):

{
    "question": "What's your favorite season?",
    "options": ["Spring", "Summer", "Autumn", "Winter"]
}

Success Response (201 CREATED):

{
    "message": "Poll created successfully!",
    "poll_id": "a-unique-poll-id",
    "poll_data": {
        "question": "What's your favorite season?",
        "options": {
            "0": "Spring",
            "1": "Summer",
            "2": "Autumn",
            "3": "Winter"
        },
        "votes": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0
        }
    }
}

2. Cast a Vote
URL: /poll/<poll_id>/vote/<option_id>

Method: POST

Example URL: /poll/a-unique-poll-id/vote/2

Success Response (200 OK):

{
    "message": "Vote cast successfully!",
    "poll_id": "a-unique-poll-id",
    "voted_for_option": "2"
}

3. Get Poll Results
URL: /poll/<poll_id>

Method: GET

Example URL: /poll/a-unique-poll-id

Success Response (200 OK):

{
    "poll_id": "a-unique-poll-id",
    "poll_results": {
        "question": "What's your favorite season?",
        "results": [
            { "option": "Spring", "votes": 0 },
            { "option": "Summer", "votes": 0 },
            { "option": "Autumn", "votes": 1 },
            { "option": "Winter", "votes": 0 }
        ]
    }
}
