from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import timedelta
import bcrypt
import mysql.connector
from googletrans import Translator
from flask_cors import CORS






app = Flask(__name__)
CORS(app)
translator = Translator()
app.secret_key = "Hello"
app.permanent_session_lifetime = timedelta(minutes=30)

def get_db_connection():
    connection = mysql.connector.connect(
        host='bdjevq5pofvlmbui9v8y-mysql.services.clever-cloud.com',
        user='u1wlojoslzwigmqm',
        password='h9ZALlV54SZ39gjiKCPa',
        database='bdjevq5pofvlmbui9v8y'
    )
    return connection

@app.route('/')
def index():
    
    if "username" in session:
        return redirect(url_for('homepage'))
    else:
        return render_template('land.html')
    
@app.route('/logpage')
def logp_disp():
    return render_template('logpage.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userid = request.form['mail']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE UserID = %s"
        cursor.execute(query, (userid,))
        exuser = cursor.fetchone()

        if exuser:
            flash("Already registered!","error")
        else:
            query = "INSERT INTO users (Name,UserID,Password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, userid, hashed_password))
        
            connection.commit()
            cursor.close()
            connection.close()
            flash("Registration Successful!","success")
        
        return redirect(url_for('logp_disp'))

@app.route('/log_in', methods=['POST'])
def log_in():
    if request.method == 'POST':
        userid = request.form.get('mail')
        password = request.form.get('password')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE UserID = %s"
        cursor.execute(query, (userid,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            stored_username = user[1]  
            stored_password = user[3]
            stored_mailid = user[2]  
            session["pword"]=stored_password

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session["username"] = stored_username
                session["mailid"] = stored_mailid
                print(f"Session mailid set to: {session['mailid']}")
                session.permanent= True
                return redirect(url_for('homepage'))
            else:
                flash("Incorrect Password","error")
                
        else:
            flash("User not found","error")
            
        return redirect(url_for('logp_disp'))


"""@app.route('/home')
def home():
    if 'username' in session:
        uname = session["username"]
        return render_template('homepage.html', username=uname)
    else:
        return redirect(url_for('index'))"""

@app.route('/log_out', methods=['GET'])
def log_out():
    session.clear() 
    return redirect(url_for('index'))

@app.route('/changepasswordform',methods=['POST','GET'])
def chngpasswordform():
    return render_template('changepword.html')

@app.route('/changepassword',methods=['POST','GET'])
def changepassword():
    newpassword = request.form.get('newpassword')
    renewpassword = request.form.get('renewpassword')

    if (newpassword == renewpassword):
        new_hashed_password = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())
        connection = get_db_connection()
        cursor = connection.cursor()
        user_id = session["username"]
        query = "UPDATE users SET Password = %s WHERE Name = %s"
        cursor.execute(query, (new_hashed_password, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        session.clear()

        
        return redirect(url_for('logp_disp'))

    else:
        return redirect(url_for('chngpasswordform'))

        

@app.route('/validate_password',methods=['POST'])
def validate_password():
    if request.method == 'POST':
        data = request.get_json()

        old_pword = data.get('oldpword')
        originalpword = session["pword"]

        if bcrypt.checkpw(old_pword.encode('utf-8'), originalpword.encode('utf-8')):
            
            return jsonify(success=True)
        else:
            
            return jsonify(success=False)

@app.route('/profile')
def profile():
    if 'username' in session:
        uname = session["username"]
        mailname = session["mailid"]
        return render_template('prof.html',username=uname,mail=mailname)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/chatpage')
def chatpage():
    return render_template('chat.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    srclang = data.get('source')
    trglang = data.get('target')

    if text:
        try:
            translated = translator.translate(text, src=srclang, dest=trglang)
            return jsonify({'translated_text': translated.text})
        except Exception as e:
            print(f"Error during translation: {str(e)}")
            return jsonify({'error': 'Translation failed'}), 500
    return jsonify({'error': 'No text provided'}), 400



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

