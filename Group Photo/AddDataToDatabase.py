import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "234101004":
        {
            "name": "Aditya Deshmukh",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 3,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "234101006":
        {
            "name": "Akshay Sitaram Bhosale",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "234101041":
        {
            "name": "Rahul Bhanudas Agarkar",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 4,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "234101049":
        {
            "name": "Shardul Nalode",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 3,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "234101055":
        {
            "name": "Vikas Kumar Khurendra",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 1,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)
