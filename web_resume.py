from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret-key')  # Needs additional configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            msg = Message('New Contact Form Submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']])

            msg.body = f"""
            New message from your portfolio website:

            From: {name}
            Email: {email}

            Message:
            {message}
            """

            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')

        except Exception as e:
            print(e)  # For debugging
            flash('An error occurred while sending your message.', 'error')

        return redirect(url_for('home', _anchor='contact'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))