import RPi.GPIO as GPIO
import os
import time

# Configuración de los pines GPIO para los sensores
SENSOR1_PIN = 17
SENSOR2_PIN = 18

# Configuración de los pines GPIO para la proyección (salida HDMI)
# Asegúrate de ajustar estos valores según tu configuración
HDMI_PIN = 21

# Configuración de la carpeta con las imágenes
IMAGES_FOLDER = "./images"
IMAGES = ["imagen1.jpg", "imagen2.jpg"]
current_image_index = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SENSOR2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(HDMI_PIN, GPIO.OUT)

def change_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(IMAGES)
    image_path = os.path.join(IMAGES_FOLDER, IMAGES[current_image_index])
    os.system(f"sudo fbi -T 2 -d /dev/fb0 -noverbose {image_path}")

def main():
    setup()
    try:
        while True:
            if GPIO.input(SENSOR1_PIN) == GPIO.LOW:
                change_image()
                time.sleep(0.5)  # Debounce
            if GPIO.input(SENSOR2_PIN) == GPIO.LOW:
                change_image()
                time.sleep(0.5)  # Debounce
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
