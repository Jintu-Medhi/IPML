import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Debanga Raj Neog",
            "major": "Robotics",
            "starting_year": 2021,
            "total_attendance": 3,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2023,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "654321":
        {
            "name": "Bibek Goswami",
            "major": "CSE",
            "starting_year": 2020,
            "total_attendance": 5,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2025-04-09 00:54:34"
        },
    "410104":
        {
            "name": "Aditya Deshmukh",
            "major": "CSE",
            "starting_year": 2023,
            "total_attendance": 4,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-04-09 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
