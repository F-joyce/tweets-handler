import subprocess
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# TODO
# Add data parametere to pass to getter, so it gets the last 10 minutes of tweets


SCRIPT_LIST = ['getter.py', 'analyzer.py', 'adder.py', 'cleaner.py']

def main():
    for script in SCRIPT_LIST:
        subprocess.call(['python', script])
        print("Finished:" + script)


sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(main, 'interval', minutes=2)

sched.start()

if __name__ == "__main__":
    sched.start()