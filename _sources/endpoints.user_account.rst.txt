user\_account endpoints
=======================

.. toctree::
   :maxdepth: 2

Notice
------

All endpoints that require authentication accept both token from cookies and headers.

Using cookies is a preferred way cause they offer some nice benefits compared to the headers approach:
* tokens from cookies are refreshing if are close to expiring, which simplifies the logic of keeping active users logged in.

Whenever you are making a request (everything except 'GET'), you need to manually include the X-CSRF-TOKEN header,
otherwise your requests will be kicked out as invalid too.


Login
-----
.. http:post:: /user_account/login

   Adds auth cookies if login successful

   **Example request:**

   .. sourcecode:: json

      {
        "username": "admin",
        "pwd": "1234",
      }

   **Example response:**

   .. sourcecode:: json

      {
          "msg": "login successful",
          "token": "user_token"
      }

   :statuscode 200: no error
   :statuscode 401: Wrong username or password


Registration
------------
.. http:post:: /user_account/registration

   **Example request:**

   .. sourcecode:: json

      {
        "username": "Admin",
        "full_name": "Admin A.A.",
        "email": "t@t.t",
        "phone": null,
        "contacts": null,
        "pwd": "1234"
      }

   **Example response:**

   .. sourcecode:: json

      {
         "msg": "Check your email...",
      }

   :statuscode 200: no error
   :statuscode 400: username is not allowed


Reset password request
----------------------
.. http:post:: /user_account/reset_password_request

   [requires NO auth cookies or headers]

   **Example request:**

   .. sourcecode:: json

      {
        "username": "Admin"
      }

   **Example response:**

   .. sourcecode:: json

      {
         "msg": "Check your email...",
      }

   :statuscode 200: no error
   :statuscode 400: user not found
   :statuscode 403: user is already authenticated


Profile settings
----------------
.. http:get:: /user_account/profile_settings

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

      {
         "contacts": null,
         "email": "d******z@yandex.ru",
         "full_name": "Admin A.A.",
         "is_email_verified": false,
         "phone": null,
         "pwd": "********",
         "username": "Admin"
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired


Confirm email
-------------
.. http:get:: /user_account/confirm_email/(str:token)

   **Example response:**

   .. sourcecode:: json

      {
         "msg": "Your email has been confirmed.",
      }

   :statuscode 200: no error
   :statuscode 400: Wrong token


Reset password
--------------
.. http:post:: /user_account/reset_password/(str:token)

   [requires NO auth cookies or headers]

   **Example request:**

   .. sourcecode:: json

      {
        "new_pwd": "1234"
      }

   **Example response:**

   .. sourcecode:: json

      {
         "msg": "Your password has been reset.",
      }

   :statuscode 200: no error
   :statuscode 400: Wrong token
   :statuscode 403: user is already authenticated


Logout
------
.. http:get:: /user_account/logout

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

      {
        "msg": "logout successful",
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired