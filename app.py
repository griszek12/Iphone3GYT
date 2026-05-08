from flask import Flask, request, send_file, render_template_string
import os
import subprocess
import uuid

app = Flask(__name__)

# Ultra prosty HTML, który nie zawiesi starego Safari
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iPhone 3G YT</title>
</head>
<body>
    <h2>YouTube dla iPhone 3G</h2>
    <form action="/convert" method="get">
        URL wideo:<br>
        <input type="text" name="url" style="width:90%"><br><br>
        <input type="submit" value="POBIERZ I KONWERTUJ">
    </form>
    <p style="font-size:12px; color:gray;">Poczekaj cierpliwie po kliknięciu...</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/convert')
def convert():
    url = request.args.get('url')
    if not url:
        return "Podaj link!"

    unique_id = str(uuid.uuid4())[:8]
    input_file = f"in_{unique_id}.mp4"
    output_file = f"out_{unique_id}.mp4"
    
    try:
        # 1. Pobieranie najniższej jakości (najszybciej)
        subprocess.run(f'yt-dlp -f "worst[ext=mp4]" "{url}" -o "{input_file}"', shell=True)

        # 2. Konwersja na format iPhone 3G: H.264 Baseline 1.3, 480x320, AAC audio
        ff_cmd = (
            f'ffmpeg -i {input_file} -c:v libx264 -profile:v baseline -level 1.3 '
            f'-s 480x320 -c:a aac -b:a 128k -ac 2 {output_file}'
        )
        subprocess.run(ff_cmd, shell=True)

        return send_file(output_file, as_attachment=True)
    
    except Exception as e:
        return f"Blad: {str(e)}"
    finally:
        # Sprzątanie plików, żeby nie zapchać dysku Railway
        if os.path.exists(input_file): os.remove(input_file)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
