# chinese_lyrics_translation
This was a quick project with web scraping and regularized expressions to find a random Chinese song, get the lyrics and corresponding Youtube video, provide word-by-word pronunciations and translations, and email the compiled results.

The Jupyter notebook has initial concept development, while the Python files are slightly more sophisticated, wrapping most things into functions. `emails.py` is the main document and `utils.py` provides some helper functions.

To use, need to update email account credentials in `emails.py` and create and specify locations for files to save lists of already seen words and exceptions under `utils.words_io`.

This could be combined with a job scheduler such as crontab to automatically send translations for a random song each day for daily language learning.
