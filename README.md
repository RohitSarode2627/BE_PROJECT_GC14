# Crime Prediction System (BE_PROJECT_GC14)
## Crime Prediction & Analytics Platform
A Machine Learning-driven Flask application designed to analyze crime patterns and predict crime occurrences using Random Forest.
### Quickstart
- Run `pip install -r requirements.txt`
- Train model: `python train_model.py`
- Launch web app: `python app.py`

A Machine Learning-powered Web Application for Crime Prediction and Analysis built with **Flask**, **Random Forest Classifier (Scikit-Learn)**, and **MySQL**.

---

## 📌 Project Overview

This project analyzes historical crime data to predict the likelihood and category of potential crimes (Robbery, Gambling, Accident, Violence, Murder, Kidnapping) based on spatial and temporal parameters:
- **Location Geocoding:** Converts address/location inputs into geographic coordinates (Latitude, Longitude) using OpenStreetMap's Nominatim geolocator.
- **Temporal Feature Engineering:** Extracts features such as Month, Day, Hour, Day of Year, Week of Year, etc.
- **Machine Learning Classification:** Utilizes a trained Random Forest Classifier model to predict the expected crime category or indicate if the place is safe at that timestamp.
- **User Authentication & Dashboard:** User registration, login, dashboard for prediction, crime density maps, and contact/feedback forms.

---

## 🛠️ Tech Stack

- **Backend Framework:** Flask, Flask-SQLAlchemy, Flask-Mail
- **Database:** MySQL Server (Database: `crime`, Tables: `register`, `contact`)
- **Database Driver:** PyMySQL & Cryptography
- **Machine Learning & Data Processing:** Scikit-Learn, Pandas, NumPy, Joblib
- **Geocoding:** GeoPy (Nominatim)
- **Frontend:** HTML5, CSS3, Bootstrap, jQuery

---

## 🚀 Setup & Installation Guide

### 1. Prerequisites
- **Python:** 3.11 or higher
- **MySQL Server:** 8.0+ running on port `3306`

### 2. Virtual Environment Setup
A dedicated virtual environment has already been created in `venv/`. To activate it:

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies
All required dependencies are listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Database Setup (MySQL)
1. Ensure your MySQL service (e.g. `MySQL84`) is running.
2. The database `crime` has been created and populated using `crime.sql`:
```powershell
# Create database and import tables
Get-Content crime.sql | & "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root -proot crime
```

### 5. Configuration (`config.json`)
Verify connection settings in `config.json`:
```json
{
    "params": {
        "local_server": "True",
        "local_uri": "mysql+pymysql://root:root@localhost/crime",
        "prod_uri": "mysql+pymysql://root:root@localhost/crime",
        "fb_url": "https://facebook.com/crime",
        "tw_url": "https://twitter.com/crime",
        "git_url": "https://github.com/crime",
        "gmail_user": "techteam@gmail.com",
        "gmail_password": "Google@12345"
    }
}
```
*(Update `root:root` with your MySQL username and password if different.)*

### 6. Machine Learning Model
The Random Forest model is saved at `model/rf_model`. If you ever need to retrain it using `data.csv`:
```bash
python train_model.py
```

### 7. Run the Application
Launch the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🔑 Default Accounts (from database)

You can log in at `/login` with existing accounts:
- **Email:** `Sandy@gmail.com` | **Password:** `123456789`
- **Email:** `sapana@gmail.com` | **Password:** `Sapana@123`
- **Email:** `tejas@gmail.com` | **Password:** `tejas@123`
- Or register a new account at `/register`.

---

## 📂 Project Structure

```
├── app.py                            # Main Flask web application
├── config.json                       # Database and mail configuration
├── crime.sql                         # MySQL database schema and initial data
├── data.csv                          # Historical crime dataset
├── train_model.py                    # Model training script
├── requirements.txt                  # Python dependencies
├── model/
│   └── rf_model                      # Trained Random Forest model (joblib)
├── templates/                        # Jinja2 HTML templates
│   ├── index.html                    # Landing page
│   ├── about.html                    # About page
│   ├── login.html                    # Login page
│   ├── register.html                 # Registration page
│   ├── dashboard.html                # Prediction dashboard
│   ├── result.html                   # Prediction result page
│   ├── map.html                      # Crime map visualization
│   └── contact.html                  # Contact form
├── static/                           # Static assets (CSS, JS, Images, Fonts)
└── venv/                             # Python 3.11 virtual environment
```