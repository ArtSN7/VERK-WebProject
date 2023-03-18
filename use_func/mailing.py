import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send(mail, text):
	print('Работаем через Yandex')
	mailsender = smtplib.SMTP('smtp.yandex.ru', 587)
	mailsender.starttls()
	mailsender.login('VerkTeam@yandex.ru', 'Verk2023')
	mail_subject = 'Notification from Verk Team'
	mail_body = text
	msg = MIMEText(mail_body, 'plain', 'utf-8')
	msg['Subject'] = Header(mail_subject, 'utf-8')
	mailsender.sendmail('VerkTeam@yandex.ru', mail, msg.as_string())
	mailsender.quit()
	print('Сообщение на адрес', mail, 'отправлено')
    
    
#send('artem.17sn@gmail.com', txt)
#вызываем функцию в основной программе, mail - почта человека из бд, text - текст который мы хотим чтобы был в письме
