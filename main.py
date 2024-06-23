import random
import statistics
from algorithms import *

def main():
    # Inicjalizacja instancji obiektów
    signal_generator = SignalGenerator(100, 5)
    sensor1 = Sensor(5)
    sensor2 = Sensor(5)
    sensor3 = Sensor(5)
    majority_voter = MajorityVoter()
    smoothing_voter = SmoothingVoter(0.5)

    # Podstawowa tabelka
    basic_signals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dist1_signals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Zmienic na zaburzone
    dist2_signals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Zmienic na zaburzone
    majority_out = []
    smoothing_out = []
    signal_generator.set_signals(basic_signals)
    for i in range(0, 10):
        majority_voter.read_input(basic_signals)
        majority_voter


    # Symulacje

    # Dla różnego próbkowania
    # Dla różnego wprowadzania błedów (co 10-20 cykli)

    # Dla 100 próbek
    # 10 okresów, 100 próbek

    # 100 okresów, 100 próbek

    # 1000 okresów, 100 próbek

    # Dla 1000 próbek
    # 10 okresów, 1000 próbek

    # 100 okresów, 1000 próbek

    # 1000 okresów, 1000 próbek



main()

