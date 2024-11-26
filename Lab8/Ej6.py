import cv2

class VideoContourDetector:
    def __init__(self):
        # Iniciar captura de video
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo acceder a la cámara.")
            self.cap = None

    def process_frame(self, frame):
        # Convertir a escala de grises y aplicar umbral
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos sobre el frame original
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
        return frame

    def run(self):
        if self.cap is None:
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se pudo leer el cuadro de la cámara.")
                break

            # Procesar el frame y mostrarlo
            processed_frame = self.process_frame(frame)
            cv2.imshow("Contours", processed_frame)

            # Salir si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar recursos
        self.cap.release()
        cv2.destroyAllWindows()

# Ejecución del programa
video_contour_detector = VideoContourDetector()
video_contour_detector.run()