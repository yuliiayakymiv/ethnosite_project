from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from database import init_db, add_news, get_all_news, get_news_by_region

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Створюємо папку для завантажень, якщо її немає
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    region = request.args.get('region', '')
    if region:
        news_list = get_news_by_region(region)
    else:
        news_list = get_all_news()
    return render_template('news.html', news_list=news_list, selected_region=region)

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        title = request.form.get('title')
        category = request.form.get('category')
        region = request.form.get('region')
        text = request.form.get('text')

        # Фото/відео — безпечне збереження з унікальним іменем
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename and allowed_file(photo.filename):
                ext = photo.filename.rsplit('.', 1)[1].lower()
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                photo_filename = unique_name

        add_news(title, name, category, region, text, photo_filename)

        return redirect(url_for('news'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)