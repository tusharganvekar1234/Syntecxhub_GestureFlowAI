
import cv2

for index in range(5):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    if cap.isOpened():
        success, frame = cap.read()

        if success:
            print(f"Camera index {index}: WORKING")
            cv2.imshow(f"Camera {index}", frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        else:
            print(f"Camera index {index}: Opened, but no video")

    cap.release()
