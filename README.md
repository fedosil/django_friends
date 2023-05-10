# Django Friends

## Running with Docker Compose

All actions should be executed from the source directory of the project.

Start docker:
   ```bash
   docker compose build
   docker compose up
   ```

API Documentation http://localhost:8000/docs/

Endpoints summary:

1. GET api/followers, api/friends, api/requests - list of followers, friends and requests accordingly
2. POST api/friends - friend request or add a follower as a friend
3. DELETE api/friends - remove from friends and requests, or reject the follower
4. GET api/users - list of users or get the user status in relation to you
5. POST auth/users - create users
6. POST auth/token/login - get authentication token