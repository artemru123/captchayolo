from flask import Flask, request, jsonify, send_from_directory, make_response, session
import random
import secrets
import io
from PIL import Image, ImageDraw, ImageFont
from flask_cors import CORS  # Добавить импорт
from flask_session import Session  # Импорт библиотеки для сессий

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




@app.route('/captcha')
def generate_captcha():
    # Генерация случайного числа
    captcha_value = random.randint(100000, 999999)
    session['captcha_value'] = captcha_value  # Сохранение капчи в сессию

    image = Image.new('RGB', (150, 60), 'black')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('static/arial.ttf', 20) # Загрузка шрифта

    x = 0
    for digit in str(captcha_value):
        draw.text((x, 15), digit, fill='white', font=font)
        bbox = font.getbbox(digit)
        x += bbox[2] - bbox[0] + 5

















    noise_intensity = 10
    for i in range(noise_intensity):
        x = random.randint(0, image.width - 1)
        y = random.randint(0, image.height - 1)
        image.putpixel((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


    for i in range(image.width):
        for j in range(image.height):
            r, g, b = image.getpixel((i, j))
            if random.random() < 0.1:
                r = min(255, r + random.randint(-20, 20))
                g = min(255, g + random.randint(-20, 20))
                b = min(255, b + random.randint(-20, 20))
                image.putpixel((i, j), (r, g, b))


    for i in range(image.width - 1):
        for j in range(image.height):
            if random.random() < 0.1:
                r, g, b = image.getpixel((i + 1, j))
                image.putpixel((i, j), (r, g, b))

    for i in range(image.width):
        for j in range(image.height - 1):
            if random.random() < 0.1:
                r, g, b = image.getpixel((i, j + 1))
                image.putpixel((i, j), (r, g, b))


    for _ in range(3):
        x1 = random.randint(0, image.width)
        y1 = random.randint(0, image.height)
        x2 = random.randint(0, image.width)
        y2 = random.randint(0, image.height)
        draw.line((x1, y1, x2, y2), fill='white', width=2)

    for _ in range(3):
        x1 = random.randint(0, image.width)
        y1 = random.randint(0, image.height)
        x2 = random.randint(x1, image.width)
        y2 = random.randint(y1, image.height)
        draw.rectangle((x1, y1, x2, y2), outline='white', width=2)

    # Сохранение изображения в байтовый поток
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    print(f"CAPTCHA image generated. Size: {image.size}")
    # Возврат изображения как ответа
    return make_response(img_io.getvalue(), 200, {'Content-Type': 'image/jpeg'})

@app.route('/check_captcha', methods=['POST'])
def check_captcha():
    user_captcha = request.form.get('captcha')
    if user_captcha is not None and user_captcha.isdigit() and int(user_captcha) == session.get('captcha_value'):
        return 'success'
    else:
        return 'error'
@app.route('/html/<path:filename>')
def serve_html(filename):
    """Serves HTML files from the specified directory."""
    return send_from_directory('C:/Users/22835/Desktop/html', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
