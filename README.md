# AI-Based Course Recommendation System After XII

An AI-powered web application that recommends suitable undergraduate courses to students after Class XII based on their academic marks, stream, interests, and career preferences.

## Project Overview

Choosing the right course after Class XII can be challenging. This system uses Machine Learning to analyze student information and recommend a suitable course.

The application provides:

- Student registration and login
- Student dashboard
- Academic details collection
- AI-based course prediction
- Course details and eligibility
- Required skills
- Career opportunities
- Alternative course suggestions
- Recommendation history
- Profile management
- Responsive web interface

## Technologies Used

### Frontend

- HTML5
- CSS3
- Jinja2 Templates

### Backend

- Python
- Flask

### Machine Learning

- Pandas
- Scikit-learn
- Joblib

### Database

- SQLite
- Flask-SQLAlchemy

### Authentication

- Flask-Login
- Werkzeug Password Hashing

## Project Structure

```text
AI_Course_Recommendation_System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── courses.csv
│   └── training_data.csv
│
├── ml/
│   ├── create_training_data.py
│   └── train_model.py
│
├── model/
│   └── course_model.pkl
│
├── templates/
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── recommend.html
│   ├── results.html
│   └── history.html
│
├── static/
│   └── css/
│       └── style.css
│
└── database/
    └── course_recommendation.db
```

## Main Features

### User Registration

Students can create an account using:

- Name
- Email
- Password
- Phone number
- Academic stream
- Interests
- Career goal

### User Login

Registered students can securely log in to access their dashboard and recommendations.

### Student Dashboard

The dashboard provides:

- Student profile information
- Course recommendation access
- Recent recommendations
- Profile management
- Recommendation history

### AI-Based Recommendation

The Machine Learning model uses student information such as:

- Mathematics marks
- Physics marks
- Chemistry marks
- Biology marks
- Computer Science marks
- English marks
- Academic stream
- Student interest

The model predicts a suitable course based on the given information.

### Course Details

The result page displays:

- Recommended course
- Course description
- Eligibility
- Course duration
- Required skills
- Career opportunities
- Alternative courses

### Recommendation History

Students can view their previous course recommendations.

### Profile Management

Students can update their personal and academic information.

## Requirements

Install the following software before running the project:

- Python 3.10 or above
- pip
- Git
- Visual Studio Code

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI_Course_Recommendation_System.git
```

Navigate to the project folder:

```bash
cd AI_Course_Recommendation_System
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

For macOS or Linux:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If the `requirements.txt` file does not exist, create it with the following content:

```text
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
pandas
scikit-learn
joblib
```

Then install the packages:

```bash
pip install -r requirements.txt
```

## Machine Learning Model Training

If the training data needs to be generated, run:

```bash
python ml/create_training_data.py
```

Train the Machine Learning model:

```bash
python ml/train_model.py
```

After successful training, the model will be saved at:

```text
model/course_model.pkl
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open this address in a web browser.

## Accessing from a Mobile Phone

To access the application from another device on the same network, make sure `app.py` contains:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

Find your computer's IP address.

For Windows:

```bash
ipconfig
```

Example:

```text
IPv4 Address: 10.169.77.240
```

Open the following address on your mobile phone:

```text
http://10.169.77.240:5000
```

The mobile phone and computer must be connected to the same Wi-Fi or hotspot network.

## Public Access Using Ngrok

Start the Flask application:

```bash
python app.py
```

Open another terminal and run:

```bash
ngrok http 5000
```

Ngrok will generate a public URL similar to:

```text
https://example.ngrok-free.app
```

This URL can be shared with others to access the application.

Do not share your Ngrok authentication token publicly.

## Application Workflow

```text
Student Opens Website
        │
        ▼
Register or Login
        │
        ▼
Student Dashboard
        │
        ▼
Enter Academic Details
        │
        ▼
Select Stream and Interest
        │
        ▼
Machine Learning Model
        │
        ▼
Course Prediction
        │
        ▼
Display Course Details
        │
        ▼
Save Recommendation History
        │
        ▼
View Previous Recommendations
```

## Example Input

```text
Mathematics: 85
Physics: 80
Chemistry: 78
Biology: 40
Computer Science: 90
English: 88

Stream: Science
Interest: Technology
```

## Example Output

```text
Recommended Course: B.E Computer Science

Duration: 4 Years

Eligibility:
12th with Physics, Chemistry, and Mathematics

Required Skills:
Programming, logical thinking, problem solving

Career Opportunities:
Software Developer, Web Developer,
Data Scientist, AI Engineer,
Full Stack Developer
```

## Dataset

### courses.csv

This file contains course information such as:

- Course name
- Description
- Eligibility
- Duration
- Required skills
- Career opportunities

### training_data.csv

This file contains the training records used by the Machine Learning model.

The training data includes:

- Student marks
- Stream
- Interest
- Recommended course

## Database

The project uses SQLite to store:

- User accounts
- Hashed passwords
- Phone numbers
- Academic stream
- Interests
- Career goals
- Recommendation history
- Recommendation timestamps

The database is automatically created at:

```text
database/course_recommendation.db
```

## Important Database Note

If the database structure is changed during development, stop the Flask server and delete:

```text
database/course_recommendation.db
```

Then restart the application:

```bash
python app.py
```

The database will be created again automatically.

Deleting the database removes existing users and recommendation history.

## Troubleshooting

### ModuleNotFoundError

Install all required dependencies:

```bash
pip install -r requirements.txt
```

### Model File Not Found

Train the model again:

```bash
python ml/train_model.py
```

Make sure the following file exists:

```text
model/course_model.pkl
```

### Flask Application Not Opening

Run:

```bash
python app.py
```

Check that port `5000` is not being used by another application.

### Mobile Cannot Access the Application

Check that:

1. Flask uses `host="0.0.0.0"`.
2. Both devices are connected to the same network.
3. The correct IP address is used.
4. Windows Firewall allows port `5000`.
5. The Flask server is running.

### Database Error

Stop the application, delete the database file, and restart:

```bash
python app.py
```

## Future Enhancements

- College recommendation
- Scholarship recommendation
- Entrance examination-based recommendations
- AI career guidance chatbot
- Course comparison
- College comparison
- Admin dashboard
- Email notifications
- PDF recommendation report
- Student feedback system
- Cloud database integration
- Deployment on Render, Railway, or PythonAnywhere
- Explainable AI recommendations
- Larger real-world dataset

## Limitations

- Recommendation quality depends on the training dataset.
- The system is intended for educational and guidance purposes.
- It should not completely replace professional career counselling.
- Available courses depend on the information stored in `courses.csv`.
- Synthetic training data may not represent every real student.

## Security Notes

For production deployment:

- Use a strong Flask secret key.
- Do not upload passwords or API keys.
- Do not upload the virtual environment.
- Do not upload the SQLite database.
- Use environment variables for sensitive configuration.
- Enable HTTPS when deploying publicly.

## Files Not to Upload

Add the following entries to `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.env
database/*.db
.idea/
.vscode/
```

## Author

**SRUJAN P R**

Bachelor of Engineering  
Computer Science and Engineering

## License

This project is developed for educational and academic purposes.
