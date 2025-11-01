# app.py
from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_email_password'
RECEIVER_EMAIL = 'your_email@example.com' 

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('contactName')
        email = request.form.get('contactEmail')
        phone = request.form.get('contactPhone')
        reason = request.form.get('contactReason')
        message = request.form.get('contactMessage')

        email_message = EmailMessage()
        email_message['Subject'] = f'Contact Form Submission: {reason}'
        email_message['From'] = SMTP_USERNAME
        email_message['To'] = RECEIVER_EMAIL
        email_message.set_content(
            f"Name: {name}\nEmail: {email}\nPhone: {phone}\nReason: {reason}\n\nMessage:\n{message}"
        )

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
                smtp.send_message(email_message)
            flash('Your message has been sent successfully!', 'success')
            return redirect('/contact')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            print(f"Email sending failed: {e}")

    return render_template('contact.html') 

if __name__ == '__main__':
    app.run(debug=True)
