# Postgres Tables

## Users

Stores each app user.

This table is used in authentication views, as well as the bill updates notification system.

### Has Connections From:

* Favorites

| Name     | Type                       | Description          |
| -------- | -------------------------- | -------------------- |
| id       | PrimaryKey, bigint, unique | Internal user id     |
| password | Varchar                    | Hashed user password |
| email    | Varchar                    | User email address   |
| username | Varchar                    | User's username      |
| phone    | Varchar                    | User's phone number  |

## Actions

Stores each distinct action taken on a bill, e.g., ("First Reading"). Represented by a one-to-many relationship between bill and actions.

This table is queried by frontend views that show bill information, such as most recent action. Additionally, it will be queried by the notification system, which updates users about favorited bills that have had a significant action associated with them in the past 24 hours.

### Connects to:

* Bills (on bill_id ForeignKey)

| Name        | Type                        | Description                                                  |
| ----------- | --------------------------- | ------------------------------------------------------------ |
| action_id   | Varchar, PrimaryKey, unique | Id of the action                                             |
| description | Varchar                     | Description of action, e.g. (“First Reading”)                |
| date        | Timestamp  with time zone   | Date of action                                               |
| category    | varchar, nullable           | Category of action. Used to group actions into broader types for tracking bill status |
| bill_id     | ForeignKey                  | `bill_id` from the bills_table for the bill associated with this action |

## Bills

Stores data for each bill.

This table is queried by frontend views that show bill information, such as the search view, and individual bill pages.

### Has Connections From:

* Actions
* Favorites
* Sponsors
* Topics

| Name    | Type                        | Description                                 |
| ------- | --------------------------- | ------------------------------------------- |
| bill_id | Varchar, PrimaryKey, unique | Id of the bill                              |
| number  | Varchar                     | Bill number used by legislature             |
| title   | Varchar                     | Official title of the bill                  |
| summary | Varchar                     | Bill summary as sourced from OpenStates API |
| status  | Varchar                     | The latest action taken on the bill         |

## Favorites

Stores data for user favorites of bills. Represents a many-to-many relationship: one user can like many bills, one bill can be associated with many users.

This table will be queried by frontend views that show users which bills they have favorited. Additionally, this table will be used for the automatic notification system that notifies users about updates from bills they have favorited.

### Connects to: 

* Bills (on bill_id ForeignKey)
* Users (on user_id ForeignKey)

| Name    | Type                | Description                                                  |
| ------- | ------------------- | ------------------------------------------------------------ |
| id      | Bigint, PrimaryKey  | Internal ID for a favorite                                   |
| bill_id | Varchar, ForeignKey | `bill_id` from the bills_table for the bill favorited        |
| user_id | Varchar, ForeignKey | `user_id` from the users table for the user favoriting the bill |

## Sponsors

Stores data for sponsors of bills. Represents a one-to-many relationship: one bill may have many sponsors.

This table is queried by frontend views that show bill information, including sponsor information.

### Connects to:

* Bills (on bill_id ForeignKey)

| Name         | Type                        | Description                                                  |
| ------------ | --------------------------- | ------------------------------------------------------------ |
| id           | Varchar, PrimaryKey, unique | Internal id of the sponsor. Separate from sponsor_id as sponsor_id comes from OpenStates and may be null |
| sponsor_id   | Varchar                     | sponsor_id from OpenStates                                   |
| sponsor_name | Varchar                     | Name of the bill sponsor                                     |
| bill_id      | Varchar, ForeignKey         | `bill_id` from the bills table, the bill that the sponsor has sponsored |
| position     | Varchar, nullable           | The position: (e.g., Member of the State House, Member of the State Senate) that the sponsor occupies |
| party        | Varchar, nullable           | The political party of the sponsor                           |

## Topics

Stores data for topics associated with each bill. Represents a many-to-many relationship: one bill may have many topics, one topic may have many bills associated with it.

This table is queried by frontend views that show bill information, including topic information.

### Connects to:

* Bills (on bill_id ForeignKey)

| Name    | Type                | Description                                                  |
| ------- | ------------------- | ------------------------------------------------------------ |
| id      | Bigint, PrimaryKey  | ID of the topic                                              |
| topic   | Varchar             | Topic name                                                   |
| bill_id | Varchar, ForeignKey | `bill_id` from the bills table, the bill the topic is associated with |