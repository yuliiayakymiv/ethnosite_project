from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from database import engine, Base, SessionLocal
from models import News
from datetime import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.getenv("SECRET_KEY", "supersecret")


Base.metadata.create_all(bind=engine)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create upload folder if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def add_news(title, name, category, region, text, photo=None):
    db = SessionLocal()

    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    timestamp = int(datetime.now().timestamp())

    news_item = News(
        title=title,
        name=name,
        category=category,
        region=region,
        text=text,
        photo=photo,
        date=date,
        timestamp=timestamp
    )

    db.add(news_item)
    db.commit()
    db.close()


def get_all_news():
    db = SessionLocal()
    news = db.query(News).order_by(News.timestamp.desc()).all()
    db.close()
    return news


def get_news_by_region(region):
    db = SessionLocal()
    news = (
        db.query(News)
        .filter(News.region == region)
        .order_by(News.timestamp.desc())
        .all()
    )
    db.close()
    return news



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

    return render_template(
        'news.html',
        news_list=news_list,
        selected_region=region
    )


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

if __name__ == '__main__':
    app.run()