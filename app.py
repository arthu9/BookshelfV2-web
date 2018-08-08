import smtplib


def send_email(subject, message, sender, password, recipients):
    try:
        sndr = '{}'.format(sender)
        pswrd = '{}'.format(password)
        rcpt = '{}'.format(recipients)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(sndr, pswrd)
        msg = 'Subject: {}\n\n{}'.format(subject, message)
        server.sendmail(sndr, rcpt, msg)
        server.quit()
        print("Success Email Sent")
    except:
        print("Email not sent")


@app.route('/send_email_message/<username>', methods=['POST', 'GET'])
def send_email_message(username):
    if g.user:
        if request.method == 'POST':
            subject = request.form['subject']
            message = request.form['message']
            password = request.form['password']
            response = requests.post('http://localhost:5050/email_info',
                                     json={'username': username, 'sender': session['user']})
            msg_dict = json.loads(response.text)
            if response.text == "Email Address not found":
                return render_template('error.html')
            else:
                sender = msg_dict['user']['sender']
                recipients = msg_dict['user']['recipients']
                email = send_email(subject, message, sender, password, recipients)
                print(email)
                return redirect(url_for('profile', username=username))
    else:
        return render_template('dashboard.html')