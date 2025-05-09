import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-1.firebasestorage.app"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

modeType = 0
counter = 0
student_id = -1  # Renamed from 'id' to avoid shadowing built-in
imgStudent = []
studentInfo = None

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                student_id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{student_id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{student_id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)  # Fixed COLOR_BGRA2BGR
                # Update data of attendance
                if studentInfo and 'last_attendance_time' in studentInfo:
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                      "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{student_id}')
                        if 'total_attendance' in studentInfo:
                            studentInfo['total_attendance'] += 1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        modeType = 2  # Set to student info mode
                        counter = 2  # Start counting for student info display
                    else:
                        modeType = 3  # Already marked
                        counter = 0

            # Display student info for approximately 10 seconds (mode 2)
            if modeType == 2:
                # Update background to show student info mode background
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                # Display student information on the background
                if studentInfo is not None:
                    if 'total_attendance' in studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                   cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    if 'major' in studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                   cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(student_id), (1006, 493),
                               cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    if 'standing' in studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                   cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    if 'year' in studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                   cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    if 'starting_year' in studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                   cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    if 'name' in studentInfo:
                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                   cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                # Keep in student info mode for approximately 5 seconds (200 frames at 30fps)
                if counter >= 400:  # ~5 seconds at 30fps
                    counter = 0
                    modeType = 0
                    studentInfo = None
                    imgStudent = []
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)