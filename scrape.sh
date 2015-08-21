#!/bin/sh 

scrapy crawl igokisen -t json -o items.json --loglevel WARNING

# TODO: http://doc.scrapy.org/en/latest/topics/practices.html#run-from-script
