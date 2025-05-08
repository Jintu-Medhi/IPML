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
│   ├── 📁 Images
│   ├── 📁 Resources
│   ├── 📄 AddDataToDatabase.py
│   ├── 📄 EncodeFile.p
│   ├── 📄 EncodeGenerator.py
│   ├── 📄 main.py
│   └── 📄 serviceAccountKey.json
├── 📁 Group Photo
│   ├── 📁 Images
│   ├── 📄 AddDataToDatabase.py
│   ├── 📄 EncodeFile.p
│   ├── 📄 EncodeGenerator.py
│   ├── 📄 attendance_ui.py
│   ├── 📄 group_photo.png
│   ├── 📄 main.py
│   └── 📄 serviceAccountKey.json
└── 📄 README.md
