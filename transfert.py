import sys
import os
import qrcode
import base64
from io import BytesIO
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = os.path.expanduser("~/Downloads/transferts")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Adresse IP et port
ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = 5000
url = f"http://{ip}:{port}"

def generate_qr_base64():
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        for f in files:
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        return "✅ Fichiers transférés avec succès !"
    qr_data = generate_qr_base64()
    return render_template("upload.html", qr_data=qr_data, server_url=url)

@app.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    links = [f"<a href='/download/{f}'>{f}</a>" for f in files]
    return "<br>".join(links)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    print(f"📱 Ouvre {url} sur ton navigateur ou scanne le QR code affiché.")
    app.run(host="0.0.0.0", port=port)

