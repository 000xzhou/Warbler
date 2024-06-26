# Warbler

- How is the logged in user being kept track of?
- What is Flask’s **_g_** object?
- What is the purpose of **_add_user_to_g ?_**
- What does **_@app.before_request_** mean?

**Here are some questions your tests should answer for the User model:**

1. Does the repr method work as expected?
2. Does **_is_following_** successfully detect when **_user1_** is following **_user2_**?
3. Does **_is_following_** successfully detect when **_user1_** is not following **_user2_**?
4. Does **_is_followed_by_** successfully detect when **_user1_** is followed by **_user2_**?
5. Does **_is_followed_by_** successfully detect when **_user1_** is not followed by **_user2_**?
6. Does **_User.create_** successfully create a new user given valid credentials?
7. Does **_User.create_** fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
8. Does **_User.authenticate_** successfully return a user when given a valid username and password?
9. Does **_User.authenticate_** fail to return a user when the username is invalid?
10. Does **_User.authenticate_** fail to return a user when the password is invalid?

Try to formulate a similar set of questions for the **Message** model.

For the routing and view function tests, things get a bit more complicated. You should make sure that requests to all the endpoints supported in the **_views_** files return valid responses. Start by testing that the response code is what you expect, then do some light HTML testing to make sure the response is what you expect.

**You should also be testing authentication and authorization. Here are some examples of questions your view function tests should answer regarding these ideas:**

1. When you’re logged in, can you see the follower / following pages for any user?
2. When you’re logged out, are you disallowed from visiting a user’s follower / following pages?
3. When you’re logged in, can you add a message as yourself?
4. When you’re logged in, can you delete a message as yourself?
5. When you’re logged out, are you prohibited from adding messages?
6. When you’re logged out, are you prohibited from deleting messages?
7. When you’re logged in, are you prohibiting from adding a message as another user?
8. When you’re logged in, are you prohibiting from deleting a message as another user?
