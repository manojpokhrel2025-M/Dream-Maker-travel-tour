import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Dream Makers Tours', os.environ.get('MAIL_USERNAME'))
app.config['MAIL_DEBUG'] = True

# ✅ Print loaded credentials (remove after debugging)
print("MAIL_USERNAME:", app.config['MAIL_USERNAME'])
print("MAIL_PASSWORD:", '***' if app.config['MAIL_PASSWORD'] else 'Not Set')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        msg = Message(
            subject=f"New Inquiry from {name} - Dream Makers Website",
            recipients=['gpmanojjj@gmail.com'],
            reply_to=email
        )
        msg.html = render_template('email_template.html', name=name, email=email, phone=phone, message=message)

        try:
            mail.send(msg)
            flash('Your message has been sent successfully! We\'ll get back to you soon.', 'success')
        except Exception as e:
            # ✅ Print the full error to the terminal
            print("="*50)
            print("ERROR sending email:")
            print(e)
            print("="*50)
            # Temporarily show error to user (remove later)
            flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True)