
# import cv2

# def resize_img(img, width, height):
#     up_points = (width, height) 
#     img_resize = cv2.resize(img, up_points) 
#     return img_resize

# if __name__ == "__main__":
#     img = cv2.imread('/home/leyla/Desktop/FOTOS/my_photo.jpg') 
#     rimg = resize_img(img, 1000, 1000) 


#     cv2.imshow("resize image", rimg) 
#     cv2.waitKey(0)
    
    
import cv2
import numpy as np
import matplotlib.pyplot as plt   

def resize_img(img, width, height):
    up_points = (width, height) 
    img_resize = cv2.resize(img, up_points) 
    return img_resize

if __name__ == "__main__":

    img = cv2.imread('/home/leyla/Desktop/FOTOS/ASS.jpg') 
    rimg = resize_img(img,200, 200) 
    image_rgb = cv2.cvtColor(rimg, cv2.COLOR_BGR2RGB)

    #f, ax = plt.subplots(1, 1, figsize=(10, 10))
    # # Imagen RGB original
    # ax.imshow(rimg)
    # ax.set_title("Original")
    # ax.axis('on')
    # plt.show()

    f, axarr = plt.subplots(1, 3, figsize=(10, 6))
    axarr[0].imshow(img)
    axarr[0].set_title('Imagen Original')
    axarr[0].axis('on')

    axarr[1].imshow(rimg)
    axarr[1].set_title('Imagen Resize')
    axarr[1].axis('on')
    
    axarr[2].imshow(image_rgb)
    axarr[2].set_title('Imagen Resize RGB')
    axarr[2].axis('on')

    plt.show()
    
    
    
    
