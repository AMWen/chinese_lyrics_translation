# chinese_lyrics_translation
This was a quick project with web scraping and regularized expressions to find a random Chinese song, get the lyrics and corresponding Youtube video, provide word-by-word pronunciations and translations (of any words not previously seen), and email the compiled results.

The Jupyter notebook has initial concept development, while the Python files are slightly more sophisticated, wrapping most things into functions. `emails.py` is the main document and `utils.py` provides some helper functions.

To use, need to update email account credentials in `emails.py` and create and specify locations for files to save lists of already seen words and exceptions under `utils.words_io`.

This could be combined with a job scheduler such as crontab to automatically send translations for a random song each day for daily language learning.

**Example:** `15 8,20 * * * //anaconda3/bin/python /link/to/emails.py > /tmp/test.log` to run the `emails.py` code every day at 8:15 am and pm.

## Sample email output

    Song of the day: 憂愁 (Gloom)
    Artist: 琳誼 Ring

    Song link: https://www.kkbox.com/tw/tc/song/lFB0051a0Y78TbJN8TbJN0XL-index.html
    Video link: https://www.youtube.com/watch?v=fIcyi6tUhUY

    Lyrics:
    若不是為了你 我哪會這麼憂愁

    又擱睏袂去 猶原擱想到你
    親像你在我的身邊
    情願不識你 乎兩人的代誌
    隨一切漸漸的過去

    想起當初時 你牽著我的手
    講永遠袂放抹記
    就是放抹去 來乎你留置阮的心
    每日相見 為你傷害自己

    若不是為了你 我哪會這麼憂愁
    來乎人看不起 來為你睏袂去
    若不是因為你 我早就放咧乎去
    因為你不值我 將燒酒飲下去

    若不是為了你 我哪會這麼憂愁
    來乎人看不起 來為你睏袂去
    若不是因為你 我早就放咧乎去
    因為你不值我 將燒酒飲下去
    我想不開 我愛上你
    我想不開 我愛上你 我愛上你

    想起當初時 你牽著我的手
    講永遠袂放抹記
    就是放抹去 來乎你留置阮的心
    每日相見 為你傷害自己 （我愛上你）

    若不是為了你 我哪會這麼憂愁
    來乎人看不起 來為你睏袂去
    若不是因為你 我早就放咧乎去
    因為你不值我 將燒酒飲下去

    若不是為了你 我哪會這麼憂愁
    來乎人看不起 來為你睏袂去
    若不是因為你 我早就放咧乎去
    因為你不值我 將燒酒飲下去

    若不是為了你 我哪會這麼憂愁
    來乎人看不起 來為你睏袂去
    若不是因為你 我早就放咧乎去
    因為你不值我 將燒酒飲下去

    我愛上你 我愛上你
    我愛上你 我愛上你
    我想不開 我愛上你 我愛上你


    Translations:
    講: jiang3, to speak, to explain, to negotiate, to emphasise, to be particular about, as far as sth is concerned, speech, lecture
    留置: liu2zhi4, to leave in place, to set aside (for further use), to retain, to detain, (medicine) indwelling
    看不起: kan4bu5qi3, to look down upon, to despise
    不值: bu4zhi2, not worth
    燒酒: shao1jiu3, name of a famous Tang dynasty wine, same as 白酒[bai2 jiu3]
