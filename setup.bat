@echo off
echo Setting up the Civic Issue Complaint Portal...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py generate_sample_data
echo Setup Complete!
pause
