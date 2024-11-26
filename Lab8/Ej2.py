import cv2

class CameraFilter:
    def __init__(self):  # Cambiado a __init_
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo acceder a la cámara.")
            self.cap = None

    def apply_filter(self, frame, filter_type):
        if filter_type == 'gray':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif filter_type == 'edge':
            return cv2.Canny(frame, 100, 200)
        elif filter_type == 'blur':
            return cv2.GaussianBlur(frame, (15, 15), 0)
        else:
            return frame

    def run(self):
        if self.cap is None:
            return  # Salir si no se pudo inicializar la cámara

        filter_type = 'none'
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se pudo leer el cuadro de la cámara.")
                break

            filtered_frame = self.apply_filter(frame, filter_type)
            cv2.imshow('Camera', filtered_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('1'):
                filter_type = 'gray'
            elif key == ord('2'):
                filter_type = 'edge'
            elif key == ord('3'):
                filter_type = 'blur'
            elif key == ord('0'):
                filter_type = 'none'

        self.cap.release()
        cv2.destroyAllWindows()

# Ejecutar
camera = CameraFilter()
camera.run()