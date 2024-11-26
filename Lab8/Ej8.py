import cv2
import gpiozero
from time import sleep

class MotionAlarm:
    def __init__(self, buzzer_pin=17, threshold=500):
        # Initialize video capture and buzzer
        self.cap = cv2.VideoCapture(0)  # USB camera
        self.buzzer = gpiozero.Buzzer(buzzer_pin)
        self.threshold = threshold  # Threshold for contour area size to detect movement

        # Initialize background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

    def detect_movement(self, frame):
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Remove shadows (optional)
        _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check for large enough contours (indicating movement)
        movement_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > self.threshold:
                movement_detected = True
                break

        return movement_detected

    def run(self):
        print("Press 'q' to exit.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture image.")
                break

            # Detect movement
            if self.detect_movement(frame):
                print("Movement detected! Activating buzzer.")
                self.buzzer.on()
                sleep(0.5)  # Buzzer on duration
                self.buzzer.off()
            else:
                self.buzzer.off()  # Ensure the buzzer is off if no movement

            # Display video for debugging purposes
            cv2.imshow('Frame', frame)
            cv2.imshow('Foreground Mask', self.bg_subtractor.apply(frame))

            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.buzzer.off()

# Instantiate and run the motion alarm system
motion_alarm = MotionAlarm(buzzer_pin=17)
motion_alarm.run()