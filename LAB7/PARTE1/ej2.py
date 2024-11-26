import cv2
import sys
import matplotlib.pyplot as plt   

def resize_img(img, width, height):
    up_points = (width, height)
    img_resize = cv2.resize(img, up_points)
    image_rgb = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    return image_rgb

def select_size_option():
    print("Selecciona el tamaño de la imagen:")
    print("1. Original")
    print("2. Pequeño (200x200)")
    print("3. Mediano (500x500)")
    print("4. Grande (800x800)")
    print("Presiona 's' para salir")
    
    option = input("Ingresa el número correspondiente: ")
    return option

if __name__ == "__main__":

    img = cv2.imread('/home/leyla/Desktop/FOTOS/ASS.jpg')
    
    if img is None:
        print("Error: No se pudo cargar la imagen")
    else:
        while True:
            
            option = select_size_option()

            if option == 's':  # Verifica si se presionó 's' para salir
                print("Saliendo")
                break

            # Ajustar el tamaño según la opción
            if option == "1":
                rimg = img
            elif option == "2":
                rimg = resize_img(img, 200, 200) 
            elif option == "3":
                rimg = resize_img(img, 500, 500)  
            elif option == "4":
                rimg = resize_img(img, 800, 800)  
            else:
                print("Opción no válida")
                continue  # Reiniciar el ciclo si la opción es inválida

            # Mostrar la imagen reescalada o original
            f, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.imshow(rimg)
            ax.set_title("Imagen reescalada")
            ax.axis('on')
            plt.show()

