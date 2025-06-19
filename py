#!/bin/bash

# Check if parameter is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./py [command]"
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

# Function to cleanup on exit
cleanup() {
    echo "Stopping server..."
    if [ -f "server.pid" ]; then
        kill $(cat server.pid) 2>/dev/null
        rm server.pid
    fi
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Ensure virtual environment is activated
if [ -d "venv" ] && [ -z "${VIRTUAL_ENV}" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Process commands
case $1 in
    "r")
        echo "Starting development server with logging..." | tee -a server.log
        python manage.py runserver 2>&1 | tee -a server.log
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
        echo "Usage: ./py [command]"
        echo "Commands:"
        echo "  r  - Run server with logging"
        echo "  mm - Make migrations"
        echo "  m  - Migrate"
        echo "  c  - Create superuser"
        echo "  s  - Show migrations"
        exit 1
        ;;
esac