# import smtplib
# try:
#     server = smtplib.SMTP("smtp.gmail.com",port=597)
#     server.starttls()
#     #receiver email
#     receiver_mail = input("enter the receiver mail:")
#     ##small creditals
#     sender_email = "scollege869@gmail.com"
#     password = "owjw fuyh gsqg navj"
#     server.login(sender_email,password)


#     subject = input("enter the subject:")
#     body = input("enter the body:")
#     message = f"subject:{subject} \n\n {body}"
#     server.sendmail(sender_email,receiver_mail,message)
#     print("mail sent")
#     server.quit()
# except Exception as e:
#     print("an error occured",e)

import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.ehlo()  # optional, but sometimes helpful
    server.starttls()
    server.ehlo()

    receiver_mail = input("Enter the receiver email: ")
    sender_email = "scollege869@gmail.com"
    password = "owjw fuyh gsqg navj"  # App password

    server.login(sender_email, password)

    subject = input("Enter the subject: ")
    body = input("Enter the body: ")
    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(sender_email, receiver_mail, message)
    print("Mail sent successfully.")
    server.quit()

except Exception as e:
    print("An error occurred:", e)
