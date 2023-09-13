import mysql.connector
import os
from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Function to insert form data into the MySQL database


def insert_form_data(name, email, message, gender, subscribe):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',  # Replace with your MySQL password
        database='form'
    )
    cursor = connection.cursor()
    sql = 'INSERT INTO users (name, email, message, gender, subscribe) VALUES (%s, %s, %s, %s, %s)'
    if subscribe == 'on':
        subscribe = 1
    else:
        subscribe = 0
    data = (name, email, message, gender, subscribe)
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['mail']
        message = request.form['message']
        gender = request.form['gender']
        subscribe = request.form.get('Subscribe', False)
        # Handling file upload
        photo = request.form['photo']
        if photo:
            photo_filename = photo.filename
        #     # Save the photo to a desired location
        photo.save('uploads/' + photo_filename)


        insert_form_data(name, email, message, gender, subscribe)

        # Send email to the entered email address
        send_email(name, email, message, gender, subscribe)

        return render_template('form2.html')
    return render_template('form.html')


def send_email(name, email, message, gender, subscribe):
    # Replace the following variables with your email configuration
    sender_email = 'nawabdar5@gmail.com'
    sender_password = 'jlocbokxuhojzuit'
    receiver_email = email

    subject = 'Thank you for submitting the form! (Automated Response) now you are enrolled in I.T.vedant banglore'
    body = f'''
    Hi {name},
    you can submit your Fee here:"https://student.itvedant.com/index.php/student/fees"
    while complete your fee dues you will recive another email regarding feee 
    if you have any issue plz contact us" :https://www.itvedant.com"


    We hope this email finds you well. We wanted to express our sincerest gratitude for taking the time to complete our form. Your valuable input means a great deal to us.

	Here are the details you submitted:

    Name: {name}
    Email: {email}
    Message: {message}
    Gender: {gender}
    Subscribe: {subscribe}

    As this is an automated message, please do not reply to this email. Should you have any questions, concerns, or further feedback, we kindly request you to contact us through the appropriate channels provided on our website.

    Regards,
    NAWAB AHMAD DAR
    '''

    # Create a MIMEText object to represent the email content
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(body, 'plain'))

    # Connect to the email server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email,
                        email_message.as_string())


if __name__ == '__main__':
    app.run(debug=True)
