import cv2
import mediapipe as mp

camara = cv2.VideoCapture(0)
mpFace = mp.solutions.mediapipe.python.solutions.face_detection
detectorCara = mpFace.FaceDetection(0.7)
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
while camara.isOpened():
    exito, img = camara.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Pasamos la imagen a RGB
    resultados = detectorCara.process(imgRGB) # Procesamos la imagen en RGB
    if resultados.detections:
        for id, detections in enumerate(resultados.detections): # Se recorre las caras detectadas
            bboxC = detections.location_data.relative_bounding_box # Se obtiene los datos de x, y, altura y anchura de la cara detectada
            altura, anchura, _ = img.shape # Se obtiene también la altura y anchura de la imagen para ahora pasar a píxeles los datos anteriores (ya que están de 0 a 1)
            bbox = int(bboxC.xmin * anchura), int(bboxC.ymin * altura), int(bboxC.width * anchura), int(bboxC.height * altura) # Se pasan a píxeles y lo guardamos en una variable
            cv2.rectangle(img, bbox, (0,255,0), 2) # Se pinta el rectángulo en la cara detectada
            cv2.putText(img, f"{int(detections.score[0]*100)}%",(bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2) # Se escribe el porcentaje de detección de la cara
            
    cv2.imshow("WebCam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
camara.release()