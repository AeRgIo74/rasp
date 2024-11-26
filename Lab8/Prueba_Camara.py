import cv2

cap = cv2.VideoCapture(0)  # Usa 0 para la cámara principal, cambia a 1 si no la detecta

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo recibir el cuadro (end of stream?). Saliendo ...")
        break

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()