import cv2
import mediapipe as mp
import time
import math
from pycaw.pycaw import AudioUtilities
import numpy as np

camara = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
manos = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

# Inicializamos las variables para calcular los fps
pTime = 0 # tiempo previo
cTime = 0 # tiempo actual (current Time)
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
rango_volumen = volume.GetVolumeRange() # Obtenemos el rango del volumen
volMin = rango_volumen[0] # Guardamos el volumen mínimo
volMax = rango_volumen[1] # Guardamos el volumen máximo
volumenBarra=400
voluemPorcentaje=0
while camara.isOpened():
    exito, img = camara.read()
    altura, anchura, _ = img.shape
    img.flags.writeable = False
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Se convierte la imagen a RGB ya que la clase HandLandmarker utiliza imágenes RGB
    resultados = manos.process(imgRGB)
    img.flags.writeable = True
    if resultados.multi_hand_landmarks:
        for mano in resultados.multi_hand_landmarks: # Con este bucle obtenemos la información de cada mano
            mpDraw.draw_landmarks(img, mano, mpHands.HAND_CONNECTIONS)
            # Obtenemos los puntos del índice y del pulgar para pintaar un círculo en ellos
            indiceY=int(mano.landmark[8].y * altura)
            indiceX=int(mano.landmark[8].x * anchura)
            pulgarX=int(mano.landmark[4].x * anchura)
            pulgarY=int(mano.landmark[4].y * altura)
            # Obtenemos el centro entre ambos para pintar un círculo en medio de la línea (representando el volumen 0)
            cX = (indiceX+pulgarX)//2
            cY = (indiceY+pulgarY)//2
            cv2.circle(img, (indiceX,indiceY), 10, (0,255,255),4)
            cv2.circle(img, (pulgarX,pulgarY), 10, (0,255,255),4)
            # Dibujamos la línea entre el pulgar y el índice
            cv2.line(img, (indiceX,indiceY), (pulgarX, pulgarY), (0,255,255), 4)
            cv2.circle(img, (cX,cY), 10, (0,255,255),cv2.FILLED)
            longitudLinea = math.hypot(indiceX-pulgarX, indiceY-pulgarY) # Calculamos la distnacia entre el pulgar y el índice
            # El método interp nos sirve para hacer una interpolación lineal, es decir, toma un valor de entrada y lo “traduce” a otro rango de valores de forma proporcional
            # Esto lo hacemos para el volumen, el volumen para mostrarlo en la barra y para el porcentaje del volumen
            volumen = np.interp(longitudLinea, [10,180], [volMin, volMax])
            volumenBarra = np.interp(longitudLinea, [10,180], [400, 150])
            voluemPorcentaje = np.interp(longitudLinea, [10,180], [0, 100])
            volume.SetMasterVolumeLevel(volumen, None) # Establecemos el volumen del sistema al volumen calculado
            if longitudLinea<15: # Si la distancia es menor que 15, el círculo que está en medio de la línea se pinta de otro color
                cv2.circle(img, (cX,cY), 10, (0,255,0),cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (255,0,0), 3) # Pintamos el rectángulo que representa la barra del volumen
    cv2.rectangle(img, (50,int(volumenBarra)), (85,400), (255,0,0), cv2.FILLED) # Rellenamos ahora la barra con el volumen correspondiente
    cv2.putText(img, f"{int(voluemPorcentaje)}%", (40,450), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3) # Pintamos el porcentaje del volumen
    cTime = time.time()
    fps = 1/(cTime-pTime) # Calculamos los fps
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
    cv2.imshow("WebCam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

camara.release()