@echo off
echo Starting the Civic Issue Complaint Portal...
call venv\Scripts\activate.bat
python manage.py runserver
pause
