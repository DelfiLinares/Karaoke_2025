import os
import socket
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid 

UPLOAD_FOLDER = '../videos_grabados' 
PORT = 5000

app = Flask(__name__)
CORS(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB máximo

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

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    # Manejar preflight request de CORS
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
    
    try:
        if 'file' not in request.files:
            print("❌ Error: No se encontró el archivo en la petición")
            return jsonify({"success": False, "error": "No se encontró el archivo"}), 400

        file = request.files['file']

        if file.filename == '':
            print("❌ Error: Nombre de archivo vacío")
            return jsonify({"success": False, "error": "Ningún archivo seleccionado"}), 400

        # Generamos un nombre de archivo único
        filename = secure_filename(str(uuid.uuid4()) + ".webm")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"📹 Guardando video como: {filename}")
        file.save(filepath)
        
        # Verificar que el archivo se guardó correctamente
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ Video guardado correctamente: {filename} ({file_size} bytes)")
        else:
            print(f"❌ Error: El archivo no se guardó correctamente")
            return jsonify({"success": False, "error": "Error al guardar el archivo"}), 500

        # Construimos la URL completa para el QR
        local_ip = get_local_ip()
        video_url = f"http://{local_ip}:{PORT}/videos/{filename}"

        print(f"🔗 URL generada para QR: {video_url}")
        
        # Devolvemos la URL al navegador
        return jsonify({"success": True, "url": video_url}), 200
        
    except Exception as e:
        print(f"❌ Error en upload_file: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/videos/<filename>')
def uploaded_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            print(f"📤 Sirviendo video: {filename}")
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        else:
            print(f"❌ Video no encontrado: {filename}")
            return jsonify({"error": "Video no encontrado"}), 404
    except Exception as e:
        print(f"❌ Error al servir video: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Ruta de prueba para verificar que el servidor funciona"""
    return jsonify({"status": "OK", "message": "Servidor funcionando correctamente"}), 200

if __name__ == '__main__':
    # Crear la carpeta de subidas si no existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print(f"📁 Carpeta creada: {UPLOAD_FOLDER}")

    local_ip = get_local_ip()
    print("=" * 50)
    print("🎤 SERVIDOR DE KARAOKE INICIADO")
    print("=" * 50)
    print(f"📱 IP Local: {local_ip}")
    print(f"🔌 Puerto: {PORT}")
    print(f"🌐 URL del servidor: http://{local_ip}:{PORT}")
    print(f"📹 Videos se guardarán en: {os.path.abspath(UPLOAD_FOLDER)}")
    print("\n⚠️  IMPORTANTE:")
    print("   1. Asegúrate de que todos los dispositivos estén en la MISMA red WiFi")
    print("   2. Abre video.html desde un servidor HTTP (no directamente)")
    print("   3. Para probar el servidor: http://localhost:5000/test")
    print("=" * 50)

    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)