

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
# Імпортуємо тільки необхідне
from database import init_db, add_news, get_all_news, get_news_by_region

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

# Створюємо таблиці при запуску
init_db()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

@app.route('/react/<int:news_id>/<string:reaction_type>', methods=['POST'])
def react(news_id, reaction_type):
    from database import SessionLocal, News
    db = SessionLocal()
    news_item = db.query(News).filter(News.id == news_id).first()

    if not news_item:
        db.close()
        return jsonify({"error": "News not found"}), 404

    # Action може бути 'add' або 'remove'
    data = request.json
    action = data.get('action', 'add')
    increment = 1 if action == 'add' else -1

    # оновлюємо потрібний лічильник
    field_name = f"{reaction_type}_count"
    if hasattr(news_item, field_name):
        current_val = getattr(news_item, field_name) or 0
        setattr(news_item, field_name, max(0, current_val + increment))
        db.commit()

    result = {reaction_type: getattr(news_item, field_name)}
    db.close()
    return jsonify(result)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    from database import SessionLocal, News
    db = SessionLocal()
    # Шукаємо новину в базі за її ID
    news_item = db.query(News).filter(News.id == news_id).first()
    db.close()

    if news_item:
        return render_template('news_detail.html', n=news_item)
    else:
        return "Новину не знайдено", 404@app.route('/news/<int:news_id>')


if __name__ == '__main__':
    app.run(debug=True)
