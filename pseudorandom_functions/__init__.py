# pseudorandom generators

from math import log, sqrt, exp, pi

def pseudorandom():
    fixed_multiplier, temporary_multiplier = 5167, 3729
    while True:
        yield fixed_multiplier * temporary_multiplier // 100 % 10000 / 10000
        temporary_multiplier = fixed_multiplier * temporary_multiplier % 10000

pseudorandom_generator = pseudorandom()

def gener():
    return pseudorandom_generator.__next__()

def exponential(mean):
    return mean * log(1/(1-gener()))

def normal(mean, sdev):
    for _ in range(1000):
        b = mean + sdev*sqrt(2*log(100000/(sqrt(2*pi)*sdev)))
        a = mean - sdev*sqrt(2*log(100000/(sqrt(2*pi)*sdev)))
        ks1 = gener()
        ks2 = gener()
        ret = (b-a)*ks1+a
        ni = ks2/(sqrt(2*pi)*sdev)
        if ( (1/(sqrt(2*pi)*sdev))*exp(-((ret-mean)**2)/(2*(sdev**2))) >= ni ):
            return ret

def discrete(problist):
    total = 0
    cumulative = [0]
    for p in problist:
        total = total + p
        cumulative.append(total)
    y = gener()
    for i in range(1,len(cumulative)):
        if y>=cumulative[i-1] and y<cumulative[i]:
            return i

if __name__  == "__main__":
    for _ in range(10):
        print(gener())
    for _ in range(10):
        print(normal(10,2))
    for _ in range(10):
        print(discrete([0.5, 0.3, 0.2]))

