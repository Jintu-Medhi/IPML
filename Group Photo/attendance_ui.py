import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import face_recognition
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from PIL import Image, ImageTk
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, db, storage

# ----------------- Firebase Setup ------------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-1.firebasestorage.app"
})
bucket = storage.bucket()

# ----------------- Load Encodings ------------------
with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)

# ----------------- Main Function -------------------
def mark_attendance(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    image_cv = cv2.imread(image_path)

    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    output = []

    for i, (x, y, w, h) in enumerate(faces):
        face_crop = image_cv[y:y + h, x:x + w]
        imgS = cv2.resize(face_crop, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                studentInfo = db.reference(f'Students/{id}').get()
                if studentInfo:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    studentInfo['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(studentInfo['last_attendance_time'])

                    output.append(f"{studentInfo['name']} - ✅ Present (Total: {studentInfo['total_attendance']})")

    if not output:
        messagebox.showinfo("Attendance", "No recognized faces found.")
    else:
        messagebox.showinfo("Attendance Marked", "\n".join(output))

# ----------------- Upload Image Function -------------------
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select Group Photo",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    # Preview image
    img = Image.open(file_path)
    img.thumbnail((400, 300))
    img = ImageTk.PhotoImage(img)
    img_label.configure(image=img)
    img_label.image = img

    mark_attendance(file_path)

# ----------------- GUI -------------------
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("550x500")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Upload Group Photo to Mark Attendance", font=("Arial", 14), bg="#f0f0f0")
title_label.pack(pady=20)

upload_btn = tk.Button(root, text="📷 Upload Image", command=upload_image, font=("Arial", 12), bg="#4caf50", fg="white")
upload_btn.pack(pady=10)

img_label = tk.Label(root, bg="#f0f0f0")
img_label.pack(pady=20)

root.mainloop()