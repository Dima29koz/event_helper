user\_account endpoints
=======================

.. toctree::
   :maxdepth: 2

.. http:get:: /


.. http:post:: /api/login

   **Example request:**

   .. sourcecode:: json

      {
        "username": "admin",
        "pwd": "1234",
        "remember": true
      }

   **Example response:**

   .. sourcecode:: json

      {
          "data": {
            "token": "user_token"
          },
          "msg": "success",
          "status": "OK"
      }

   :statuscode 200: no error


.. http:post:: /api/registration

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
        "status": "OK",
         "msg": "Check your email...",
      }

      {
        "status": "ERR",
         "msg": "username is not allowed.",
      }

   :statuscode 200: no error


.. http:post:: /api/reset_password_request

   **Example request:**

   .. sourcecode:: json

      {
        "username": "Admin"
      }

   **Example response:**

   .. sourcecode:: json

      {
        "status": "OK",
         "msg": "Check your email...",
      }

      {
        "status": "ERR",
         "msg": "user not found",
      }


   :statuscode 200: no error


.. http:get:: /api/profile_settings

   **Example response:**

   .. sourcecode:: json

      {
        "data": {
            "contacts": null,
            "email": "d******z@yandex.ru",
            "full_name": "Admin A.A.",
            "is_email_verified": false,
            "phone": null,
            "pwd": "********",
            "username": "Admin"
        },
        "msg": "success",
        "status": "OK"
      }

   :statuscode 200: no error


.. http:get:: /api/confirm_email/(str:token)

   **Example response:**

   .. sourcecode:: json

      {
        "status": "OK",
         "msg": "Your email has been confirmed.",
      }

      {
        "status": "ERR",
         "msg": "user not found.",
      }

   :statuscode 200: no error


.. http:post:: /api/reset_password/(str:token)

   **Example request:**

   .. sourcecode:: json

      {
        "new_pwd": "1234"
      }

   **Example response:**

   .. sourcecode:: json

      {
        "msg": "user not found",
        "status": "ERR"
      }

      {
        "status": "OK",
         "msg": "Your password has been reset.",
      }

   :statuscode 200: no error


.. http:get:: /api/logout

   **Example response:**

   .. sourcecode:: json

      {
        "status": "1234",
        "msg": "user logout",
      }

   :statuscode 200: no error