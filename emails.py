# -*- coding: utf-8 -*-

# Import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

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


# Set up the SMTP server
s = SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login('XYZ@gmail.com', 'pwdstring')  # TODO: update this

# Set up the parameters of the message
msg = MIMEMultipart()
msg['From'] = 'name'  # TODO: update this
msg['To'] = 'XYZ@gmail.com'  # TODO: update this
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
