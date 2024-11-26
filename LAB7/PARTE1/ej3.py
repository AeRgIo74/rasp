import cv2
# import matplotlib.pyplot as plt

def resize_img(img, width, height):
    up_points = (width, height)
    img_resize = cv2.resize(img, up_points)
    return img_resize

def rotate_image(image):
    #  sentido horario
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

if __name__ == "__main__":
    img = cv2.imread('/home/leyla/Desktop/FOTOS/ASS.jpg')
    
    if img is None:
        print("Error: No se pudo cargar la imagen.")
    else:

        rimg = resize_img(img, 400, 400)
        cv2.imshow("RESIZE IMAGE", rimg)

        while True:
            key = cv2.waitKey(1)
            if key == 27:  #  "ESC"
                break
            elif key == ord('r'):  # rote
                rimg = rotate_image(rimg)
                cv2.imshow("RESIZE IMAGE", rimg)  

        cv2.destroyAllWindows()  # Cerrar todas las ventanas
