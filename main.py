from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from kasa import SmartPlug
import asyncio
import os

IP_ADDRESS = "192.168.1.3"
scheduler = BlockingScheduler()
plug = SmartPlug(IP_ADDRESS)
asyncio.run(plug.update())
os.environ['TZ'] = 'America/New_York'


def main():
    print(f"{datetime.now()} - Adding Daily Job To Scheduler")
    print(datetime.now())
    scheduler.add_job(schedule_on_and_off_time, 'cron', hour=18, minute=50, misfire_grace_time=300)

    try:
        print(f"{datetime.now()} - Scheduler Starting")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def schedule_on_and_off_time():
    print(f"{datetime.now()} - Adding Todays Power")
    scheduler.add_job(power_on, 'date', run_date=get_sunset(), misfire_grace_time=300)
    scheduler.add_job(power_off, 'date', run_date=get_sunrise(), misfire_grace_time=300)


def power_on():
    print(f"{datetime.now()} - Turning Lights On {datetime.now()}")
    asyncio.run(plug.turn_on())


def power_off():
    print(f"{datetime.now()} - Turning Lights Off {datetime.now()}")
    asyncio.run(plug.turn_off())


def get_sunrise():
    tomorrows_sunrise = date.today() + timedelta(days=1)
    sunrise = _get_sun_information(tomorrows_sunrise).get("sunrise")
    print(f"{datetime.now()} - Lights Should Turn Off At {sunrise}")
    return sunrise


def get_sunset():
    sunset = _get_sun_information(date.today()).get("sunset")
    print(f"{datetime.now()} - Lights Should Turn On At {sunset}")
    return sunset


def _get_sun_information(day):
    lakewood = LocationInfo(name="Lakewood", region="United States", timezone="America/New_York", latitude=41.4724629,
                            longitude=-81.802996)
    return sun(lakewood.observer, date=day, tzinfo=lakewood.timezone)


if __name__ == '__main__':
    main()
