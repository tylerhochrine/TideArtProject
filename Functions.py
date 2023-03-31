from datetime import datetime, timedelta
import requests
import time


def before_next_tide(pdtmNextTideTime):
    dtmNow = datetime.now().replace(second=0, microsecond=0)

    return dtmNow < datetime.strptime(pdtmNextTideTime['t'], '%Y-%m-%d %H:%M')


def get_current_tide():
    dtmToday = datetime.today().date().strftime('%Y%m%d')

    noaa_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?&end_date={dtmToday}&range=12&station=8443970" \
               "&product=predictions&datum=STND&time_zone=lst_ldt&interval=hilo&units=english&format=json "
    response = requests.get(noaa_url)

    return response.json()['predictions'][-1]


def get_tomorrow_tides():
    dtmTomorrow = datetime.now() + timedelta(1)
    dtmTomorrow = dtmTomorrow.strftime('%Y%m%d')

    noaa_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={dtmTomorrow}&end_date={dtmTomorrow}" \
               f"&station=8443970&product=predictions&datum=STND&time_zone=lst_ldt&interval=hilo&units=english&format" \
               f"=json "
    response = requests.get(noaa_url)

    return response.json()['predictions']


def next_tide(pdctTides):
    dtmNextTide = pdctTides[0]
    pdctTides = pdctTides[1:]

    return dtmNextTide, pdctTides


# function to get the current water level from the API
# ~6-7 minute delay due to NOAA record keeping
# dtmTime will be 0 if not run before, otherwise it will be equal to the most recent water level record
# function will sleep until the current minute is divisible by 6
# data will only return once NOAA has updated the data
def get_current_water_level(dtmTime):
    noaa_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=8443970&product" \
               "=water_level&datum=STND&time_zone=lst_ldt&units=english&format=json "

    if dtmTime != 0:
        dtmNow = datetime.today()

        # remaining minutes and seconds until the minute is divisible by 6
        intSleepMinutes = 5 - (dtmNow.minute % 6)
        intSleepSeconds = 60 - dtmNow.second

        time.sleep(intSleepMinutes * 60 + intSleepSeconds)

        response = requests.get(noaa_url)

        # loops until the api updates the data
        while response.json()['data'][0]['t'] == dtmTime:
            # sleeps for 5 seconds if data is still equal to previous data so as to not call API too much
            time.sleep(5)

            response = requests.get(noaa_url)

    # runs immediately if not run before
    else:
        response = requests.get(noaa_url)

    dtmTime = response.json()['data'][0]['t']
    dblHeight = response.json()['data'][0]['v']

    return dtmTime, dblHeight
