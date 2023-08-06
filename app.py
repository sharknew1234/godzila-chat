from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site'
db = SQLAlchemy(app)


class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    img = db.Column(db.String(10000), nullable=True)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.app_context().push()
db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        text = request.form['text']
        img = request.files['image']

        if img and allowed_file(img.filename):
            filename = f"static/{img.filename}"
            img.save(filename)

            new_sms = SMS(text=text, img=filename)
            db.session.add(new_sms)
            db.session.commit()

            # return redirect(url_for('index'))

    sms = SMS.query.all()
    return render_template('index.html', sms=sms)


if __name__ == '__main__':
    app.run()
