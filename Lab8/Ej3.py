import cv2
import os
import numpy as np

class CameraCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo acceder a la cámara.")
            self.cap = None
        self.capture_count = 1  # Unique capture count

    def save_frame(self, frame):
        os.makedirs("Captures", exist_ok=True)
        image_path = f"Captures/image_{self.capture_count}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Frame saved at {image_path}")
        self.capture_count += 1  # Increment capture count for a unique name each time
        return image_path

    def apply_grayscale_and_show_quadrants(self, image_path):
        # Load the last saved image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print("Error: No se pudo cargar la imagen.")
            return
        
        # Get dimensions
        height, width = img.shape[:2]
        half_height, half_width = height // 2, width // 2
        
        # Divide into quadrants
        top_left = img[:half_height, :half_width]
        top_right = img[:half_height, half_width:]
        bottom_left = img[half_height:, :half_width]
        bottom_right = img[half_height:, half_width:]

        # Add a white frame between quadrants
        frame_size = 10
        combined_height = height + frame_size
        combined_width = width + frame_size

        # Create a blank image to hold the quadrants with separation frames
        combined_image = np.ones((combined_height, combined_width), dtype=np.uint8) * 255

        # Place quadrants in the blank image with frames
        combined_image[:half_height, :half_width] = top_left          # Top left
        combined_image[:half_height, half_width + frame_size:] = top_right  # Top right
        combined_image[half_height + frame_size:, :half_width] = bottom_left # Bottom left
        combined_image[half_height + frame_size:, half_width + frame_size:] = bottom_right # Bottom right

        # Show the combined image
        cv2.imshow("Quadrants with Frame", combined_image)
        cv2.waitKey(0)  # Wait until a key is pressed
        cv2.destroyAllWindows()

    def run(self):
        if self.cap is None:
            return

        last_image_path = None
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se pudo leer el cuadro de la cámara.")
                break

            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):  # Quit
                break
            elif key == ord('f'):  # Capture frame
                last_image_path = self.save_frame(frame)  # Save with unique name each time

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

        # Apply grayscale filter and show the last captured image in quadrants if it exists
        if last_image_path:
            self.apply_grayscale_and_show_quadrants(last_image_path)

# Run the program
camera_capture = CameraCapture()
camera_capture.run()