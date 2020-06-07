import sqlite3
import statistics
import pandas as pd
import numpy
from datetime import datetime
from pytz import timezone
import os

# 'LINUX' or 'WINDOWS'
CURRENT_OS = "WINDOWS"

# load environment variables
from dotenv import load_dotenv
load_dotenv()

AM304_DB = os.getenv(f'AM304_DB_{CURRENT_OS}')
AM305_DB = os.getenv(f'AM305_DB_{CURRENT_OS}')

class DB:
    def get_eeg_data(self, animal, start_time, end_time):
        conn304 = sqlite3.connect(AM304_DB)
        conn305 = sqlite3.connect(AM305_DB)
        tz = timezone('US/Central')

        if animal == "AM304":
            conn = conn304
        elif animal == "AM305":
            conn = conn305

        start_epoch = tz.localize(datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        end_epoch = tz.localize(datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        cur = conn304.cursor()
        cur.execute("select * from eeg where time between {} and {};".format(start_epoch, end_epoch))
        sqlresult = cur.fetchall()
        cur.close()
        data = pd.DataFrame(sqlresult, columns=['Time', 'EEG1', 'EEG2'])
        data['Time'] = data['Time'].map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        return data

    def get_ss_data(self, animal, start_time, end_time):
        conn304 = sqlite3.connect(AM304_DB)
        conn305 = sqlite3.connect(AM305_DB)
        tz = timezone('US/Central')

        if animal == "AM304":
            conn = conn304
        elif animal == "AM305":
            conn = conn305

        start_epoch = tz.localize(datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        end_epoch = tz.localize(datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        cur = conn.cursor()
        cur.execute("select * from ss where time between {} and {};".format(start_epoch, end_epoch))
        sqlresult = cur.fetchall()
        cur.close()
        data = pd.DataFrame(sqlresult, columns=['Time', 'SS'])
        data['Time'] = data['Time'].map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        return data

    def get_temp_data(self, animal, start_time, end_time):
        conn304 = sqlite3.connect(AM304_DB)
        conn305 = sqlite3.connect(AM305_DB)
        tz = timezone('US/Central')

        if animal == "AM304":
            conn = conn304
        elif animal == "AM305":
            conn = conn305

        start_epoch = tz.localize(datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        end_epoch = tz.localize(datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        cur = conn.cursor()
        cur.execute("select * from temp where time between {} and {};".format(start_epoch, end_epoch))
        sqlresult = cur.fetchall()
        cur.close()
        data = pd.DataFrame(sqlresult, columns=['Time', 'Temp'])
        data['Time'] = data['Time'].map(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        print(type(data['Temp'][2]))
        return data

    def get_temp_stats(self, animal, start_time, end_time):
        conn304 = sqlite3.connect(AM304_DB)
        conn305 = sqlite3.connect(AM305_DB)
        tz = timezone('US/Central')

        if animal == "AM304":
            conn = conn304
        elif animal == "AM305":
            conn = conn305

        start_epoch = tz.localize(datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        end_epoch = tz.localize(datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")).timestamp()
        cur = conn.cursor()
        cur.execute("select * from temp where time between {} and {};".format(start_epoch, end_epoch))
        sqlresult = cur.fetchall()
        cur.close()
        data = pd.DataFrame(sqlresult, columns=['Time', 'Temp'])
        temps = [float(x) for x in data['Temp'] if str(x) != 'nan']
        stats = []
        stats.append({'Statistic': 'max', 'Value': max(temps)})
        stats.append({'Statistic': 'min', 'Value': min(temps)})
        stats.append({'Statistic': 'mean', 'Value': statistics.mean(temps)})
        stats.append({'Statistic': 'stdev', 'Value': statistics.stdev(temps)})
        stats.append({'Statistic': 'n', 'Value': len(temps)})

        return {'data': stats}