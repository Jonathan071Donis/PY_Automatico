from flask import Flask, render_template, request
import pywhatkit as kit
import pyautogui
import time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numero = request.form['numero']
        mensaje = request.form['mensaje']
        numero_veces = int(request.form['veces'])

        # Calcular el tiempo de envío (2 minutos en el futuro)
        ahora = datetime.now()
        tiempo_envio = ahora + timedelta(minutes=2)
        hora_envio = tiempo_envio.hour
        minuto_envio = tiempo_envio.minute

        try:
            # Enviar el primer mensaje con pywhatkit
            print(f"Preparando para enviar mensaje al número {numero} en 2 minutos...")
            kit.sendwhatmsg(numero, mensaje, hora_envio, minuto_envio)
            print(f"Mensaje programado para enviarse a las {hora_envio}:{minuto_envio}.")
            
            # Esperar que la página de WhatsApp Web cargue
            print("Esperando que se abra WhatsApp Web...")
            time.sleep(15)  # Ajusta este tiempo según el rendimiento de tu sistema
            
            # Hacer clic en el campo de entrada del mensaje
            print("Preparando para enviar múltiples mensajes...")
            pyautogui.click(1000, 700)  # Cambia las coordenadas si es necesario
            time.sleep(2)

            # Enviar el mensaje varias veces
            for i in range(1, numero_veces):
                pyautogui.write(mensaje)
                pyautogui.press('enter')
                print(f"Mensaje enviado correctamente. Iteración: {i + 1}")
                time.sleep(10)  # Espera entre envíos

        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
            return "Hubo un error al enviar los mensajes. Verifica la consola para más detalles."

    return render_template('index.html')

if __name__ == '__main__':
    print("Iniciando la aplicación Flask...")
    app.run(debug=True)
