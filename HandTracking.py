import cv2
import mediapipe as mp
import time
camara = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
manos = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

# Inicializamos las variables para calcular los fps
pTime = 0 # tiempo previo
cTime = 0 # tiempo actual (current Time)
dedosLevantados = 0

while camara.isOpened():
    exito, img = camara.read()
    altura, anchura, _ = img.shape
    img.flags.writeable = False
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Se convierte la imagen a RGB ya que la clase HandLandmarker utiliza imágenes RGB
    resultados = manos.process(imgRGB)
    img.flags.writeable = True
    dedosLevantados=0
    baseManos = []
    if resultados.multi_hand_landmarks:
        for mano in resultados.multi_hand_landmarks: # Con este bucle obtenemos la información de cada mano
            mpDraw.draw_landmarks(img, mano, mpHands.HAND_CONNECTIONS)
            x = int(mano.landmark[mpHands.HandLandmark.WRIST].x * anchura)
            y = int(mano.landmark[mpHands.HandLandmark.WRIST].y * altura)
            # Guardamos las coordenadas de las bases de las manos para luego tener las coordenadas de las manos y pintar si la mano es la izquierda o derecha
            baseManos.append((x,y))

            # Vamos obteniendo cada parte de la mano
            indiceY=mano.landmark[8].y
            indiceMedio=mano.landmark[6].y
            indiceBase=mano.landmark[5].y
            indiceBaseX=mano.landmark[5].x

            corazonY=mano.landmark[12].y
            corazonMedio=mano.landmark[10].y
            corazonBase=mano.landmark[9].y

            anularY=mano.landmark[16].y
            anularMedio=mano.landmark[14].y
            anularBase=mano.landmark[13].y

            menhiqueY=mano.landmark[20].y
            menhiqueMedio=mano.landmark[18].y
            menhiqueBase=mano.landmark[17].y

            pulgarY=mano.landmark[4].y
            pulgarMedio=mano.landmark[3].y
            pulgarBase=mano.landmark[2].y
            pulgarX=mano.landmark[4].x

            # Luego se comprueba si la parte alta del dedo es menor en cuanto a coordenadas que las partes inferiores del dedo, si es así, quiere decir que ese dedo está levantado
            # Se comprueba si es menor ya que el punto de origen (0,0) es arriba a la izquerda de la cámara, por lo que cuanto más se baje en la cámara, mayor será x e y
            if indiceY<indiceMedio and indiceY<indiceBase:
                dedosLevantados+=1

            if corazonY<corazonMedio and corazonY<corazonBase:
                dedosLevantados+=1 

            if anularY<anularMedio and anularY<anularBase:
                dedosLevantados+=1

            if menhiqueY<menhiqueMedio and menhiqueY<menhiqueBase:
                dedosLevantados+=1

            if abs(pulgarX - indiceBaseX) > 0.1 and pulgarY < pulgarBase:
                dedosLevantados+=1

        labels = []
        # Luego obtenemos el nombre de la mano (Izquierda o derecha)
        for mano in resultados.multi_handedness:
            for clasificacion in mano.classification:
                labels.append(clasificacion.label)

    cTime = time.time()
    fps = 1/(cTime-pTime) # Calculamos los fps
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)
    cv2.putText(img, f"Dedos levantados: {dedosLevantados}", (10,450), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),3)
    contador = 0
    for base in baseManos:
        # Escribirmos el nombre de la mano en las coordenadas guardadas en el array base
        cv2.putText(img, labels[contador], (base[0]-35, base[1]+40), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),3) 
        contador+=1
    cv2.imshow("WebCam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

camara.release()