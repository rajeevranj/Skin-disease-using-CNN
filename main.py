from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
from forms import RegistrationForm, LoginForm
import pymysql
import pymysql.cursors
import pandas as pd
import os
from audio_wave import *

APP_ROOT=os.path.dirname(os.path.abspath(__file__))
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join(APP_ROOT, 'static/image/')
app.config['SECRET_KEY']='b0b4fbefdc48be27a6123605f02b6b86'

@app.before_first_request
def initialize():
    session['loggedin']=False

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    #Database connection
    db=pymysql.connect(host="localhost", port=3306, user="root", password="", db="emotion_recognition", cursorclass=pymysql.cursors.DictCursor)
    #Table as a data frame
    register=pd.read_sql_query('select * from {}'.format('register'), db)

    if form.validate_on_submit():
        all_emails=register['email']
        if form.email.data in list(all_emails):
            row=all_emails[all_emails==form.email.data]
            index=row.index[0] ### Id is (1 + index)
            if form.password.data == register['password'][index]:
                session['loggedin']=True
                flash(f"Welcome {register['name'][index]} ! You have been logged in.",'success')
                return redirect(url_for('application'))
            else:
                flash("You password was incorrect. Please try again with correct password.",'warning')
                return redirect(url_for('login'))
        else:
            flash(f"No account with the email id {form.email.data} exists. Please register now.",'info')
            return redirect(url_for('register'))
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    #Database connection
    db=pymysql.connect(host="localhost", port=3306, user="root", password="", db="emotion_recognition", cursorclass=pymysql.cursors.DictCursor)
    #Table as a data frame
    register=pd.read_sql_query('select * from {}'.format('register'), db)

    if form.validate_on_submit():
        email=form.email.data
        all_emails=register['email']
        if email in list(all_emails):
            flash('Account already exists with this Email Id! Please Log In.','warning')
            db.close()
            return redirect(url_for('login'))
        else:
            #Insert new record
            try:
                with db.cursor() as cur:
                    sql = "INSERT INTO `register` (`name`,`email`,`password`) VALUES (%s, %s, %s)"
                    cur.execute(sql, ({form.username.data}, {form.email.data}, {form.password.data}))
                db.commit()
            finally:
                db.close()
            flash(f'Account Created for {form.username.data} Sucessfully!','success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/upload", methods=["POST"])
def upload():
    target=os.path.join(APP_ROOT, 'static/audio/')

    if not os.path.isdir(target):
        os.mkdir(target)
    file=request.files["myaudio"]
    filename=file.filename
    if filename=="":
        flash('No File Selected','danger')
        return redirect(url_for('application'))

    destination="/".join([target, filename])
    #Extension check
    ext = os.path.splitext(destination)[1]
    if (ext==".wav"):
        pass
    else:
        flash("Invalid Extenstions! Please select a .wav audio file only.", category="danger")
        return redirect(url_for('application'))

    if not os.path.isfile(destination):
        file.save(destination)

    result=record_audio(record=False, file_loc=destination)
    new_dest=('static/audio/'+str(filename))
    return render_template("upload.html", img_name=filename, emo=result, destination=new_dest)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    #flash('Logged Out Sucessfully!','success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
