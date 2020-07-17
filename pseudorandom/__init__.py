# PseudoRandom generators

from math import log, sqrt, exp, pi

class PseudoRandom():
    def __init__(self, fixed = 5167, temp = 3729):
        self.__fixed_multiplier__ = fixed
        self.__temporary_multiplier__ = temp

    def gener(self):
        res = self.__fixed_multiplier__ * self.__temporary_multiplier__ // 100 % 10000 / 10000
        self.__temporary_multiplier__ = self.__fixed_multiplier__ * self.__temporary_multiplier__ % 10000
        return res

    def exponential(self, mean):
        return mean * log(1/(1-self.gener()))

    def normal(self, mean, sdev):
        for _ in range(1000):
            b = mean + sdev*sqrt(2*log(100000/(sqrt(2*pi)*sdev)))
            a = mean - sdev*sqrt(2*log(100000/(sqrt(2*pi)*sdev)))
            ks1 = self.gener()
            ks2 = self.gener()
            ret = (b-a)*ks1+a
            ni = ks2/(sqrt(2*pi)*sdev)
            if ( (1/(sqrt(2*pi)*sdev))*exp(-((ret-mean)**2)/(2*(sdev**2))) >= ni ):
                return ret

    def discrete(self, problist):
        total = 0
        cumulative = [0]
        for p in problist:
            total = total + p
            cumulative.append(total)
        y = self.gener()
        for i in range(1,len(cumulative)):
            if y>=cumulative[i-1] and y<cumulative[i]:
                return i

if __name__  == "__main__":
    pr = PseudoRandom()
    for _ in range(10):
        print(pr.gener())
    for _ in range(10):
        print(pr.normal(10,2))
    for _ in range(10):
        print(pr.discrete([0.5, 0.3, 0.2]))

