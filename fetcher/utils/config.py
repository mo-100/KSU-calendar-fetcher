from configparser import ConfigParser
import datetime
import json


cfg = ConfigParser()
cfg.read('config.ini')


LAST_STUDY_DAY = datetime.datetime.fromisoformat(cfg['semester']['LastStudyDay'])
if 'FirstStudyDay' in cfg['semester']:
    FIRST_STUDY_DAY = datetime.datetime.fromisoformat(cfg['semester']['FirstStudyDay'])
else:
    FIRST_STUDY_DAY = datetime.datetime.now()
DRIVER_WAIT_TIME = int(cfg['scraper.settings']['WaitTime'])
CLASS_ALARM = int(cfg['alarm.settings']['ClassAlarmBefore'])
FINAL_ALARM = int(cfg['alarm.settings']['FinalAlarmBefore'])

with open('replace.json', 'r', encoding='utf-8') as f:
    replaces = json.load(f)
    REPLACE_LIST: list[tuple[str, str]] = [(r['from'], r['to']) for r in replaces]