from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import render_template, redirect, url_for, request, session

app = Flask(__name__)
password = quote_plus('Ak@080901')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/conference_data'
db = SQLAlchemy(app)

class ConferenceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    conference = db.Column(db.String(120), nullable=False)

@app.route('/')
def main():
    if 'username' in session:
        conferences = ConferenceData.query.with_entities(ConferenceData.conference).distinct()
        return render_template('main.html', conferences=conferences)
    else:
        return redirect(url_for('login'))
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    name = request.form['name']
    conference = request.form['conference']

    data = ConferenceData(email=email, name=name, conference=conference)
    db.session.add(data)
    db.session.commit()

    return 'Data submitted successfully!'

@app.route('/retrieve')
def retrieve():
    conferences = ConferenceData.query.with_entities(ConferenceData.conference).distinct()
    return render_template('retrieve.html', conferences=conferences)

@app.route('/display', methods=['POST'])
def display():
    selected_conference = request.form['selected_conference']
    data = ConferenceData.query.filter_by(conference=selected_conference).all()
    return render_template('display.html', data=data)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # For simplicity, hardcoding the credentials (replace with database check)
        if username == 'Akarsh' and password == '123456':
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')

    return render_template('login.html', message=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.secret_key = '123456'
    app.run(debug=True)


