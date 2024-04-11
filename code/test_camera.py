import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera capture failed")
        break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        img_name = input('Entrez le nom de votre device à ajouter : ')
        cv2.imwrite(f'{img_name}.png',gray)
        break
        
    if cv2.waitKey(1) & 0xFF == 27:
        break
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
