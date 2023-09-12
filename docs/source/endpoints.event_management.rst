event\_management endpoints
===========================

.. toctree::
   :maxdepth: 2

   events.event_management


Create event
------------
.. http:post:: /event_management/create_event

   [requires auth cookies or headers]

   **Example request:**

   .. sourcecode:: json

      {
          "title": "event1",
          "description": "description🍰",
          "date_start": "2023-09-02T07:20:34.984Z",
          "date_end": "2023-09-04T07:20:34.984Z",
          "timezone": "+0300",
          "cost_reduction_factor": 25,
          "location_id": 1
      }

   **Example response:**

   .. sourcecode:: json

      {
          "key": "event_key",
          "msg": "Event created."
      }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired / Not allowed


All user`s events
-----------------
.. http:get:: /event_management/events

   [requires auth cookies or headers]

   **Example response:**

   .. sourcecode:: json

    {
        "creator_on": [
            {
                "cost_reduction_factor": 25,
                "date_end": "2023-09-04T07:20:35",
                "date_start": "2023-09-02T07:20:35",
                "date_tz": "+0300",
                "description": "description🍰",
                "id": 1,
                "key": "047e960963834069991c304fda7a1073",
                "location": "Гадюкино",
                "title": "event1"
            }
        ],
        "member_on": []
    }

   :statuscode 200: no error
   :statuscode 401: Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")
   :statuscode 403: Token has expired