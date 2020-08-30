from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta, tzinfo
from apscheduler.schedulers.blocking import BlockingScheduler
from kasa import SmartPlug
import asyncio
import os
import pytz

IP_ADDRESS = "192.168.1.3"
scheduler = BlockingScheduler()
plug = SmartPlug(IP_ADDRESS)
asyncio.run(plug.update())
os.environ['TZ'] = 'US/Eastern'


def main():
    print("Adding Daily Job To Scheduler")
    # print(datetime.now(pytz.timezone('US/Eastern')))
    print(datetime.now())
    # Daily at 12:05 set the next set of sunset and sunrise times.
    # scheduler.add_job(schedule_on_and_off_time, 'cron', hour=0, minute=5)
    scheduler.add_job(schedule_on_and_off_time, 'cron', hour=16, minute=15)

    try:
        print("Scheduler Starting")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def schedule_on_and_off_time():
    print(f"Adding Todays Power")
    scheduler.add_job(power_on, 'date', run_date=get_sunset(), misfire_grace_time=300)
    scheduler.add_job(power_off, 'date', run_date=get_sunrise(), misfire_grace_time=300)


def power_on():
    print(f"Turning Lights On {datetime.now()}")
    asyncio.run(plug.turn_on())


def power_off():
    print(f"Turning Lights Off {datetime.now()}")
    asyncio.run(plug.turn_off())


def get_sunrise():
    tomorrows_sunrise = date.today() + timedelta(days=1)
    sunrise = _get_sun_information(tomorrows_sunrise).get("sunrise")
    print(f"Lights Should Turn Off At {sunrise}")
    return sunrise


def get_sunset():
    sunset = _get_sun_information(date.today()).get("sunset")
    print(f"Lights Should Turn On At {sunset}")
    return sunset


def _get_sun_information(day):
    lakewood = LocationInfo(name="Lakewood", region="United States", timezone="America/New_York", latitude=41.4724629,
                            longitude=-81.802996)
    return sun(lakewood.observer, date=day, tzinfo=lakewood.timezone)


if __name__ == '__main__':
    main()
