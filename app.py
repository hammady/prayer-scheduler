#!/usr/bin/env python

from csv import DictReader
from os import environ
from datetime import datetime, timedelta
from urllib.request import urlopen
from crontab import CronTab
from dotenv import load_dotenv


def read_csv_data(file_name):
    print(f'Reading CSV file at: {file_name}')
    csv_data = urlopen(file_name).readlines()
    csv_data = [line.decode('utf-8') for line in csv_data]
    csv_reader = DictReader(csv_data)
    return csv_reader

def get_today_prayers(file_name):
    # get today's prayer times
    today = datetime.now()
    today_str = today.strftime('%m/%d/%Y')
    for row in read_csv_data(file_name):
        row_date = datetime.strptime(row['Date'], '%m/%d/%Y')
        row_date_str = row_date.strftime('%m/%d/%Y')
        if row_date_str == today_str:
            return row
    raise Exception(f'No prayer times found for {today_str}')

def parse_time(time_str):
    # parse prayer time string to datetime object
    return datetime.strptime(time_str, "%I:%M %p")

def extract_prayer_times(prayer_times):
    # extract prayer times from csv row
    return {
        'fajr': parse_time(prayer_times['Fajr Iqaamah 1']),
        'dhuhr': parse_time(prayer_times['Zhuhr Iqaamah']),
        'asr': parse_time(prayer_times['\'Asr Iqaamah']),
        'maghrib': parse_time(prayer_times['Maghrib']),
        'isha': parse_time(prayer_times['Ishaa Iqaamah 1'])
    }

def get_thresholds(file_name):
    # get thresholds from csv file
    ret = dict()
    for row in read_csv_data(file_name):
        ret[row['prayer']] = {
            'before': int(row['before']) if row['before'] else None,
            'after': int(row['after']) if row['after'] else None,
            'jumaa': parse_time(row['jumaa']) if row['jumaa'] else None
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
    # read full csv file
    file_name = environ['FULL_CSV_URL']
    # get prayer times for today
    prayers_row = get_today_prayers(file_name)
    # extract prayer times
    prayer_times = extract_prayer_times(prayers_row)
    # read before/after thresholds
    file_name = environ['THRESHOLDS_CSV_URL']
    thresholds = get_thresholds(file_name)
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
    job = cron.new(command="cd /home/prayertimes && /usr/local/bin/python ./app.py")
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
