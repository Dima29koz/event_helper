user\_account endpoints
=======================

.. toctree::
   :maxdepth: 2


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
          "msg": "login successful"
      }

   :statuscode 200: no error
   :statuscode 401: Wrong username or password


Refresh token
-------------
.. http:post:: /user_account/refresh

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

      {
         "msg": "access token refreshed"
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired


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


Locations
---------
All user`s locations
^^^^^^^^^^^^^^^^^^^^
.. http:get:: /user_account/locations

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

    [
        {
            "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
            "description": "ехать от станции удобнее всего на верблюдах",
            "geo": "55.104086, 36.998032",
            "id": 1,
            "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
            "name": "Гадюкино"
        },
        {
            "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
            "description": null,
            "geo": "55.104086, 36.998032",
            "id": 2,
            "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
            "name": "Гадюкино2"
        }
    ]


   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired


Create location
^^^^^^^^^^^^^^^
.. http:get:: /user_account/create_location

   [requires auth cookies or headers]

   **Example request:**

    .. sourcecode:: json

       {
           "name": "Гадюкино",
           "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
           "geo": "55.104086, 36.998032",
           "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
           "description": "ехать от станции удобнее всего на верблюдах"
       }

   **Example response:**

   .. sourcecode:: json

      {
          "data": {
              "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
              "description": "ехать от станции удобнее всего на верблюдах",
              "geo": "55.104086, 36.998032",
              "id": 1,
              "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
              "name": "Гадюкино"
          },
          "msg": "Location created."
        }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired


Get location
^^^^^^^^^^^^
.. http:get:: /user_account/location/<int:location_id>

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

      {
          "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
          "description": "ехать от станции удобнее всего на верблюдах",
          "geo": "55.104086, 36.998032",
          "id": 3,
          "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
          "name": "Гадюкино"
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Not allowed


Update location
^^^^^^^^^^^^^^^
.. http:post:: /user_account/location/<int:location_id>

   [requires auth cookies or headers]

   **Example request:**

    .. sourcecode:: json

       {
           "name": "Гадюкино1",
           "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
           "geo": "55.104086, 36.998032",
           "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
           "description": "ехать от станции удобнее всего на верблюдах"
       }

   **Example response:**

   .. sourcecode:: json

      {
         "data": {
             "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
             "description": "ехать от станции удобнее всего на верблюдах",
             "geo": "55.104086, 36.998032",
             "id": 3,
             "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
             "name": "Гадюкино1"
         },
         "msg": "Location updated"
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Not allowed


Delete location
^^^^^^^^^^^^^^^
.. http:delete:: /user_account/location/<int:location_id>

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

      {
          "msg": "Location deleted"
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Not allowed


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