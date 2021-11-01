# prayer-schedule

Run arbitrary scripts based on prayer times loaded from CSV file.
All scripts located in `before-hooks.d` will be executed before the prayer
Iqama times by 20 minutes (5 minutes for Maghrib and Juma'as).
All scripts located in `after-hooks.d` will be executed after the prayer
Iqama times by 40 minutes. This applies also to the final Juma'a, but not the
eariler ones.

The current hooks set the stream title located in the mounted volume on the host.
They also switch the mic on (in the before hook) and off (in the after hook).

## Build

```bash
docker build . -t prayer-scheduler:1
```

## Configure

1. `CSV_FILE` environment variable: Path of CSV file to load, default: `prayers-timetable.csv`
1. The CSV above should have the following column names in the header: 
    1. Fajr Iqaamah 1
    1. Zhuhr Iqaamah
    1. 'Asr Iqaamah
    1. Maghrib
    1. Ishaa Iqaamah 1
1. Time zone is set to `Canada/Eastern`, can be overriden from the `Dockerfile`
1. Jumaa prayers schedule can be changed in `add_jumaah` function in `app.py` 

## Run

```bash
docker run -d \
    --name=prayer-scheduler \
    -v c:/Users/User/Documents/butt:/stream-config \
    --restart always \
    prayer-scheduler:1
```
