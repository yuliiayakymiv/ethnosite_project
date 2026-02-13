from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Створюємо папку для завантажень, якщо її немає
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

news_list = []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    return render_template('news.html', news_list=news_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        name = request.form.get('name')
        title = request.form.get('title')
        category = request.form.get('category')
        region = request.form.get('region')
        text = request.form.get('text')
        
        # Обробка завантаженого файлу
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                photo_filename = photo.filename
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        
        # Додаємо новину до списку
        news_item = {
            'name': name,
            'title': title,
            'category': category,
            'region': region,
            'text': text,
            'photo': photo_filename
        }
        news_list.append(news_item)
        
        # Перенаправляємо на сторінку новин
        return redirect(url_for('news'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)