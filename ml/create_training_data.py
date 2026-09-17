import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "training_data.csv"
output_file = BASE_DIR / "data" / "training_data.csv"

df = pd.read_csv(input_file)

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

interest_map = {
    "B.Tech Computer Science": [
        "Programming", "Technology", "AI", "Problem Solving"
    ],
    "B.Tech Artificial Intelligence and Machine Learning": [
        "AI", "Programming", "Mathematics", "Technology"
    ],
    "B.Tech Information Science": [
        "Programming", "Technology", "Problem Solving"
    ],
    "BCA": [
        "Programming", "Technology", "Web Development"
    ],
    "B.Tech Electronics and Communication": [
        "Electronics", "Technology", "Robotics"
    ],
    "B.Tech Mechanical Engineering": [
        "Machines", "Design", "Technology"
    ],
    "B.Tech Civil Engineering": [
        "Construction", "Design", "Engineering"
    ],
    "B.Tech Biotechnology": [
        "Biology", "Research", "Laboratory"
    ],
    "B.Sc Mathematics": [
        "Mathematics", "Research", "Teaching"
    ],
    "B.Sc Physics": [
        "Physics", "Research", "Technology"
    ],
    "B.Sc Chemistry": [
        "Chemistry", "Research", "Laboratory"
    ],
    "B.Sc Biotechnology": [
        "Biology", "Healthcare", "Research"
    ],
    "B.Sc Nursing": [
        "Healthcare", "Biology", "Medical"
    ],
    "B.Pharm": [
        "Medicine", "Healthcare", "Chemistry"
    ],
    "MBBS": [
        "Medicine", "Healthcare", "Biology"
    ],
    "BDS": [
        "Medicine", "Healthcare", "Biology"
    ],
    "B.Com": [
        "Accounting", "Business", "Finance"
    ],
    "B.Com Computer Applications": [
        "Accounting", "Programming", "Business"
    ],
    "BBA": [
        "Business", "Management", "Marketing"
    ],
    "BA Economics": [
        "Economics", "Business", "Research"
    ],
    "BA English": [
        "Writing", "Literature", "Communication"
    ],
    "BA Fine Arts": [
        "Drawing", "Design", "Creativity"
    ],
    "BA History": [
        "History", "Research", "Teaching"
    ],
    "BA Journalism and Mass Communication": [
        "Writing", "Media", "Communication"
    ],
    "BA Political Science": [
        "Politics", "Research", "Public Service"
    ],
    "BA Psychology": [
        "Psychology", "Healthcare", "Research"
    ],
    "BA Sociology": [
        "Society", "Research", "Social Service"
    ],
    "Bachelor of Social Work": [
        "Social Service", "Society", "Community"
    ]
}

rng = np.random.default_rng(42)

expanded_rows = []

for _, original_row in df.iterrows():

    course_name = original_row["recommended_course"]

    if course_name in interest_map:
        interests = interest_map[course_name]
    else:
        interests = [original_row["interest"]]

    # Create 20 variations for each original course
    for _ in range(20):

        row = original_row.copy()

        # Slightly vary marks to create realistic training examples
        for column in mark_columns:
            mark = float(row[column])

            if mark > 0:
                variation = rng.normal(0, 7)
                new_mark = round(np.clip(mark + variation, 35, 100))
                row[column] = int(new_mark)

        # Randomly select a related interest
        row["interest"] = rng.choice(interests)

        expanded_rows.append(row)

expanded_df = pd.DataFrame(expanded_rows)

expanded_df.to_csv(output_file, index=False)

print("Training dataset expanded successfully")
print("New dataset shape:", expanded_df.shape)
print("Number of courses:", expanded_df["recommended_course"].nunique())
print("Samples per course:")
print(expanded_df["recommended_course"].value_counts())
print("Saved to:", output_file)