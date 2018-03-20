import smtplib
from config import *
def send_mail(msg):
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.starttls()
       server.login(login, password)
       server.sendmail("lololo123laura456@gmail.com", "vip-laura2002@mail.ru", msg.encode("utf-8"))
       server.quit()
       return True
