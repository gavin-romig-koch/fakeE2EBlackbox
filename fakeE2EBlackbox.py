from prometheus_client import start_http_server, Gauge, Counter, Summary
import random
import time
import datetime

INSIGHTS_E2E_UP = Gauge('insights_e2e_blackbox_up', 'Blackbox e2e works')
INSIGHTS_E2E_SUCCESS = Summary('insights_e2e_blackbox_success', 'Blackbox e2e success')

starttime = datetime.datetime.now()

def process_request():
    scale = 100
    r = random.random()
    kilobytes = r*scale
    # seconds = (r * 3) + random[-r/3,+r/3)
    # seconds = (r * 2) + random[0,r*2]
    seconds = (r * 2) + (random.random() * (r * 2))
    print("sleeping for ",seconds)
    time.sleep(seconds)

    totalupseconds = (datetime.datetime.now()-starttime).total_seconds()
    print("total up seconds ",totalupseconds)

    if totalupseconds < (1.5 * 60):
        downaverage = 0.07
    elif totalupseconds < (3.5 * 60):
        downaverage = 1.1
    else:
        downaverage = 0.06
    print("downaverage ",downaverage)

    if random.random() < downaverage:
        print("down")
        INSIGHTS_E2E_UP.set(0)
        INSIGHTS_E2E_SUCCESS.observe(0)
    else:
        print("up")
        INSIGHTS_E2E_UP.set(1)
        INSIGHTS_E2E_SUCCESS.observe(1)
        
        
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request()
        #print("sleeping for ", 60)
        #time.sleep(60)
