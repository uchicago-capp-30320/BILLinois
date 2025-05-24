# Updating Django Models and Database Schema

BILLinois uses Django's built in migration system to make updates to the database schema.

In order to update the database schema:

Go to `apps/core/models.py`, and create or edit the appropriate model. Each _class_ is a table, while each variable declared within that class is a field. Read the [Django documentation](https://docs.djangoproject.com/en/5.2/topics/db/models/) on models for more information.

1. **Edit The Models File**

```python
class actions_mock_django(models.Model):
    """
    A mock model for the actions table.
    Meant to store mock data for actions taken on legislation.
    """
    bill_id = models.ForeignKey("bills_mock_django", on_delete=models.CASCADE)
    action_id = models.CharField(unique=True, primary_key=True)
    description = models.CharField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'actions_mock_django'
```

2. **Generate a Migration**

Use the `makemigrations` command to generate a migration file. This will make a new migration file in the `apps/core/migrations` directory.

`uv run python manage.py makemigrations core`

3. **Apply the Migration**

This step actually updates the database with the migration.

`uv run python manage.py migrate`

4.  **Confirm the Migration Worked**

You can use your favorite database IDE to check that the migration worked, or you can use the command line by typing:

`uv run python manage.py dbshell`

Then:

`\dt` to list the tables

5. **Commit Your Migration Files**

The migration file created by this process should be committed to GitHub! These files work like a running ledger for how the database has changed over time. Without these files, other users won't be able to apply or build upon database changes.

## Other Notes

You can name a migration, for example:

`uv run python manage.py makemigrations core --name add_status_field`
