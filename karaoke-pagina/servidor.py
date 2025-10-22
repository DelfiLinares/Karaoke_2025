import os
import socket
from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import uuid 

UPLOAD_FOLDER = 'videos_grabados' 
PORT = 5000

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    if file:
        # Generamos un nombre de archivo único para evitar que se sobreescriban
        filename = secure_filename(str(uuid.uuid4()) + ".webm")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Construimos la URL completa para el QR
        local_ip = get_local_ip()
        video_url = f"http://{local_ip}:{PORT}/videos/{filename}"

        # Devolvemos la URL al navegador
        return jsonify({"success": True, "url": video_url})

# --- Ruta para servir/descargar los videos guardados ---
@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Crear la carpeta de subidas si no existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    local_ip = get_local_ip()
    print("--- Servidor de Karaoke Listo ---")
    print(f"Para que funcione, los celulares deben conectarse a la misma red Wi-Fi.")
    print(f"La URL para el QR será similar a: http://{local_ip}:{PORT}/videos/...")
    print("---------------------------------")

    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)