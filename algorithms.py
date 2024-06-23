import numpy as np
import random
from collections import Counter


# Generator sygnału
class SignalGenerator:
    def __init__(self, samples, periods):
        self.signals = []
        self.samples = samples  # Liczba probek w okresie
        self.periods = periods  # Liczba okresów

    # Generowanie próbek sygnału f(x)=50sin+50
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

    def read_input(self, signal):
        self.signal = signal

    def distort_signal(self):
        dist = random.randint(-self.delta, self.delta)
        self.distorted_signal = self.signal + dist

    def get_output(self):
        return self.distorted_signal


class Voter:
    def __init__(self):
        self.readings = []
        self.output = 0

    def read_input(self, readings):
        self.readings = readings

    def vote(self):
        pass

    def get_output(self):
        return self.output


# Głosowanie większościowe
class MajorityVoter(Voter):
    def vote(self):
        # Policz występowanie poszczególnych odczytów
        reading_counts = Counter(self.readings)
        # Znajdź najczęściej występujący odczyt
        most_common_reading, count = reading_counts.most_common(1)[0]
        # Jeżeli wszystkie są różne
        if count == 1:
            self.output = None # Brak wyniku
        else:
            self.output = most_common_reading


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
        # Policz występowanie poszczególnych odczytów
        reading_counts = Counter(self.readings)
        # Znajdź najczęściej występujący odczyt
        most_common_reading, count = reading_counts.most_common(1)[0]
        # Jeżeli wszystkie są różne
        if count == 1:
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
            self.output = most_common_reading

