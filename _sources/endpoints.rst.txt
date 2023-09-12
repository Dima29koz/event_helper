endpoints
=========

.. toctree::
   :maxdepth: 2

   endpoints.user_account
   endpoints.event_management


.. note::

    All endpoints that require authentication accept both token from cookies and headers.

    Using cookies is a preferred way cause they offer some nice benefits compared to the headers approach:

    * tokens from cookies are refreshing if are close to expiring, which simplifies the logic of keeping active users logged in.

    Whenever you are making a request (everything except 'GET'), you need to manually include the X-CSRF-TOKEN header,
    otherwise your requests will be kicked out as invalid too.

Index
-----
.. http:get:: /

Test
----
.. http:get:: /test

   **Example response:**

   .. sourcecode:: json

      {
          "msg": "hello"
      }

   :statuscode 200: no error