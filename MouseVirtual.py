import cv2
import mediapipe as mp
import time
import pyautogui
import math
camara = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
manos = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
pTime = 0
cTime = 0
velocidad_mouse = 10
while camara.isOpened():
    exito, img = camara.read()
    img.flags.writeable = False
    img = cv2.flip(img, 1)
    camera_heigh, camera_width, _ = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Se convierte la imagen a RGB ya que la clase HandLandmarker utiliza imágenes RGB
    resultados = manos.process(imgRGB)
    img.flags.writeable = True
    # Definir el tamaño del rectángulo (ancho, alto)
    rect_width, rect_height = 500, 300
    
    # Calcular las coordenadas del rectángulo centrado
    top_left = ((camera_width - rect_width) // 2, (camera_heigh - rect_height) // 2)
    bottom_right = ((camera_width + rect_width) // 2, (camera_heigh + rect_height) // 2)
    rectangulo_x1 = (camera_width - rect_width) // 2
    rectangulo_x2 = (camera_width + rect_width) // 2
    rectangulo_y1 = (camera_heigh - rect_height) // 2
    rectangulo_y2 = (camera_heigh + rect_height) // 2
    # Centro del rectángulo
    cx = (rectangulo_x1 + rectangulo_x2) // 2
    cy = (rectangulo_y1 + rectangulo_y2) // 2
    primer_cuarto_x=cx-30
    segundo_cuarto_x=cx+30
    primer_cuarto_y = cy-20
    segundo_cuarto_y = cy+20
    lado_cuadrado_pequenho = 60
    cuadro_x1 = cx - lado_cuadrado_pequenho // 2
    cuadro_y1 = cy - lado_cuadrado_pequenho // 2
    cuadro_x2 = cx + lado_cuadrado_pequenho // 2
    cuadro_y2 = cy + lado_cuadrado_pequenho // 2
    # Dibujar el rectángulo en el centro de la imagen
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)  # Verde con grosor 3
    cv2.rectangle(img, (cuadro_x1, cuadro_y1), (cuadro_x2, cuadro_y2), (0, 0, 255), 2)
    if resultados.multi_hand_landmarks:
        for mano in resultados.multi_hand_landmarks: # Con este bucle obtenemos la información de cada mano
            mpDraw.draw_landmarks(img, mano, landmark_drawing_spec=mpDraw.DrawingSpec(color=(255,255,0)))
            landmarks = mano.landmark
            x1 = int(mano.landmark[4].x * camera_width)
            y1 = int(mano.landmark[4].y * camera_heigh)
            x2 = int(mano.landmark[8].x * camera_width)
            y2 = int(mano.landmark[8].y * camera_heigh)
            distancia = math.hypot(x2 - x1, y2 - y1)
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * camera_width)
                y = int(landmark.y * camera_heigh)
                if id==8:
                    cv2.circle(img, (x,y), 10, (0,255,255),4)
                    mov_x = 0
                    mov_y=0
                    if ((x>rectangulo_x1 and x<rectangulo_x2) and (y>rectangulo_y1 and y<rectangulo_y2)) and not((x>cuadro_x1 and x<cuadro_x2) and (y>cuadro_y1 and y<cuadro_y2)):
                        if(x<cx):
                            mov_x=-velocidad_mouse
                        else:
                            mov_x=velocidad_mouse
                        
                        if not(y>primer_cuarto_y and y<segundo_cuarto_y):
                            if y>cy:
                                mov_y=velocidad_mouse
                                if x>primer_cuarto_x and x<segundo_cuarto_x:
                                    mov_x=0
                            else:
                                mov_y=-velocidad_mouse
                                if x>primer_cuarto_x and x<segundo_cuarto_x:
                                    mov_x=0
                        pyautogui.moveRel(mov_x, mov_y)
                if id==4:
                    cv2.circle(img, (x,y), 10, (0,255,255),4)
                    if distancia<30:
                        pyautogui.click()
                        pyautogui.sleep(1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)
    cv2.imshow("WebCam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

camara.release()