fetches classes and finals from ksu edugate website and generates an icalendar file to use to import to any other calendar app

### how to use:

1. run ```pip install -r requirements.txt```
2. run ```python main.py {browser} {student id} {password}``` possible browsers: {firefox, chrome, edge, safari}<br>
e.g.: ```python main.py chrome 444123456 password```
3. a file "term.ics" will be generated with your classes and finals, you can import it in your calendar

#### config:
you can change some variables in the config file like the last day in your semester, alarm times, and browser wait time
