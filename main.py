import subprocess
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# TODO
# Add data parametere to pass to getter, so it gets the last 10 minutes of tweets

# SINCE is the x minutes since result will be fetched UNTIL UNTIL
SINCE = 5
UNTIL = 0

SCRIPT_LIST = ['getter.py', 'analyzer.py', 'adder.py', 'cleaner.py']

def main():
    for script in SCRIPT_LIST:
        subprocess.call(['python', script])
        print("Finished:" + script)


sched = BlockingScheduler()

# Schedule job_function to be called every x time
sched.add_job(main, 'interval', minutes=SINCE-UNTIL)

if __name__ == "__main__":
    sched.start()