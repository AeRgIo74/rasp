import cv2
import sys
import matplotlib.pyplot as plt

# # Forzar la salida a UTF-8
# sys.stdout.reconfigure(encoding='utf-8')

class ImageProcessor:

    def __init__(self, image_path):

        self.image_path = image_path
        self.image = cv2.imread(image_path)
        
        if self.image is None:
            raise ValueError("Error: No se pudo cargar la imagen")
        
        #  BGR a RGB , matplotlib
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def horizontally(self):
        # Cortar la imagen horizontalmente 
        top_half = self.image_rgb[:self.image_rgb.shape[0] // 2]
        bottom_half = self.image_rgb[self.image_rgb.shape[0] // 2:]
        return top_half, bottom_half

    def vertically(self):
        # Cortar la imagen verticalmente 
        left_half = self.image_rgb[:, :self.image_rgb.shape[1] // 2]
        right_half = self.image_rgb[:, self.image_rgb.shape[1] // 2:]
        return left_half, right_half

    def cut_into_quadrants(self):
        # desempaquetado
        height, width = self.image_rgb.shape[:2]
        quadrants = [
            self.image_rgb[:height // 2, :width // 2],  
            self.image_rgb[:height // 2, width // 2:],  
            self.image_rgb[height // 2:, :width // 2], 
            self.image_rgb[height // 2:, width // 2:], 
        ]
        return quadrants

if __name__ == "__main__":
    try:
        image_path = '/home/leyla/Desktop/FOTOS/ASS.jpg'
        processor = ImageProcessor(image_path)

        # Cortar y obtener imágenes
        top_half, bottom_half = processor.horizontally()
        left_half, right_half = processor.vertically()
        quadrants = processor.cut_into_quadrants()

        # Crear una figura con una cuadrícula 3x3
        f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(5, 5))

        # Mostrar la imagen original
        ax1.set_title('Imagen Original')
        ax1.imshow(processor.image_rgb)
        ax1.axis('on')

        # Mostrar la mitad superior
        ax2.set_title('Mitad Superior')
        ax2.imshow(top_half)
        ax2.axis('on')

        # Mostrar la mitad inferior
        ax3.set_title('Mitad Inferior')
        ax3.imshow(bottom_half)
        ax3.axis('on')

        # Mostrar la mitad izquierda
        ax4.set_title('Mitad Izquierda')
        ax4.imshow(left_half)
        ax4.axis('on')

        # Mostrar la mitad derecha
        ax5.set_title('Mitad Derecha')
        ax5.imshow(right_half)
        ax5.axis('on')

        # Mostrar Cuadrante 1
        ax6.set_title('Cuadrante 1')
        ax6.imshow(quadrants[0])
        ax6.axis('on')

        # Mostrar Cuadrante 2
        ax7.set_title('Cuadrante 2')
        ax7.imshow(quadrants[1])
        ax7.axis('on')

        # Mostrar Cuadrante 3
        ax8.set_title('Cuadrante 3')
        ax8.imshow(quadrants[2])
        ax8.axis('on')

        # Mostrar Cuadrante 4
        ax9.set_title('Cuadrante 4')
        ax9.imshow(quadrants[3])
        ax9.axis('on')

        plt.tight_layout()
        plt.show()

        print("To continue close the window")
        cv2.waitKey(0) # no se usa 
        cv2.destroyAllWindows()

    except ValueError as e:
        print(e)
        
        
        
        
        
