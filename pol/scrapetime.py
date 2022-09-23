import datetime
import os

def pol():
    exec(open("/home/daniel/shared/pol/pol-index.py").read())
    dt = str(datetime.datetime.now().strftime("%H:%M"))
    print("/pol/ done " + dt)

import time
import schedule
from schedule import every, run_pending

schedule.every(5).minutes.do(pol)

while True: 
    run_pending()
    time.sleep(1)
