import smtplib, ssl

def send_email(message, recipient_email):
    smtp_server = "smtp.gmail.com"
    port = 587
    with open("data.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split(",")
            sender_email = line[0]
            password = line[1]

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()

