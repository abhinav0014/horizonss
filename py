@echo off
REM filepath: e:\Abhinav\Coder\horizonss\py.bat

IF "%1"=="" (
    echo Usage: py [command]
    echo Commands:
    echo   r  - Run server with logging
    echo   mm - Make migrations
    echo   m  - Migrate
    echo   c  - Create superuser
    echo   s  - Show migrations
    exit /b 1
)

REM Ensure virtual environment is activated
IF EXIST "venv" (
    IF "%VIRTUAL_ENV%"=="" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    )
)

REM Process commands
IF "%1"=="r" (
    echo Starting development server with logging... >> server.log
    python manage.py runserver >> server.log 2>&1
) ELSE IF "%1"=="mm" (
    echo Making migrations... >> server.log
    python manage.py makemigrations >> server.log 2>&1
) ELSE IF "%1"=="m" (
    echo Applying migrations... >> server.log
    python manage.py migrate >> server.log 2>&1
) ELSE IF "%1"=="c" (
    echo Creating superuser... >> server.log
    python manage.py createsuperuser >> server.log 2>&1
) ELSE IF "%1"=="s" (
    echo Showing migrations status... >> server.log
    python manage.py showmigrations >> server.log 2>&1
) ELSE (
    echo Invalid command: %1
    echo Usage: py [command]
    echo Commands:
    echo   r  - Run server with logging
    echo   mm - Make migrations
    echo   m  - Migrate
    echo   c  - Create superuser
    echo   s  - Show migrations
    exit /b 1
)