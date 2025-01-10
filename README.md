# KSU Calendar Fetcher
Automatically fetch your KSU (King Saud University) class schedule and final exam dates from Edugate and generate an iCalendar file that you can import into any calendar application.
## Features
- 🔄 Automatic login to KSU Edugate
- 📅 Extracts regular class schedules
- 📝 Captures final exam schedules
- 🗓️ Generates standard iCalendar (.ics) file
- 🌐 Multi-browser support (Firefox, Chrome, Edge, Safari)
- ⏰ Configurable reminder notifications
- ⚙️ Customizable settings through config file

## Prerequisites
Before you begin, ensure you have:
- Python 3.11 or higher installed
- A supported web browser (Firefox, Chrome, Edge, or Safari)
- Valid KSU Edugate credentials
- Internet connection

## Installation
1. Clone this repository:
```bash
git clone https://github.com/M01010/KSU-Calendar-Fetcher.git
cd KSU-Calendar-Fetcher
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Basic Usage
Run the script using the following command:
```bash
python main.py {browser} {student_id} {password}
```
Replace the parameters with your information:
- `{browser}`: Your preferred browser (firefox, chrome, edge, safari)
- `{student_id}`: Your KSU student ID
- `{password}`: Your Edugate password

Example:
```bash
python main.py chrome 444123456 password
```

### Configuration
You can customize various settings in the `config.ini` file

### Generated Calendar
The script will create a file named `term.ics` containing your schedule. You can import this file into various calendar applications:
- Google Calendar
  1. Open Google Calendar
  2. Click the '+' next to 'Other calendars'
  3. Select 'Import'
  4. Choose the generated .ics file
- Apple Calendar
  1. Open Calendar app
  2. File → Import
  3. Select the .ics file
- Microsoft Outlook
  1. Open Outlook
  2. File → Open & Export → Import/Export
  3. Select 'Import an iCalendar (.ics) file'

## Extending to Other Universities
This project is designed with extensibility in mind and can be adapted to work with other university portals. To extend the code for your university:

- Create a New University Class
- Inherit from the base scraper class
- create new classes for your finals and classes with whatever variables you want
- Implement schedule extraction method specific to your university's portal

Example structure for adding a new university:
```python
class NewUniversityScraper(CalendarScraper):
    def get_events(self) -> list[CalendarEvent]:
        # Implement schedule extraction for your university
        pass


class NewUniversityClass(CalendarEvent):
    def make_event(self) -> Event:
        # Implement how you want the event to appear in the calendar
        pass

class NewUniversityFinal(CalendarEvent):
    def make_event(self) -> Event:
        # Implement how you want the event to appear in the calendar
        pass
```

If you successfully extend this project to another university, consider contributing back to help other students!

## Security Notes
- Your credentials are never stored and are only used to log in to Edugate
- The script runs locally on your machine and doesn't send data to any third parties

## Limitations
- May need updates if Edugate's interface changes

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate comments.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This tool is unofficial and not affiliated with King Saud University. Use at your own risk.
