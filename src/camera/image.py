import cv2 as cv
import sys

cv.destroyAllWindows()

def open_camera(id: int, OS_IS_WIN: bool):
    if OS_IS_WIN: # selon si on est sous windows, il faut cv.CAP_V4L2.
        cap = cv.VideoCapture(id, cv.CAP_V4L2)              #Valeur propre à mon pc : id = 2
    else:
        cap = cv.VideoCapture(id)

    cap.set(cv.CAP_PROP_FPS, 10)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Impossible d'ouvrir la caméra.")
        exit()
    return cap

def capture_video(id: int, OS_IS_WIN = False):             #cap est un objet    openCV
    cap = open_camera(id, OS_IS_WIN)
    while True:
        ret , frame = cap.read()
        frame = cv.flip(frame, 1) # flip image
        if not ret:
            print("La frame n'a pas pu être capturée... Fin du programme.")
            break
            
        else:
            ret, buffer = cv.imencode('.jpg',frame)
            frame_bytes = buffer.tobytes()

            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' +
                  frame_bytes + b'\r\n')
    close_camera(cap)
            
def close_camera(cap):
    cap.release()
    cv.destroyAllWindows()

#CONTROLE MOUVEMENT CAMERA
#Liste des controles avec : v4l2-ctl -d /dev/video2 --list-ctrls-menus

