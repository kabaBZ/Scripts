import schedule
import time
from AliCheckIn import aliCheck
from FreeIP import CrawlIP


schedule.every().day.at("10:00").do(aliCheck.run)

schedule.every().day.at("14:00").do(CrawlIP.run)


aliCheck.run()
CrawlIP.run()

print("初始任务执行完毕,开始运行计划任务")
while True:
    schedule.run_pending()
    time.sleep(1)
