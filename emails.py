# -*- coding: utf-8 -*-

# Import necessary packages
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from urllib.parse import urlencode
from urllib.request import urlopen

from utils import shuffle, song_info, translate

# Find and shuffle songs
songs = shuffle()

# Loop until get song with translations or run out of songs
i = 0
cont = True
while cont:
    # Get song information
    song_link, title, artist, lyrics, video_link = song_info(songs[i])

    # Translate song
    translations = translate(title + artist + lyrics)

    # Iterate counter and continue loop if no translations and still have songs remaining
    i += 1
    cont = (i < len(songs)) and len(translations) == 0

# Make translations into one giant block of text
translations = '\n'.join(translations)


# Gmail variables and tokens
GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
GOOGLE_CLIENT_ID = 'XXX.apps.googleusercontent.com'  # TODO: update this
GOOGLE_CLIENT_SECRET = 'XXX'  # TODO: update this
GOOGLE_REFRESH_TOKEN = 'XXX'  # TODO: update this

# Emails
username = 'XXX@gmail.com'  # TODO: update this
toaddr = 'XXX@gmail.com'  # TODO: update this

# Get access token
params = {
    'client_id': GOOGLE_CLIENT_ID,
    'client_secret': GOOGLE_CLIENT_SECRET,
    'refresh_token': GOOGLE_REFRESH_TOKEN,
    'grant_type': 'refresh_token',
}
request_url = f'{GOOGLE_ACCOUNTS_BASE_URL}/o/oauth2/token'
response = urlopen(request_url, urlencode(params).encode('UTF-8')).read().decode('UTF-8')
access_token = json.loads(response)['access_token']

# Get authorization string
auth_string = f'user={username}\1auth=Bearer {access_token}\1\1'
auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')

# Set up the SMTP server
s = SMTP(host='smtp.gmail.com', port=587)
s.ehlo(GOOGLE_CLIENT_ID)
s.starttls()
s.docmd('AUTH', 'XOAUTH2 ' + auth_string)

# Set up the parameters of the message
msg = MIMEMultipart()
msg['From'] = username
msg['To'] = toaddr
msg['Subject'] = 'Daily digest'

# Create message
message = (
    'Song of the day: {}\n'.format(title)
    + 'Artist: {}\n\n'.format(artist)
    + 'Song link: {}\n'.format(song_link)
    + 'Video link: {}\n\n'.format(video_link)
    + 'Lyrics: {}\n\n'.format(lyrics)
    + 'Translations: \n{}'.format(translations)
)

# Add in the message body
msg.attach(MIMEText(message, 'plain'))

# Send the message
s.send_message(msg)
del msg

# Terminate the SMTP session and close the connection
s.quit()
