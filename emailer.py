import smtplib

def send_email(header, body, email):
	# Set up the email message
	from_email = 'ignoremarietess2000@gmail.com'
	to_email = email
	subject = header
	body = body

	message = f'Subject: {subject}\n\n{body}'

	# Set up the SMTP server
	smtp_server = 'smtp.gmail.com'
	port = 587
	smtp_username = 'quizkpynoreply@gmail.com'
	smtp_password = 'egpnrrpwhvnekohp'

	smtp_conn = smtplib.SMTP(smtp_server, port)
	smtp_conn.starttls()
	smtp_conn.login(smtp_username, smtp_password)

	# Send the email
	smtp_conn.sendmail(from_email, to_email, message)

	# Close the connection
	smtp_conn.quit()
