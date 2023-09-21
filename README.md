# Part 1 - Satellite Monitoring

The **satellite_monitoring** folder contains a Python script that implements a Satellite Monitoring System along with a test file for the health endpoint. The system collects real-time satellite data from an external API, calculates statistics and health status, and serves the information through two API endpoints using Flask.


## Setup Instructions

1. Navigate to the project folder
```
cd satellite_monitoring
```

2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
3. Install required packages by running the following command
```
pip install flask requests
```

4. In your terminal, run the application
```
python app.py
```

The terminal output will inform you where the app is being run, e.g.
```
 * Running on http://127.0.0.1:5000
```

5. In your browser, navigate to the link obtained from step 2, and access the 2 API endpoints.
```
http://127.0.0.1:5000/stats
http://127.0.0.1:5000/health
```

6. To run tests for the health endpoint, stop the application and run the following command in the terminal.
```
python -m unittest -v test_health
```


# Part 2 - Privacy Guard

The **privacy_guard** folder contains a Django project that includes an app for a user management system. The system fulfills the following requirements:

- Basic user authentication & authorization
- SSO (Google OAuth)
- Encryption and decryption of PII (SSN)
- Downloading user data
- Removing user data



## Setup Instructions
1. Navigate to the project folder
```
cd privacy_guard
```

2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the following commands
```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser to be able to access the admin dashboard and follow the prompts
```
python manage.py createsuperuser
```

6. Run the application
```
python manage.py runserver
```

7. Based on the following terminal output, navigate to the link in your browser.
```
Starting development server at http://127.0.0.1:8000/
```


