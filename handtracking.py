import cv2
import mediapipe as mp

# initialize the hand tracking module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# capture the video stream from the webcam
cap = cv2.VideoCapture(0)

while True:
    # read a frame from the video stream
    ret, frame = cap.read()

    # convert the image to RGB format
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect hands in the image
    results = hands.process(image)

    # if hands are detected, get the landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # get the landmark coordinates
            landmark_coords = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

            # check if the hand gesture corresponds to the letter "k"
            thumb_tip = landmark_coords[4]
            index_tip = landmark_coords[8]
            pinky_tip = landmark_coords[20]
            if thumb_tip[1] < index_tip[1] < pinky_tip[1]:
                print("Found the character k!")

    # display the image with hand landmarks and bounding boxes
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow("Hand Tracking", image)

    # exit the program when the "q" key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
