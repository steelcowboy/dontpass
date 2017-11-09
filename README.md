# Don't Pass v0.1
Don't Pass is a Python tool you can run to scrape data from Cal Poly PASS
and email you the information. It allows you to select classes (and optionally
professors) to watch, and can be configured to periodically email you regarding
updates to the number of seats available, the size of the waitlist, and other
relevant information.

## Dependencies
- phantomjs
- python-selenium

## Config file
Don't Pass requires a settings.py file to be in the src dir with the following
variables declared:

`classes`: A list of classes which you wish to have displayed
`instructors`: A list of instructors to filter the classes
`show_all_inst`: If this is not false, all instructors will be shown for all
classes
`show_closed`: Whether or not you wish to see closed classes
