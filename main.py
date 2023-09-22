import schedule
import time
from AliCheckIn import aliCheck
from FreeIP import CrawlIP


schedule.every().day.at("10:00").do(aliCheck.run)

schedule.every().day.at("14:00").do(CrawlIP.run)

while True:
    schedule.run_pending()
    time.sleep(1)
