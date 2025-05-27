# Postgres Tables

```mermaid
erDiagram
    USERS 1 to zero or more FAVORITES : has
    FAVORITES zero or more optionally to 1 BILLS : marks
    SPONSORS one or more optionally to one or more BILLS : introduces
	BILLS 1 to zero or more ACTIONS : has
	BILLS one or more to one or more TOPICS : has
```

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
