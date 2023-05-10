import cv2
import numpy as np
from pyzbar.pyzbar import decode
import openpyxl
cap = cv2.VideoCapture(0)
detected_codes = []
students = {
'19EPCI021' : 'NITTIN',
'19EPCI028' : 'NAREN',
'19EPCI020' : 'NITHIN',
'19EPCI029' : 'SUDHARSHAN',
'19EPCI031' : 'THAARUN',
'19EPCI004' : 'ALLEN',
'19EPCI001' : 'AADHITHYAN',
'19EPCI002' : 'AKHIL',
'19EPCI003' : 'AKHILESH',
'19EPCI005' : 'ANALA',
'19EPCI006' : 'ANANDH',
'19EPCI007' : 'ATHESH',
'19EPCI008' : 'FAIZA',
'19EPCI009' : 'GOKUL',
'19EPCI010' : 'INBA',
'19EPCI011' : 'INDHU',
'19EPCI012' : 'JIHIN',
'19EPCI013' : 'KARTHI.C',
'19EPCI014' : 'KARTHI.M',
'19EPCI015' : 'KARTHI.R',
'19EPCI016' : 'KAVIRAM',
'19EPCI017' : 'KEERTHI',
'19EPCI018' : 'ASHRAF',
'19EPCI019' : 'FARHAN',
}
workbook = openpyxl.Workbook()
worksheet = workbook.active
while True:
    success, img = cap.read()

    if not success:
        break

    # Decode all barcodes in the image
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

            # Add the code to the list of detected codes
            detected_codes.append(data)

    # Draw a rectangle on the image for scanning

            print(students.get(res))
    # Display the image

    cv2.imshow("Barcode Scanner", img)
    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
