import face_recognition
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-1.firebasestorage.app"
})

bucket = storage.bucket()

# Load the EncodeFile
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

# Load the image (group photo)
print("Loading group photo ...")
image = face_recognition.load_image_file("group_photo.png")
print(f"Group photo loaded: {image.shape} (Height x Width x Channels)")

# Detect faces
face_locations = face_recognition.face_locations(image)
print(f"Detected {len(face_locations)} faces in the group photo.")

# Draw rectangles around faces
for top, right, bottom, left in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

# Show the image with rectangles
plt.imshow(image)
plt.axis('off')
plt.title(f'Detected {len(face_locations)} face(s)')
plt.show()

# Convert image to OpenCV format
image = cv2.imread('group_photo.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load OpenCV's pre-trained Haar cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Detect faces using Haar cascade
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.02, minNeighbors=5)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Convert BGR to RGB for displaying with matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize the counter for attendance updates
counter = 0

# Loop through the detected faces to match and update attendance
for i, (x, y, w, h) in enumerate(faces):
    face_crop = image[y:y + h, x:x + w]
    imgS = cv2.resize(face_crop, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        # Compare the encodings with the known ones
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        print(f"Matches: {matches}")  # Debug print

        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(f"Face distances: {faceDis}")  # Debug print

        matchIndex = np.argmin(faceDis)
        print(f"Match index: {matchIndex}")  # Debug print

        if matches[matchIndex]:
            id = studentIds[matchIndex]
            print(f"✅ Match found for ID: {id}")

            # Get the student info from Firebase
            studentInfo = db.reference(f'Students/{id}').get()
            if studentInfo:
                print(f"📋 Student info: {studentInfo}")

                # Update the attendance info in Firebase
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")

                # Update attendance only if it's a new attendance
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                studentInfo['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save updated attendance info
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(studentInfo['last_attendance_time'])

                print(f"📅 Updated attendance for {id}: Total Attendance {studentInfo['total_attendance']}")

                # Reset counter after marking attendance
                counter = 0
            else:
                print(f"⚠️ No student info found for ID: {id}")
