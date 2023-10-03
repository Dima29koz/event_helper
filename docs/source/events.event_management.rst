event\_management events
========================

.. toctree::
   :maxdepth: 2

connect
-------
**Headers:**

.. sourcecode::

    Event-Key: key


**Emits:**

* message

.. sourcecode::

    'connected'

disconnect
----------

get_data
--------
**Example request:**

.. sourcecode:: json

    {
        // Optional[auth] - user access tokens
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        // possible values: ['event', 'location', 'members']
        "entity": "event"
    }

**Emits:** [to current_user]

* get_event

.. sourcecode:: json

    {
        "title": "event1",
        "description": "description🍰",
        "date_start": "2023-09-02T07:20:35",
        "date_end": "2023-09-04T07:20:35",
        "date_tz": "+0300",
        "cost_reduction_factor": 25
    }

* get_event_location

.. sourcecode:: json

    {
        "name": "Гадюкино",
        "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
        "geo": "55.104086, 36.998032",
        "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
        "description": null
    }

* get_event_members

.. sourcecode:: json

    [
        {
            "user": "Admin",
            "id": 3,
            "nickname": "creator",
            "days_amount": 2,
            "date_from": null,
            "date_to": null,
            "is_drinker": true,
            "is_involved": true,
            "money_impact": 0,
            "role": "organizer"
        }
    ]

update_data
-----------
.. note::
    Requires User to be **event creator** or member with **organizer** role

**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "entity": "event",
        "data": {
            "title": "event1",
            "description": "description🍰",
            "date_start": "2023-09-02T07:20:35.0Z",
            "date_end": "2023-09-04T07:20:35.0Z",
            "date_tz": "+0300",
            "cost_reduction_factor": 25
        }
    }

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "entity": "location",
        "data": {
            "name": "Гадюкино",
            "address": "экологический лагерь Клочково-Гадюкино, сельское поселение Тарутино, Жуковский район, Калужская область",
            "geo": "55.104086, 36.998032",
            "maps_link": "https://yandex.ru/maps/-/CDQ0mW-Y",
            "description": "описание локации"
        }
    }

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "entity": "member",
        "data": {
            "id": 1,
            "nickname": "Skipper",
            "days_amount": 2,
            "date_from": "2023-09-02T07:20:34.0Z",
            "date_to": null,
            "is_drinker": true,
            "is_involved": true,
            "role": "organizer"
        }
    }

**Emits:** [to all connected users]

.. note::
    Response is same to `get_data` response

* update_event
* update_event_location
* update_event_member

delete_event
------------
.. note::
    Requires User to be **event creator**

**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        }
    }

**Emits:** [to all connected users]

* delete_event

add_member
----------
.. note::
    Requires User to be **event creator** or member with **organizer** role

**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "member": {
            "nickname": "creator",
            "days_amount": 2,
            "date_from": null,
            "date_to": null,
            "is_drinker": true,
            "is_involved": true,
            "role": "organizer",
            "user_id": 1
        }
    }

**Emits:** [to all connected users]

* add_member

join_event
----------
**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "member": {
            "nickname": "creator",
            "days_amount": 2,
            "date_from": "2023-09-02T07:20:34.0Z",
            "date_to": null,
            "is_drinker": true
        }
    }

**Emits:** [to all connected users]

* add_member

update_me
---------
**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "member": {
            "nickname": "creator",
            "days_amount": 2,
            "date_from": "2023-09-02T07:20:34.0Z",
            "date_to": null,
            "is_drinker": true
        }
    }

**Emits:** [to all connected users]

* update_event_member

delete_me
---------
**Emits:** [to all connected users]

* delete_member

delete_member
-------------
.. note::
    Requires User to be **event creator** or member with **organizer** role

**Example request:**

.. sourcecode:: json

    {
        "auth": {
            "csrf_access_token": "{{csrf_access_token}}"
        },
        "member_id": 2
    }

**Emits:** [to all connected users]

* delete_member
