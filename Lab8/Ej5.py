import cv2
import os

class ImageContours:
    def __init__(self, image_folder="Captures"):
        self.image_folder = image_folder
        self.image_path = self.get_latest_image_path()
        self.image = None

    def get_latest_image_path(self):
        # Obtener la imagen más reciente en la carpeta
        images = [img for img in os.listdir(self.image_folder) if img.endswith(".jpg")]
        if not images:
            print("No hay imágenes en la carpeta.")
            return None
        images.sort(key=lambda x: os.path.getmtime(os.path.join(self.image_folder, x)), reverse=True)
        return os.path.join(self.image_folder, images[0])

    def load_image(self):
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            if self.image is None:
                print("Error: No se pudo cargar la imagen.")
        else:
            print("Error: No hay imagen disponible para cargar.")

    def process_contours(self):
        if self.image is not None:
            # Convertir a escala de grises y aplicar umbral
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # Encontrar y dibujar contornos
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(self.image, contours, -1, (0, 255, 0), 3)

            # Mostrar imagen con contornos
            cv2.imshow("Contours", self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: No se ha cargado ninguna imagen.")

    def run(self):
        self.load_image()
        self.process_contours()

# Ejecución del programa
contour_detector = ImageContours()
contour_detector.run()