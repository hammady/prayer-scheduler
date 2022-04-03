#!/usr/bin/env python

from csv import DictReader
from os import environ
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from crontab import CronTab
from dotenv import load_dotenv


def read_csv_data(file_name, user_agent=None):
    print(f'Reading CSV file at: {file_name}')
    request = Request(file_name)
    if user_agent:
        request.add_header('User-Agent', user_agent)
    csv_data = urlopen(request).readlines()
    csv_data = [line.decode('utf-8-sig') for line in csv_data] # utf-8-sig removes BOM
    csv_reader = DictReader(csv_data)
    return csv_reader

def get_today_prayers(file_name, date_format, user_agent):
    # get today's prayer times
    today = datetime.now()
    today_str = today.strftime(date_format)
    print(f'Today: {today_str}')
    for row in read_csv_data(file_name, user_agent):
        row_date = datetime.strptime(row['Date'], date_format)
        row_date_str = row_date.strftime(date_format)
        if row_date_str == today_str:
            return row
    raise Exception(f'No prayer times found for {today_str}')

def parse_time(time_str, time_format):
    # parse prayer time string to datetime object
    return datetime.strptime(time_str, time_format)

def get_prayers_header(file_name, user_agent):
    for row in read_csv_data(file_name, user_agent):
        return row

def extract_prayer_times(prayer_times, prayers_header, time_format):
    # extract prayer times from csv row
    return {key: parse_time(prayer_times[header], time_format) \
        for key, header in prayers_header.items()}

def get_thresholds(file_name, time_format, user_agent):
    # get thresholds from csv file
    ret = dict()
    for row in read_csv_data(file_name, user_agent):
        ret[row['prayer']] = {
            'before': int(row['before']) if row['before'] else None,
            'after': int(row['after']) if row['after'] else None,
            'jumaa': parse_time(row['jumaa'], time_format) if row['jumaa'] else None
        }
    return ret

def add_jumaah(prayer_times, thresholds):
    if datetime.now().weekday() == 4:
        del prayer_times['dhuhr']
        for jumaa in ['jumaa1', 'jumaa2', 'jumaa3', 'jumaa4', 'jumaa5', 'jumaa6']:
            row = thresholds.get(jumaa)
            if row:
                prayer_times[jumaa] = row['jumaa']

def print_prayer_times(prayer_times):
    for prayer, time in prayer_times.items():
        print(f'{prayer}: {time.hour}:{time.minute}')

def init_cron():
    cron_user = environ['CRON_USER']
    cron = CronTab(user=cron_user)
    cron.remove_all()
    before_command = f'/home/{cron_user}/run-hooks.sh before'
    after_command = f'/home/{cron_user}/run-hooks.sh after'
    return (cron, before_command, after_command)

def add_cron_jobs(cron, prayer_times, thresholds, before_command, after_command):
    
    def add_cron_job_with_time_diff(cron, time, time_diff, command):
        time += timedelta(minutes=time_diff)
        job = cron.new(command=command)
        job.hour.on(time.hour)
        job.minute.on(time.minute)

    for prayer, time in prayer_times.items():
        timediff = thresholds[prayer].get('before', None)
        if timediff:
            add_cron_job_with_time_diff(cron, time, timediff, f'{before_command} {prayer}')
        timediff = thresholds[prayer].get('after', None)
        if timediff:
            add_cron_job_with_time_diff(cron, time, timediff, f'{after_command} {prayer}')

def main():
    # load environment variables from .env file
    load_dotenv()
    # read full csv file to get prayer times for today
    file_name = environ['FULL_CSV_URL']
    date_format = environ.get('DATE_FORMAT', '%m/%d/%Y')
    user_agent = environ.get('CSV_REQUESTER_USER_AGENT', None)
    prayers_row = get_today_prayers(file_name, date_format, user_agent)
    # read prayer header definitions from csv file
    file_name = environ['HEADER_CSV_URL']
    prayers_header = get_prayers_header(file_name, user_agent)
    # extract prayer times
    time_format = environ.get('TIME_FORMAT', '%I:%M %p')
    prayer_times = extract_prayer_times(prayers_row, prayers_header, time_format)
    # read before/after thresholds
    file_name = environ['THRESHOLDS_CSV_URL']
    thresholds = get_thresholds(file_name, time_format, user_agent)
    # add Jumaah (in case today is Friday)
    add_jumaah(prayer_times, thresholds)
    # print prayer times
    print_prayer_times(prayer_times)

    cron, before_command, after_command = init_cron()
    # add prayer times to cron
    add_cron_jobs(
        cron=cron, prayer_times=prayer_times, thresholds=thresholds,
        before_command=before_command, after_command=after_command
    )

    # add a final crontab at 3:00 AM to run this script again
    job = cron.new(command="cd /home/prayertimes && /usr/local/bin/python ./app.py >> /var/log/app.log 2>&1")
    job.hour.on(3)
    job.minute.on(0)

    # add a cron job that runs every minute to allow health checks
    cron.new(command="touch /tmp/healthz")

    # write cron to disk
    cron.write()

    # print all cron jobs
    for job in cron:
        print(job)

main()
