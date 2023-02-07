# -*- coding: utf-8 -*-

# Import necessary packages
import json
import random
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from chinese import ChineseAnalyzer

# Headers for urllib requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
}


# Function to get shuffled list of songs
def shuffle():
    chart_html = urlopen(Request('https://kma.kkbox.com/charts/weekly/song?cate=297', headers=headers)).read()
    songs = re.findall(
        r'"song_url":"https:\\/\\/www.kkbox.com\\/tw\\/tc\\/song\\/(\S{24}-index.html)"', chart_html.decode()
    ) + re.findall(r'"song_url":"https:\\/\\/www.kkbox.com\\/tw\\/tc\\/song\\/(\S{18})"', chart_html.decode())

    # Shuffle the songs
    random.shuffle(songs)

    return songs


# Function to find song title, artist, lyrics, and youtube link
def song_info(song):
    # Get the song link
    song_link = 'https://www.kkbox.com/tw/tc/song/' + song
    print(song_link)

    # Find title of song and clean up a bit
    song_html = urlopen(Request(song_link, headers=headers)).read()
    title = re.findall(r'\<title\>([^\t\n\r\f\v]*)-歌詞', song_html.decode())[0].replace('&lt;', '<').replace('&gt;', '>')
    print(title)

    # Find artist name
    artist = (
        re.findall(r'\<title\>[^\t\n\r\f\v]*-歌詞-([^\t\n\r\f\v]*)-', song_html.decode())[0]
        .replace('&lt;', '<')
        .replace('&gt;', '>')
    )
    print(artist)

    # Find lyrics and clean up a bit
    lyrics = (
        re.findall(r'"text":([^\t\n\r\f\v}]*)', song_html.decode())[0]
        .replace('\\n', '\n')
        .replace('"', '')
        .replace('\\r', '')
    )

    # Get video link from youtube
    html = urlopen("https://www.youtube.com/results?search_query=%s" % (quote(title + artist))).read()
    video_ids = re.findall(r"watch\?v=(\S{11})", html.decode())
    video_link = "https://www.youtube.com/watch?v=" + video_ids[0]
    print(video_link)

    return song_link, title, artist, lyrics, video_link


# Function to get list of words from seen or exceptions list
def words_io(typ='except', words=None):
    # Specify file path
    if typ == 'except':
        save_file = '/path/to/exceptions/file'  # TODO: update this
    else:
        save_file = '/path/to/seen/words/file'  # TODO: update this

    # Get list of words if none given
    if words is None:
        f = open(save_file, 'r')
        words = json.load(f)
        f.close()

        return words

    # Else write list of words to file
    else:
        with open(save_file, 'w') as f:
            f.write(json.dumps(list(words)))


# Function to add list of words to seen or exceptions list
def add(word_list, typ='except'):
    # Get list of words
    words = words_io(typ)

    # Append new word_list to list
    words.extend(word_list)

    # Print new list
    print(words)

    # Save new list
    words_io(typ, words)


# Function to remove list of words from seen or exceptions list
def remove(word_list, typ='except'):
    # Get list of words
    words = set(words_io(typ))

    # Remove new word_list
    words.difference_update(set(word_list))

    # Print new list
    print(words)

    # Save new list
    words_io(typ, words)


# Function to translate the lyrics
def translate(lyrics):
    analyzer = ChineseAnalyzer()
    result = analyzer.parse(lyrics, traditional=True)

    # Get list of words seen before
    seen = set(words_io('seen'))

    # Get list of words on exception list (want to review again)
    exceptions = set(words_io())

    # Remove exceptions from seen list
    seen.difference_update(set(exceptions))

    # Create list of unique words not seen before or want to review
    words = [word for word in result.tokens() if not (word in seen or seen.add(word))]

    # Save new list of words
    words_io('seen', seen)

    # Convert word list append pinyin and translation(s) to each word
    translations = []
    for word in words:
        defs = result[word]

        # Only proceed if matches to a word with a definition and pinyin
        if defs[0].pinyin is not None:

            # Go through all definitions if multiple (since dictionary need a separate key for each)
            for d in defs:
                translations.append(word + ': ' + ''.join(d.pinyin) + ', ' + ', '.join(d.definitions))

    return translations
