# Postgres Tables

```mermaid
erDiagram
    USERS 1 to zero or more FAVORITES : has
    FAVORITES zero or more to 1 BILLS : marks
    SPONSORS one or more to one or more BILLS : introduces
	BILLS 1 to one or more ACTIONS : has
	BILLS zero or more to zero or more TOPICS : has
	UPDATES 1 to 1 BILLS : has
    USER_NOTIFICATION_QUEUE 1 to 1 USERS : has
    MOST_RECENT_UPLOAD
```

Note: Django auto-creates an `id` primary key if one does not already exist in the table.

## Users

::: apps.accounts.models.User

## Actions

::: apps.core.models.ActionsTable

## Bills

::: apps.core.models.BillsTable

## Favorites

::: apps.core.models.FavoritesTable

## Sponsors

::: apps.core.models.SponsorsTable

## Topics

::: apps.core.models.TopicsTable

## Updates

::: apps.core.models.UpdatesTable

## Most Recent Upload

::: apps.core.models.MostRecentUpload

## User Notification Queue
 
::: apps.core.models.UserNotificationQueue
