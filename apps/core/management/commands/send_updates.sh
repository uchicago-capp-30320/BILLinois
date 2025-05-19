#!/bin/bash

DEBUG=0

if [ "$1" = "debug" ]; then
    DEBUG=1
fi

if [ "$DEBUG" = 1 ]; then
    echo "Running send_updates.sh in debug mode at $(date)"
else
    echo "Running send_updates.sh in production mode at $(date)"
fi

# Only run script with debug command if DEBUG is set to 1
if [ "$DEBUG" = 1 ]; then
    uv run python manage.py populate_notification_queue --DEBUG &&
    uv run python manage.py send_update_notifications --DEBUG &&
    uv run python manage.py remove_received_email
else
    uv run python manage.py populate_notification_queue &&
    uv run python manage.py send_update_notifications &&
    uv run python manage.py remove_received_email
fi
