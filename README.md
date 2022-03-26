# prayer-scheduler

Run arbitrary scripts based on prayer times loaded from CSV file.
All scripts located in `before-hooks.d`/`after-hooks.d` will be executed
before/after the prayer Iqama times by a configurable threshold.
Thresholds are configured in a sepparate CSV file.
For any common configuration for the hooks, create scripts as necessary
in the `hooks-config.d` directory. These will be sourced by the application.

The current hooks send BUTT commands to set the stream title.
They also enable stream signal detection (in the before hook) and disable it (in the after hook).

## Build

```bash
docker build . -t prayer-scheduler:1
```

Default time zone is set to `Canada/Eastern`. It can be overriden by supplying
a build argument to the docker build:

```bash
docker build . --build-arg TIMEZONE=America/New_York -t prayer-scheduler:1
```

Time zones are important for the prayer times to be correct.
All times in the CSV files are assumed to match the same time zone.
For a list of all timezones, see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Configure

Environment variables can be stored in `.env` which will be loaded automatically.
All defaults for the below environment variables can be found in this file.
The format of the environment variables is: File path (file://) or URL (https://).

1. `FULL_CSV_URL`: Main CSV file to load.
This CSV should have all year timetable as rows, with the five prayer times as columns.
1. `HEADER_CSV_URL`: CSV file mapping prayer names to column headers in the previous file.
This file should have the standard prayer names as its header row, and the column names in
the previous file as its first row. Following rows are ignored.
1. `THRESHOLDS_CSV_URL` Thresholds CSV file to load. This CSV should have all prayers as rows,
with the following column names in the header:
    1. prayer (fajr, dhuhr, asr, maghrib, ishaa, jumaa1, jumaa2, ...)
    1. before (minutes before the iqama time of the prayer to trigger the before hooks)
    1. after (minutes after the iqama time of the prayer to trigger the after hooks)
    1. jumaa (if the prayer is juma'a, the jumaa time)
## Run

```bash
docker run -d \
    --name=prayer-scheduler \
    --restart always \
    prayer-scheduler:1
```

## Health Check

The Dockerfile contains a health check that will run every 20 seconds and will
exit with a non-zero exit code if the minutely cron job has not been run for
the last 5 minutes, which denotes the cron scheduler is malfunctioning.
