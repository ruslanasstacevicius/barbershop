
def hourmin(minutes):
    return "{:02d}".format(minutes // 60) + ":" + "{:02d}".format(minutes % 60)


class Event:

    MESSAGES = {
        1: "WORKDAY {0} STARTED",
        2: "Arrival of {0} client(s). Total clients so far: {1}",
        3: "Client {0} starts being served by worker {1}. Service type: {2} duration: {3} finish time: {4}. Worker will work: {5}",
        4: "Client {0} goes to row. Row lenght becomes: {1}",
        5: "Client {0} served. Worker {1} is free. Served so far: {2}",
        6: "Client {0} leaves row. Waiting time: {1} row lenght: {2}. Total time in row: {3}. Total clients in row: {4}",
        7: "Client {0} leaves unserved. Total unserved so far: {1}",
        8: "OFFICIAL WORKDAY {0} END",
    }

    def __init__(self, tm, tp, data):
        self.tm = tm
        self.tp = tp
        self.data = data

    def __repr__(self):
        timetype = hourmin(self.tm) + " - " + str(self.tp) + " - "
        textline = timetype + self.MESSAGES[self.tp].format(*self.data)
        return textline


if (__name__ == "__main__"):
    ev = Event(420, 1, (1,))
    print(ev)
