import requests  #for http requests

from bs4 import BeautifulSoup  # for web scraping

import smtplib # for sending email

#importing 2 objects from email.mime for email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#system date and time manipulation
import datetime

now = datetime.datetime.now()

#email content placeholder

content = ''

#extracting HackerNews stories

def extract_news(url):
    print('Extracting HackerNews stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>\n'+'<br>'+'-'*50+'<br>') 
    response = requests.get(url)   #response is an http response body

    #this is local variable 
    content = response.content  #getting actual content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        #telling soup to find everything that is td with attributes class=title and valign=''
        #enumerate for all values with numbers
        cnt +=  ((str(i+1)+' ::  '+ tag.text + "\n" + '<br>')
        if tag.text != 'More' else ''
        )
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-----<br>')
content += ('<br><br>End of Message')

#composing mail
print('composing mail...')

#create parameters required for email authentication
SERVER = 'smtp.gmail.com'  #smtp server
PORT = 587 #port no
FROM = '*****************' #your from email id
TO= '*****************' #your to email ids (can be a list)
PASS = '********' #your email id's password

#fp = open(file_name,'rb')
#create a text/palin message
#msg = MIMEText('')
msg = MIMEMultipart()

#message.add_header('Content-Disposition','attachment',filename='empty.txt')
msg['Subject'] = 'Top News Stories HN (automated email)' + '' + str(now.day) + '.' + str(now.month) + '.' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

#attaching content to email and making it like html
msg.attach(MIMEText(content,'html'))

#fp.close()

#authentication

print('Initiating server...')

server = smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)   #to see debug messages 
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM,TO,msg.as_string())

print("email sent")

server.quit()




