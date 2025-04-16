import boto3
import io
import base64
from flask import Flask, request, render_template, redirect, url_for, flash

AWS_REGION = 'us-east-1'
try:
    rekognition_client = boto3.client('rekognition', region_name=AWS_REGION)
except Exception as e:
    print(f"Критична помилка: Не вдалося створити клієнт Boto3. Перевірте облікові дані/регіон. Помилка: {e}")
    rekognition_client = None 

app = Flask(__name__)
app.secret_key = 'very_secret_key_here' 

# Дозволені розширення файлів зображень
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Функція для перевірки дозволеного типу файлу
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_and_detect():
    if not rekognition_client:
         flash("Помилка: AWS Rekognition клієнт не ініціалізовано. Перевірте конфігурацію.", "error")
         return render_template('index.html', results=None, uploaded_image_data=None)

    if request.method == 'POST':
        # Перевірка, чи файл є у запиті
        if 'image_file' not in request.files:
            flash('Файл не було надіслано', 'warning')
            return redirect(request.url)

        file = request.files['image_file']

        # Якщо користувач не вибрав файл, браузер надсилає порожній файл без імені
        if file.filename == '':
            flash('Файл не вибрано', 'warning')
            return redirect(request.url)

        # Якщо файл існує та має дозволене розширення
        if file and allowed_file(file.filename):
            try:
                # Читання байтів зображення
                image_bytes = file.read()

                #  API Rekognition
                response = rekognition_client.detect_labels(
                    Image={'Bytes': image_bytes},
                    MaxLabels=10,         # кількість міток
                    MinConfidence=80.0    # впевненість
                )

                results = []
                if 'Labels' in response:
                    for label in response['Labels']:
                        label_info = {
                            'Name': label['Name'],
                            'Confidence': f"{label['Confidence']:.2f}%"
                        }
                        # Додавання батьківських категорій
                        if label.get('Parents'):
                             label_info['Parents'] = ", ".join([p['Name'] for p in label['Parents']])
                        results.append(label_info)

                # Кодування завантаженого зображення для відображення на сторінці
                file.seek(0)
                image_data_uri = base64.b64encode(file.read()).decode('utf-8')

                return render_template('index.html', results=results, uploaded_image_data=image_data_uri)

            except FileNotFoundError:
                 flash(f"Помилка: Файл не знайдено", "error")
                 return redirect(request.url)
            except Exception as e:
                flash(f"Помилка під час виклику AWS Rekognition API: {e}", "error")
                print(f"Помилка AWS Rekognition API: {e}")
                return render_template('index.html', results=None, uploaded_image_data=None)

        else:
            flash('Неприпустимий тип файлу. Дозволені: png, jpg, jpeg, gif', 'warning')
            return redirect(request.url)

    return render_template('index.html', results=None, uploaded_image_data=None)

# Запуск сервера розробки Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 