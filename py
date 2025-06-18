#!/bin/bash

# Check if parameter is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./manage.sh [command]"
    echo "Commands:"
    echo "  r  - Run server with logging"
    echo "  mm - Make migrations"
    echo "  m  - Migrate"
    echo "  c  - Create superuser"
    echo "  s  - Show migrations"
    exit 1
fi

# Function to log command output
log_command() {
    "$@" 2>&1 | tee -a server.log
}

# Process commands
case $1 in
    "r")
        echo "Starting development server with logging..." | tee -a server.log
        log_command python manage.py runserver > server.log 2>&1 &
        echo "Server started with PID $!" | tee -a server.log               
        ;;
    "mm")
        echo "Making migrations..." | tee -a server.log
        log_command python manage.py makemigrations
        ;;
    "m")
        echo "Applying migrations..." | tee -a server.log
        log_command python manage.py migrate
        ;;
    "c")
        echo "Creating superuser..." | tee -a server.log
        log_command python manage.py createsuperuser
        ;;
    "s")
        echo "Showing migrations status..." | tee -a server.log
        log_command python manage.py showmigrations
        ;;
    *)
        echo "Invalid command: $1"
        echo "Usage: ./manage.sh [command]"
        echo "Commands:"
        echo "  r  - Run server with logging"
        echo "  mm - Make migrations"
        echo "  m  - Migrate"
        echo "  c  - Create superuser"
        echo "  s  - Show migrations"
        exit 1
        ;;
esac