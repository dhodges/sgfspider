#!/bin/sh

# TODO: http://doc.scrapy.org/en/latest/topics/practices.html#run-from-script

echo 'searching games on http://igokisen.web.fc2.com...'

scrapy crawl igokisen -t json -o items.json --loglevel WARNING

NUMFILES=`find downloaded_games/|grep .sgf|wc|awk '{print $1}'`

echo
echo "$NUMFILES new file(s) found"
echo

./gather_downloaded_games.py
