#!/usr/bin/env python

from csv import DictReader
from os import environ
from datetime import datetime, timedelta
from crontab import CronTab
from dotenv import load_dotenv


def get_today_prayers(file_name):
    # get today's prayer times
    today = datetime.now()
    today_str = today.strftime('%m/%d/%Y')
    with open(file_name, 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
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

def add_jumaah(prayer_times):
    if datetime.now().weekday() == 4:
        del prayer_times['dhuhr']
        prayer_times['jumaa1'] = parse_time('1:30 PM')
        prayer_times['jumaa2'] = parse_time('2:30 PM')
        prayer_times['jumaa3'] = parse_time('3:15 PM')

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

def add_cron_jobs(cron, prayer_times, before_command, after_command):
    
    def add_cron_job_with_time_diff(cron, time, time_diff, command):
        time += timedelta(minutes=time_diff)
        job = cron.new(command=command)
        job.hour.on(time.hour)
        job.minute.on(time.minute)

    for prayer, time in prayer_times.items():
        # before
        if prayer == 'maghrib' or prayer.startswith('jumaa'):
            timediff = -5
        else:
            timediff = -20
        add_cron_job_with_time_diff(cron, time, timediff, f'{before_command} {prayer}')

        # after
        if prayer != 'jumaa1' and prayer != 'jumaa2':
            add_cron_job_with_time_diff(cron, time, 40, f'{after_command} {prayer}')

def main():
    # load environment variables from .env file
    load_dotenv()
    # read csv file
    file_name = environ['CSV_FILE']
    # get prayer times for today
    prayers_row = get_today_prayers(file_name)
    # extract prayer times
    prayer_times = extract_prayer_times(prayers_row)
    # add Jumaah (in case today is Friday)
    add_jumaah(prayer_times)
    # print prayer times
    print_prayer_times(prayer_times)

    cron, before_command, after_command = init_cron()
    # add prayer times to cron
    add_cron_jobs(
        cron=cron, prayer_times=prayer_times,
        before_command=before_command, after_command=after_command
    )

    # add a final crontab at 3:00 AM to run this script again
    job = cron.new(command="cd /home/prayertimes && /usr/local/bin/python ./app.py")
    job.hour.on(3)
    job.minute.on(0)

    # write cron to disk
    cron.write()

main()
