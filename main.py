import random
import statistics

class SignalGenerator:
    def __init__(self, minval, maxval):
        self.signals = []
        self.min_val = minval
        self.max_val = maxval
        self.iter = 0

    def print_signals(self):
        print(self.signals)    

    def generate_signal(self):
        for i in range(self.max_val):
            self.signals.append(i)
        for i in range(self.max_val):
            self.signals.append(self.max_val-i)
        print(f"GENERATED: {self.signals}")
    
    def get_data_stream(self, data_num):
        temp = self.iter
        self.iter = (self.iter + data_num) % len(self.signals)
        if self.iter > len(self.signals):
            return self.signals[0]
        return self.signals[temp:self.iter] # ?


class Sensor:
    def __init__(self):
        self.delta = 1
        self.signal = 0
        self.distorted_signal = 0

    def read_input(self, signal):
        self.signal = signal

    def distort_signal(self):
        dist = random.randint(-self.delta, self.delta)
        self.distorted_signal = self.signal + dist
        
    def get_output(self):
        return self.distorted_signal


class Comparator:
    def  __init__(self):
        self.readings = []
        self.vote_median = 0

    def median_voting(self):
        self.vote_median = statistics.median(self.readings)
    
    def readInput(self, readings):
        self.readings = readings
    
    def getOutput(self):
        print(f"sensor readings: {self.readings}")
        print(f"vote: {self.vote_median}")
        return self.vote_median
    

def main():
    signal_generator = SignalGenerator(0,50)
    signal_generator.generate_signal()

    sensor1 = Sensor()
    sensor2 = Sensor()
    sensor3 = Sensor()
    comparator = Comparator()

    number_of_data = 99
    for i in range(number_of_data):
        data_stream = signal_generator.get_data_stream(1)

        sensor1.read_input(data_stream[0])
        sensor1.distort_signal()

        sensor2.read_input(data_stream[0])
        sensor2.distort_signal()

        sensor3.read_input(data_stream[0])
        sensor3.distort_signal()

        comparator.readInput([sensor1.get_output(), sensor2.get_output(), sensor3.get_output()])
        comparator.median_voting()
        comparator.getOutput()

main()