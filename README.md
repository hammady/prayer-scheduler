# prayer-scheduler

Run arbitrary scripts based on prayer times loaded from CSV file.
All scripts located in `before-hooks.d`/`after-hooks.d` will be executed
before/after the prayer Iqama times by a configurable threshold.
Thresholds are configured in a sepparate CSV file.

The current hooks set the stream title located in the mounted volume on the host.
They also switch the mic on (in the before hook) and off (in the after hook).

## Build

```bash
docker build . -t prayer-scheduler:1
```

## Configure

Environment variables can be stored in `.env` which will be loaded automatically.

1. `FULL_CSV_URL` environment variable: File path (file://) or URL (https://) of main CSV file to load,
default: `file:///home/prayertimes/prayers-timetable.csv`
1. The CSV above should have all year timetable as rows, with the following column names in the header:
    1. Fajr Iqaamah 1
    1. Zhuhr Iqaamah
    1. 'Asr Iqaamah
    1. Maghrib
    1. Ishaa Iqaamah 1
1. `THRESHOLDS_CSV_URL` environment variable: File path (file://) or URL (https://)  of thresholds CSV file to load,
default: `file:///home/prayertimes/thresholds.csv`
1. The CSV above should have all prayers as rows, with the following column names in the header:
    1. prayer (fajr, dhuhr, asr, maghrib, ishaa, jumaa1, jumaa2, ...)
    1. before (minutes before the iqama time of the prayer to trigger the before hooks)
    1. after (minutes after the iqama time of the prayer to trigger the after hooks)
    1. jumaa (if the prayer is juma'a, the jumaa time)
1. Time zone is set to `Canada/Eastern`, can be overriden from the `Dockerfile`

## Run

```bash
docker run -d \
    --name=prayer-scheduler \
    -v c:/Users/User/Documents/butt:/stream-config \
    --restart always \
    prayer-scheduler:1
```
