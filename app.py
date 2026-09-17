from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd


# ==================================================
# APP CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

app.config["SECRET_KEY"] = "course-recommendation-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" +
    str(BASE_DIR / "database" / "course_recommendation.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ==================================================
# LOAD MACHINE LEARNING MODEL
# ==================================================

MODEL_PATH = BASE_DIR / "model" / "course_model.pkl"

model = None

if MODEL_PATH.exists():
    try:
        model = joblib.load(MODEL_PATH)
        print("Machine learning model loaded successfully")
    except Exception as error:
        print("Error loading model:", error)
else:
    print("Warning: Model file not found")


# ==================================================
# DATABASE MODELS
# ==================================================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # Student profile fields
    stream = db.Column(
        db.String(50),
        nullable=True
    )

    interests = db.Column(
        db.String(255),
        nullable=True
    )

    career_goal = db.Column(
        db.String(255),
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class RecommendationHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    predicted_course = db.Column(
        db.String(150),
        nullable=False
    )

    stream = db.Column(
        db.String(50),
        nullable=True
    )

    interest = db.Column(
        db.String(150),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "recommendation_history",
            lazy=True
        )
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ==================================================
# COURSE DATASET
# ==================================================

COURSES_PATH = BASE_DIR / "data" / "courses.csv"

if COURSES_PATH.exists():

    courses_df = pd.read_csv(COURSES_PATH)

    # Remove accidental spaces from column names
    courses_df.columns = courses_df.columns.str.strip()

else:

    courses_df = pd.DataFrame()

    print("Warning: courses.csv not found")


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def clean_value(value, default="Not specified"):
    """
    Converts empty or missing values into a readable value.
    """

    if value is None:
        return default

    if pd.isna(value):
        return default

    value = str(value).strip()

    if not value:
        return default

    return value


def get_course_details(course_name):
    """
    Gets complete details for a predicted course.
    """

    if courses_df.empty:
        return {}

    if "course_name" not in courses_df.columns:
        return {}

    matched = courses_df[
        courses_df["course_name"].astype(str).str.strip().str.lower()
        == str(course_name).strip().lower()
    ]

    if matched.empty:
        matched = courses_df[
            courses_df["course_name"].astype(str).str.contains(
                str(course_name),
                case=False,
                na=False
            )
        ]

    if matched.empty:
        return {}

    return matched.iloc[0].to_dict()


def get_alternative_courses(predicted_course, stream=None):
    """
    Returns alternative courses from the dataset.
    """

    if courses_df.empty:
        return []

    if "course_name" not in courses_df.columns:
        return []

    alternatives = courses_df[
        courses_df["course_name"].astype(str).str.lower()
        != str(predicted_course).lower()
    ].copy()

    # Prefer courses matching the student's stream
    if stream and "stream" in alternatives.columns:

        stream_matches = alternatives[
            alternatives["stream"].astype(str).str.lower()
            == str(stream).lower()
        ]

        if not stream_matches.empty:
            alternatives = stream_matches

    return alternatives.head(5).to_dict(
        orient="records"
    )


def get_course_field(course_details, possible_names, default):
    """
    Finds a course field even if the CSV uses slightly different names.
    """

    for column in possible_names:

        if column in course_details:
            return clean_value(
                course_details[column],
                default
            )

    return default


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template(
        "home.html",
        user=current_user
    )


# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            flash("Please fill in all required fields.")

            return redirect(
                url_for("register")
            )

        if password != confirm_password:

            flash("Passwords do not match.")

            return redirect(
                url_for("register")
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already registered.")

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Registration successful. Please login."
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash("Invalid email or password.")

    return render_template("login.html")


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("home")
    )


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    recent_recommendations = RecommendationHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        RecommendationHistory.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        recent_recommendations=recent_recommendations
    )


# ==================================================
# STUDENT PROFILE
# ==================================================

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.name = request.form.get(
            "name",
            current_user.name
        ).strip()

        current_user.phone = request.form.get(
            "phone",
            ""
        ).strip()

        current_user.stream = request.form.get(
            "stream",
            ""
        ).strip()

        current_user.interests = request.form.get(
            "interests",
            ""
        ).strip()

        current_user.career_goal = request.form.get(
            "career_goal",
            ""
        ).strip()

        db.session.commit()

        flash("Profile updated successfully.")

        return redirect(
            url_for("profile")
        )

    return render_template(
        "profile.html",
        user=current_user
    )


# ==================================================
# RECOMMENDATION FORM
# ==================================================

@app.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():

    if request.method == "POST":

        stream = request.form.get(
            "stream",
            ""
        ).strip()

        interest = request.form.get(
            "interest",
            ""
        ).strip()

        mark_columns = [
            "maths",
            "physics",
            "chemistry",
            "biology",
            "computer_science",
            "accountancy",
            "economics",
            "english"
        ]

        input_data = {
            "stream": stream,
            "interest": interest
        }

        for column in mark_columns:

            value = request.form.get(
                column,
                "0"
            )

            try:

                input_data[column] = float(value)

            except (ValueError, TypeError):

                input_data[column] = 0.0

        input_df = pd.DataFrame(
            [input_data]
        )

        if model is None:

            flash(
                "Machine learning model is not available."
            )

            return redirect(
                url_for("recommend")
            )

        try:

            predicted_course = model.predict(
                input_df
            )[0]

            course_details = get_course_details(
                predicted_course
            )

            alternatives = get_alternative_courses(
                predicted_course,
                stream
            )

            # Save recommendation history
            history = RecommendationHistory(
                user_id=current_user.id,
                predicted_course=str(
                    predicted_course
                ),
                stream=stream,
                interest=interest
            )

            db.session.add(history)
            db.session.commit()

            # Extract flexible course information
            eligibility = get_course_field(
                course_details,
                [
                    "eligibility",
                    "Eligibility",
                    "minimum_qualification"
                ],
                "Refer to the institution's admission requirements."
            )

            duration = get_course_field(
                course_details,
                [
                    "duration",
                    "Duration",
                    "course_duration"
                ],
                "Varies by institution."
            )

            career_opportunities = get_course_field(
                course_details,
                [
                    "career_opportunities",
                    "careers",
                    "Career Opportunities",
                    "career"
                ],
                "Software, technology, education, business, or related fields."
            )

            description = get_course_field(
                course_details,
                [
                    "description",
                    "Description",
                    "course_description"
                ],
                "This course may be suitable based on your academic profile and interests."
            )

            skills = get_course_field(
                course_details,
                [
                    "skills",
                    "required_skills",
                    "Skills"
                ],
                "Problem-solving, communication, and subject knowledge."
            )

            return render_template(
                "results.html",
                predicted_course=predicted_course,
                course_details=course_details,
                recommendations=[
                    course_details
                ] if course_details else [],
                alternatives=alternatives,
                eligibility=eligibility,
                duration=duration,
                career_opportunities=career_opportunities,
                description=description,
                skills=skills,
                stream=stream,
                interest=interest
            )

        except Exception as error:

            print(
                "Recommendation error:",
                error
            )

            flash(
                "Unable to generate recommendation. Please check your inputs."
            )

            return redirect(
                url_for("recommend")
            )

    return render_template(
        "recommend.html",
        user=current_user
    )


# ==================================================
# RECOMMENDATION HISTORY
# ==================================================

@app.route("/history")
@login_required
def history():

    recommendations = RecommendationHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        RecommendationHistory.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        recommendations=recommendations
    )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

with app.app_context():

    database_folder = BASE_DIR / "database"

    database_folder.mkdir(
        exist_ok=True
    )

    db.create_all()


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )