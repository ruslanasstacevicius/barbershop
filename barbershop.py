
from math import log, sqrt, exp, pi
from pseudorandom import pseudorandom

pr = pseudorandom()

# helper functions

def hourmin(minutes):
    return "{:02d}".format(minutes // 60) + ":" + "{:02d}".format(minutes % 60)

def printlog(e):
    timetype = hourmin(e["tm"]) + " - " + str(e["tp"]) + " - "
    textline = timetype + e["msg"].format(*e["data"])
    print(textline)
    return None

def fillEVENTS(elist, ev):
    if (len(elist) == 0):
        return [ev]
    for i in (range(len(elist))):
        if ev["tm"] < elist[i]["tm"] or (ev["tm"] == elist[i]["tm"] and ev["tp"] == 5): 
            break
    if (ev["tm"] > elist[i]["tm"]) or (ev["tm"] == elist[i]["tm"] and ev["tp"] == 2):
        i = i + 1
    return elist[:i] + [ev] + elist[i:] 

def fillWORKERS(wlist,wtm,w):
    if (len(wlist) == 0):
        return [w]
    for i, win in enumerate(wlist):
        if wtm[w-1] < wtm[win-1]: 
            break
    if wtm[w-1] >= wtm[win-1]:
        i = i + 1
    return wlist[:i] + [w] + wlist[i:]

# setup

start_hour = 7
work_hours = 8
last_minute = (work_hours+start_hour)*60

prob_incoming_clients = [0.71, 0.23, 0.05, 0.01]

prob_service_type = [0.5, 0.4, 0.1]
avg_service_duration = [12, 15, 25]
stdev_service_duration = [0.8, 1.0, 3.0]

num_of_workers = 4
N = 0
clients_arrival_interval = 5
maxrow = 8
workedtime = [0] * num_of_workers

EVENTS = []
ROW = []
WORKERS = list(range(1, num_of_workers+1))
#print(workedtime, WORKERS)

time = start_hour*60
ncl = 0
N = 0
Nserved = 0
Nwaited = 0
Twaited = 0

EVENTS = [] 
ev = {"tm": time, "tp": 1, "data": (1,), "msg": "WORKDAY {0} STARTED"}
EVENTS = fillEVENTS(EVENTS, ev)
ev = {"tm": last_minute, "tp": 8, "data": (1,), "msg": "OFFICIAL WORKDAY {0} END"}
EVENTS = fillEVENTS(EVENTS, ev)

t = time + int(round(pr.exponential(clients_arrival_interval)))
ev = {"tm": t, "tp": 2, "data": (0,0), "msg": "Arrival of {0} client(s). Total clients so far: {1}"}
EVENTS = fillEVENTS(EVENTS, ev)

while EVENTS:
    #print(EVENTS)
    #print(WORKERS,workedtime)
    ev = EVENTS.pop(0)
    time = ev["tm"]

    if ev["tp"] in [1,8]:
        printlog(ev)

    if ev["tp"] == 2:
        ncl = pr.discrete(prob_incoming_clients) 
        ev["data"] = (ncl, N+ncl)
        printlog(ev)
        for _ in range(ncl):
            N = N + 1
            if WORKERS:
                servtype = pr.discrete(prob_service_type)
                duration = round(pr.normal(avg_service_duration[servtype-1], stdev_service_duration[servtype-1]))
                worker = WORKERS.pop(0)
                workedtime[worker-1] = workedtime[worker-1] + duration
                ev = {"tm": time+duration, "tp": 5, "data": (N, worker), "msg" : "Client {0} served. Worker {1} is free. Served so far: {2}"}
                EVENTS = fillEVENTS(EVENTS,ev)
                info = (N, worker, servtype, duration, hourmin(t+duration), workedtime[worker-1] )
                msg = "Client {0} starts being served by worker {1}. Service type: {2} duration: {3} finish time: {4}. Worker will work: {5}"
                ev = {"tm": time, "tp": 3, "data": info, "msg": msg}
            else:
                if len(ROW) < maxrow:
                    ROW.append((t,N))
                    ev = {"tm": t, "tp": 4, "data": (N,len(ROW)), "msg": "Client {0} goes to row. Row lenght becomes: {1}"}
                else:
                    info = (N,N-Nserved-len(ROW)-num_of_workers+len(WORKERS))
                    msg = "Client {0} leaves unserved. Total unserved so far: {1}"
                    ev = {"tm": t, "tp": 7, "data": info, "msg": msg}
            printlog(ev)
        t = time + int(round(pr.exponential(clients_arrival_interval)))
        if t < last_minute:
            ev = {"tm": t, "tp": 2, "data": (0,0), "msg": "Arrival of {0} client(s). Total clients so far: {1}."}
            EVENTS = fillEVENTS(EVENTS, ev)

    if ev["tp"] == 5:
        Nserved = Nserved + 1
        ev["data"] = ev["data"] + (Nserved,)
        printlog(ev)
        #WORKERS.append(ev["data"][1])
        WORKERS = fillWORKERS(WORKERS,workedtime,ev["data"][1])
        if ROW:
            waitstart, rowclient  = ROW.pop(0)
            Nwaited = Nwaited + 1
            Twaited = Twaited + (time - waitstart)
            info = (rowclient, (time - waitstart), len(ROW), Twaited, Nwaited)
            msg = "Client {0} leaves row. Waiting time: {1} row lenght: {2}. Total time in row: {3}. Total clients in row: {4}"
            ev = {"tm": time, "tp": 6, "data": info, "msg": msg}
            printlog(ev)

            servtype = pr.discrete(prob_service_type)
            duration = round(pr.normal(avg_service_duration[servtype-1], stdev_service_duration[servtype-1]))
            worker = WORKERS.pop(0)
            workedtime[worker-1] = workedtime[worker-1] + duration
            ev = {"tm": time+duration, "tp": 5, "data": (rowclient, worker), "msg" : "Client {0} served. Worker {1} is free. Total served clients: {2}"}
            EVENTS = fillEVENTS(EVENTS,ev)
            info = (rowclient, worker, servtype, duration, hourmin(time+duration), workedtime[worker-1] )
            msg = "Client {0} starts being served by worker {1}. Service type: {2} duration: {3} finish time: {4}. Worker will work: {5}"
            ev = {"tm": time, "tp": 3, "data": info, "msg": msg}
            printlog(ev)

