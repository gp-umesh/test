"""
HBM_Monitor will monitor the system health on hourly basis
"""
import os
import time 
import datetime

health_folder_path = os.path.expanduser("~/.grampower/gp_concentrator/health")

def main():
    global health_folder_path
    while (True):    
        time.sleep(60)
        f = os.popen('monitor')
        content=f.read()
        timestamp = datetime.datetime.now()
        try:
            os.mkdir(health_folder_path + "/" + str(timestamp.date()))
        except OSError:
            pass
        filepath = (health_folder_path + "/" + str(timestamp.date()) +
                    "/" + str(timestamp.strftime("%H:%M:%S")) + ".log")
        file = open(filepath, "w")
        file.write(content)
        file.close()

if __name__ == "__main__":
    main()

