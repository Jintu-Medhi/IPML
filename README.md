# Face Recognition Based Attendance System

![Flow Diagram](assets/flow_att_recog.png)

/Face-Recognition-Attendance-System
│
├── Real Time/             # Real Time Attendance System for one individual at a time
  └──  Images/              # Images of indivuals
  └──  Resources/           # Background images and mode screens for the GUI
  └──  AddDataToDatabase.py # Python file for adding data to the Firebase Database
  └──  EncodeFile.p         # Pickle file containing the face encodings
  └──  EncodeGenerator.py   # Python file to generate the facial encodings
  └──  main.py              # Python file to execute the project
  └──  serviceAccountKey.json # JSON file containing Firebase service account credentials
  
├── Group Photo/           # Attendance system from a group picture
  └──  Images/              # Images of indivuals
  └──  AddDataToDatabase.py # Python file for adding data to the Firebase Database
  └──  EncodeFile.p         # Pickle file containing the face encodings
  └──  EncodeGenerator.py   # Python file to generate the facial encodings
  └──  attendance_ui.py     # Python file dealing with the UI for the message after updating the attendance
  └──  group_photo.png      # Group picture used for the attendance system
  └──  main.py              # Python file to execute the project
  └──  serviceAccountKey.json # JSON file containing Firebase service account credentials

├── README.md              # Project documentation

📁 Face-Recognition-Attendance-System
├── 📁 Real Time
│   ├── 📁 Images                # Stored individual face images
│   ├── 📁 Resources             # GUI backgrounds and mode screens
│   ├── 📄 AddDataToDatabase.py  # Add student data into Firebase Database
│   ├── 📄 EncodeFile.p          # Serialized file containing face encodings
│   ├── 📄 EncodeGenerator.py    # Script to generate facial encodings
│   ├── 📄 main.py               # Main file to run real-time attendance system
│   └── 📄 serviceAccountKey.json # Firebase service account credentials
├── 📁 Group Photo
│   ├── 📁 Images                # Stored individual face images
│   ├── 📄 AddDataToDatabase.py  # Add student data into Firebase Database
│   ├── 📄 EncodeFile.p          # Serialized file containing face encodings
│   ├── 📄 EncodeGenerator.py    # Script to generate facial encodings
│   ├── 📄 attendance_ui.py      # UI after attendance update
│   ├── 📄 group_photo.png       # Sample group photo for testing
│   ├── 📄 main.py               # Main file to run group-photo attendance system
│   └── 📄 serviceAccountKey.json # Firebase service account credentials
└── 📄 README.md                 # Project documentation

