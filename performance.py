import psutil
import time
import csv
import os
import pandas as pd
from pathlib import Path


timer = 60           
interval = 1         
run_no = 1
dark_reader = 0
start_time = 1

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_FILE = DATA_DIR / "performance_color_mutation_storm.csv"

with open(CSV_FILE, mode='a', newline='') as f:
    writer = csv.writer(f)

    # checking if the file has data written in it
    if os.path.getsize(CSV_FILE) == 0:
        writer.writerow(['run_no', 'dark_reader', 'timestamp', 'system_cpu_percent', 'brave_cpu_percent', 'brave_process_count'])
    else:
        df = pd.read_csv(CSV_FILE)
        run_no = (df.iloc[-1, 0]) + 1
        dark_reader = 1 - (df.iloc[-1, 1])
        start_time = df.iloc[-1, 2] + 1  

    # calling psutil.cpu_percent() so the first reading isnt 0 (skewed)
    psutil.cpu_percent(None)

    # recording data
    for sec in range(start_time, timer + start_time):
        # recording iteration start time
        start = time.time()

        # re/initializing parameters
        brave_cpu_perc = 0
        brave_proc_cnt = 0

        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'brave.exe':
                brave_cpu_perc += proc.cpu_percent()
                brave_proc_cnt += 1
        writer.writerow([run_no, dark_reader, sec, psutil.cpu_percent(None) / psutil.cpu_count(), (brave_cpu_perc / psutil.cpu_count()), brave_proc_cnt])
        print(f'{brave_proc_cnt} brave processes recorded at {sec} second')
                
        # making the whole iter take {interval} seconds or 0 if the whole itertion takes more than a second
        time.sleep(max(0, interval - (time.time() - start)))

