import time
import cv2
import mediapipe as mp

class DriverHandsOffDetector:
    def _init_(self, max_detection_time):
        self.max_detection_time = max_detection_time
        self.hands_off_start_time = None

    def start_detection(self):
        self.hands_off_start_time = time.time()

    def stop_detection(self):
        self.hands_off_start_time = None

    def hands_off_confidence(self):
        if self.hands_off_start_time is not None:
            elapsed_time = time.time() - self.hands_off_start_time
            return 1 - (elapsed_time / self.max_detection_time)
        return 0.0


# Create a DriverHandsOffDetector object
cLGA_MaxHandsOFFDetectionTime_sec = 5  # Maximum detection time in seconds
hands_off_detector = DriverHandsOffDetector(cLGA_MaxHandsOFFDetectionTime_sec)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1)

# Initialize the video capture
webcam = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    _, frame = webcam.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame
    results = mp_hands.process(frame_rgb)

    # Check if any hands are detected
    if results.multi_hand_landmarks:
        # Hands are detected, reset the hands-off detection
        hands_off_detector.stop_detection()
    else:
        # No hands detected, start or continue the hands-off detection
        if not hands_off_detector.hands_off_confidence():
            hands_off_detector.start_detection()

    # Get the hands-off plausibility confidence
    confidence = hands_off_detector.hands_off_confidence()

    # Display the confidence on the frame
    text = "Confidence: {:.2f}".format(confidence)
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Render the hand landmarks on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    # Display the frame (you can modify this part based on your application)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:  # Press Esc to exit
        break

# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()