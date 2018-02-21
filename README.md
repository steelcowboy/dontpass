# Don't Pass v0.3
Don't Pass is a Python tool you can run to scrape data from Cal Poly PASS
and put that information into a database. It allows you to select classes to
scrape and puts them in a database, and includes a web interface that allows
you to sort through this information and see statistics about the
changes in registration over time (if a daemon has been periodically running the
database-update, that is!)

## Dependencies
- phantomjs
- python-selenium
- django >2.0

## Config file
Don't Pass requires a settings.py file to be in the src dir with the following
variables declared:

`classes`: A list of classes which you wish to have displayed
`instructors`: A list of instructors to filter the classes
`show_all_inst`: If this is not false, all instructors will be shown for all
classes
`show_closed`: Whether or not you wish to see closed classes
`color`: If this is not false, ANSI escape sequences will be used to colorize
classs headers

## Updating the database
More to be written, but currently run `manage.py update_database`. The structure
of all this will be explained in due time

# TO-DO
- Add graphs to the web interface
- Better styling
- Cool tools
- User accounts?
