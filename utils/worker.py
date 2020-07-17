class Worker:

    nextid = 1
    
    def __init__(self, servicetime = 0, numclients = 0):
        self.id = Worker.nextid
        Worker.nextid = Worker.nextid + 1
        self.servicetime = servicetime
        self.numclients = numclients

    def __repr__(self):
        return f"{self.id}"

if __name__ == "__main__":
    wlist = [Worker() for _ in range(5)]
    print(*wlist, sep="\n")
