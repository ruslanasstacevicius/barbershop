
from pseudorandom import PseudoRandom
from utils.event import hourmin, Event
from utils.worker import Worker

def fill_events(elist, ev):
    if (len(elist) == 0):
        return [ev]
    for i in (range(len(elist))):
        if ev.tm < elist[i].tm or (ev.tm == elist[i].tm and ev.tp == 5): 
            break
    if (ev.tm > elist[i].tm) or (ev.tm == elist[i].tm and ev.tp == 2):
        i = i + 1
    return elist[:i] + [ev] + elist[i:] 

def fill_workers(wlist, w):
    if (len(wlist) == 0):
        return [w]
    for i, win in enumerate(wlist):
        if w.servicetime < win.servicetime:
            break
    if w.servicetime >= win.servicetime:
        i = i + 1
    return wlist[:i] + [w] + wlist[i:]

# setup
pr = PseudoRandom()

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

EVENTS = []
ROW = []
WORKERS = [Worker() for _ in range(num_of_workers)]

time = start_hour*60
ncl = 0
N = 0
Nserved = 0
Nwaited = 0
Twaited = 0

EVENTS = [] 
ev = Event(time, 1, (1,))
EVENTS = fill_events(EVENTS, ev)
ev = Event(last_minute, 8, (1,))
EVENTS = fill_events(EVENTS, ev)

t = time + int(round(pr.exponential(clients_arrival_interval)))
ev = Event(t, 2, (0,0))
EVENTS = fill_events(EVENTS, ev)

while EVENTS:

    ev = EVENTS.pop(0)
    time = ev.tm

    if ev.tp in [1,8]:
        print(ev)

    if ev.tp == 2:
        ncl = pr.discrete(prob_incoming_clients) 
        ev.data = (ncl, N+ncl)
        print(ev)
        for _ in range(ncl):
            N = N + 1
            if WORKERS:
                servtype = pr.discrete(prob_service_type)
                duration = round(pr.normal(avg_service_duration[servtype-1], stdev_service_duration[servtype-1]))
                worker = WORKERS.pop(0)
                worker.servicetime = worker.servicetime + duration
                worker.numclients = worker.numclients + 1
                ev = Event(time+duration, 5, (N, worker))
                EVENTS = fill_events(EVENTS, ev)
                info = (N, worker, servtype, duration, hourmin(t+duration), worker.servicetime)
                ev = Event(time, 3, info)
            else:
                if len(ROW) < maxrow:
                    ROW.append((t,N))
                    ev = Event(t, 4, (N,len(ROW)))
                else:
                    info = (N,N-Nserved-len(ROW)-num_of_workers+len(WORKERS))
                    ev = Event(t, 7, info)
            print(ev)
        t = time + int(round(pr.exponential(clients_arrival_interval)))
        if t < last_minute:
            ev = Event(t, 2, (0,0))
            EVENTS = fill_events(EVENTS, ev)

    if ev.tp == 5:
        Nserved = Nserved + 1
        ev.data = ev.data + (Nserved,)
        print(ev)
        WORKERS = fill_workers(WORKERS,ev.data[1])
        if ROW:
            waitstart, rowclient  = ROW.pop(0)
            Nwaited = Nwaited + 1
            Twaited = Twaited + (time - waitstart)
            info = (rowclient, (time - waitstart), len(ROW), Twaited, Nwaited)
            ev = Event(time, 6, info)
            print(ev)

            servtype = pr.discrete(prob_service_type)
            duration = round(pr.normal(avg_service_duration[servtype-1], stdev_service_duration[servtype-1]))
            worker = WORKERS.pop(0)
            worker.servicetime = worker.servicetime + duration
            worker.numclients = worker.numclients + 1
            ev = Event(time+duration, 5, (rowclient, worker))
            EVENTS = fill_events(EVENTS,ev)
            info = (rowclient, worker, servtype, duration, hourmin(time+duration), worker.servicetime)
            ev = Event(time, 3, info)
            print(ev)
