# Computer Vision Controls 🖐️🎥

Proyecto personal de **visión por computadora en Python** que utiliza la cámara web para detectar **manos y rostros** y permitir la interacción con el sistema mediante gestos. Incluye un mouse virtual, control de volumen con los dedos y detección facial en tiempo real.

## 🚀 Funcionalidades
- Seguimiento de manos en tiempo real
- Contador de dedos levantados en una o dos manos
- Control del mouse mediante gestos
- Control de volumen usando la distancia entre los dedos
- Detección de rostros con la cámara web

## 🛠️ Tecnologías utilizadas
- Python 3.9
- OpenCV
- MediaPipe

## 📦 Dependencias
Este proyecto requiere **Python 3.9** (ya que mediapipe 0.8.3.1 no funciona en otra versión de python) y las siguientes librerías:

  ```txt
  opencv-python>=4.12.0.88
  mediapipe==0.8.3.1
  numpy>=2.0.0
  pyautogui>=0.9.54
  pycaw
  ```

## 📥 Instalación

1. Clonar el repositorio

   ```bash
   git clone https://github.com/4drian04/computer-vision-controls.git
   cd computer-vision-controls
   ```
2. Crea un entorno virtual (opcional pero recomendado)

  ```bash
  python -m venv venv
  source venv/bin/activate  # En Windows: venv\Scripts\activate
  ```

3. Instala las dependencias

   ```bash
   pip install opencv-python>=4.12.0.88 mediapipe==0.8.3.1 numpy pyautogui pycaw
   ```
Es posible que no se pueda instalar esa versión de mediapipe con pip install, ya que está obsoleto, pero puedes descargar el archivo en esta <a href="https://dashboard.stablebuild.com/pypi-deleted-packages/pkg/mediapipe/0.8.3.1">página</a> y luego hacer un pip install de ese archivo, de esta manera podeis trabajar con esa versión
## ▶️ Uso

Ejecuta el archivo (dentro del directorio donde se encuentren los archivos python) que desees según la funcionalidad

  ```bash
  python HandTracking.py
  python MouseVirtual.py
  python ControladorVolumenDedos.py
  python FaceTracking.py
  ```

Asegúrate de tener una **cámara web o webcam** conectada.

## 🧑‍💻 Autor

Proyecto personal desarrollado por Adrián García García


