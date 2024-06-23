import numpy as np
import random
import statistics
from collections import Counter
from sklearn.linear_model import LinearRegression

# Generator sygnału
class SignalGenerator:
    def __init__(self, samples, periods):
        self.signals = []
        self.samples = samples  # Liczba probek w okresie
        self.periods = periods  # Liczba okresów

    # Generowanie próbek sygnału f(x)=50sin+50 , ZWf = [0;100]
    def generate_signal(self):
        # Obliczanie częstotliwości próbkowania
        sampling_rate = self.samples / (2 * np.pi)
        # Tablica wartości czasu
        time = np.linspace(0, self.samples / sampling_rate, self.samples * self.periods)

        self.signals = 50 * np.sin(time) + 50

    def set_signals(self, signals):
        self.signals = signals

    def get_signal(self):
        return self.signals


# Sensor odczytujący sygnał
class Sensor:
    def __init__(self, delta):
        self.delta = delta
        self.signal = 0
        self.distorted_signal = 0
        reliabilities = [0.95, 0.99]
        self.reliability = random.choice(reliabilities)

    def read_input(self, signal):
        self.signal = signal

    def distort_signal(self):
        dist = random.uniform(-self.delta, self.delta)
        self.distorted_signal = self.signal + dist

    def get_output(self):
        return self.distorted_signal


class Voter:
    def __init__(self):
        self.readings = []
        self.output = 0.0

    def read_input(self, readings):
        self.readings = readings

    def vote(self):
        pass

    def get_output(self):
        return self.output
        
#Głosowanie medianowe
class MedianVoter(Voter):  
    def vote(self):
        self.vote = statistics.median(self.readings)

#Głosowanie metodą maksymalnego prawdopodobieństwa
class MaximumLikelihood(Voter):
    def vote(self):
        a=1
    

# Głosowanie większościowe
class MajorityVoter(Voter):
    def vote(self):
        count = {}
        # Przypisz poszczególne odczyty do klas
        for reading in self.readings:
            rounded = round(reading) # 1.0 2.0 3.0
            if (count.get(rounded)):    
                count[rounded] += 1
            else:
                count[rounded] = 1

        # Znajdz najczesciej wystepujacy odczyt
        max_count_key = max(count, key=count.get)
        if(count[max_count_key] == 1):
            self.output = None
        else:
            self.output = max_count_key



# Głosowanie wygładzające
class SmoothingVoter(Voter):
    def __init__(self, threshold):
        super().__init__()
        self.previous = 0
        self.threshold = threshold

    # Ustaw poprzedni odczyt
    def set_previous(self, previous):
        self.previous = previous

    def vote(self):
        count = {}
        # Przypisz poszczególne odczyty do klas
        for reading in self.readings:
            rounded = round(reading * 2) / 2
            if (count.get(rounded)):
                count[rounded] += 1
            else:
                count[rounded] = 1

        # Znajdz najczesciej wystepujacy odczyt
        max_count_key = max(count, key=count.get)
        # Jeżeli wszystkie są różne
        if(count[max_count_key] == 1):
            # Wybierz odczyt najbliższy poprzedniemu
            # Oblicz różnice poszczególnych odczytów
            diffs = [abs(self.previous - reading) for reading in self.readings]
            index = diffs.index(min(diffs))
            nearest_reading = self.readings[index]
            # Jeżeli odległość od ostatniego wyniku jest mniejsza niż próg wygładzania
            if abs(nearest_reading - self.previous) <= self.threshold:
                self.output = nearest_reading # Weź go jako wynik
            else:
                self.output = None
        else:
            self.output = max_count_key

#Głosowanie metodą średniej ważonej

class Weighted_average_voter(Voter):
    def  __init__(self):
        super().__init__()        
        self.weights = [0.3, 0.3, 0.4] #wagi poszczegolnych voterow (mozna dostosowac)
    
    def vote(self):
        weighted_sum = sum([self.readings[i] * self.weights[i] for i in range(len(self.readings))])
        total_weight = sum(self.weights)
        self.output = weighted_sum / total_weight

class Linear_Predictor_Voter(Voter):
    def  __init__(self):
        super().__init__() 
        self.model = LinearRegression()
        self.historical_data = []

    def read_input(self, readings):
        super().read_input(readings)
        if len(self.historical_data) >= 3:
            self.historical_data = self.historical_data[1:]  # Usuwa najstarszy odczyt, jeśli jest ich więcej niż 3
        self.historical_data.append(readings)  # Dodaje najnowszy odczyt
        if len(self.historical_data) > 3:
            self.fit_linear_model() # Dostosowuje model regresji liniowej
    
    def fit_linear_model(self):
        if len(self.historical_data) > 3:
            X = np.array([data[:-1] for data in self.historical_data])
            y = np.array([data[-1] for data in self.historical_data])
            self.model.fit(X, y)

    def vote(self):
        if len(self.historical_data) > 3:
            X_new = np.array(self.readings).reshape(1, -1)
            self.output = self.model.predict(X_new)[0]
        else:
            self.output = sum(self.readings) / len(self.readings)
    
    