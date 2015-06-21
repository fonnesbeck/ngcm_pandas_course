from datetime import datetime

import pandas as pd
import numpy as np

try:
    from scipy.constants import F2C
except ImportError:  # no scipy installed
    def F2C(f):
        return (np.array(f) - 32)/1.8

dta = pd.read_table("http://academic.udayton.edu/kissock/http/"
                    "Weather/gsod95-current/NYNEWYOR.txt", sep=" *",
                    names=["month", "day", "year", "temp"])


def to_season(day_month):
    day, month = day_month
    year = 2012
    doy = datetime(year, month, day).timetuple().tm_yday

    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else

    if doy in spring:
        return 'Spring'
    elif doy in summer:
        return 'Summer'
    elif doy in fall:
        return 'Fall'
    else:
        return 'Winter'

dta["season"] = dta[['day', 'month']].apply(to_season, axis=1)
dta["tempc"] = F2C(dta.temp)
dta.to_csv("../data/weather_nyc.csv", index=False)
