
# sgfspider

Playing with [scrapy](http://scrapy.org), crawling the web for SGF Go game files.

Currently ideas only; i.e, incomplete.

Uses Python 2.7 (because of the dependency on scrapy).

You probably want to sandbox the runtime by [making sure virtualenvwrapper is installed](http://docs.python-guide.org/en/latest/dev/virtualenvs/), then:

```
$ mkvirtualenv sgfspider
$ workon sgfspider
$ pip install -r requirements.txt
```

to test:
```
$ nosetests
```

I use [redgreen](https://github.com/vmalloc/redgreen) for continuous testing
```
$ redgreen
```

A rudimentary shell script will scrape the latest games it can find and write them to the db:

```
$ ./scrape_games.sh
```

## Requirements

* Python 2.7
* Postgresql (any db would do; I just happened to write this for pgsql)

## Resources

* [scrapy.org](http://scrapy.org)
