import schedule
import time
from AliCheckIn import aliCheck
from FreeIP import CrawlIP


schedule.every().day.at("10:00").do(aliCheck.run)

schedule.every().day.at("10:46:20").do(CrawlIP.run)

while True:
    schedule.run_pending()
