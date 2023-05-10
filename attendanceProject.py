import cv2
import numpy as np
import face_recognition
import os
import sys
import subprocess
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import ImageGrab
detected_codes = []
students = {
    '19EPCI021' : 'NITTIN',
    '19EPCI015' : 'KARTHIKEYAN R',
    '19EPCI028' : 'NAREN',
    '19EPCI020' : 'NITHIN',
    '19EPCI029' : 'SUDHARSHAN',
    '19EPCI031' : 'THAARUN'
}

path = 'ImagesAttendance'
images = []
classNames = []
reslist = []
res = "No"
idname = "a"
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name,idname):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList and idname==name :
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{res}')

def run_another_file():
    try:
        subprocess.call(["/usr/bin/python3", "smtp.py"])
    except Exception as e:
        print(e)
        print("Error: file not found")

cv2.namedWindow('Attendance')

def button_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Button clicked!')
        run_another_file()
        cv2.rectangle(img, (x - 50, y - 10), (x + 50, y + 10), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "RUN", (x - 20, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

cv2.setMouseCallback('Attendance', button_callback)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    codes = decode(img)

    # Iterate over all detected codes
    for code in codes:
        # Extract the data from the code
        x, y, w, h = code.rect
        data = code.data.decode("utf-8")
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Check if the code has already been detected
        if data not in detected_codes:
            # Process the code
            res = data
            reslist.append(res)
            # Add the code to the list of detected codes
            detected_codes.append(data)
            idname = students.get(res)
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(250,250,250),2)
            markAttendance(name,idname)
        else:
            name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 250, 250), 2)
    cv2.imshow('Attendance',img)
    cv2.waitKey(1)
