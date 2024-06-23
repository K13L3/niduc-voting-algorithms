import random
import statistics
from algorithms import *

def main():

    # tabelka()
    simulate(10000, 10, 0.2, 0.4) # samples, periods, delta, threshold
    simulate(10000, 10, 0.5, 0.4)
    simulate(10000, 10, 0.6, 0.4)
    simulate(10000, 10, 0.7, 0.4)
    print("------")
    simulate(10000, 10, 0.5, 0.2) # samples, periods, delta, threshold
    simulate(10000, 10, 0.5, 0.3)
    simulate(10000, 10, 0.5, 0.5)
    simulate(10000, 10, 0.5, 0.7)
    

def tabelka():
    # Inicjalizacja instancji obiektów
    signal_generator = SignalGenerator(100, 5)
    sensor1 = Sensor(5)
    sensor2 = Sensor(5)
    sensor3 = Sensor(5)
    
    majority_voter = MajorityVoter()
    smoothing_voter = SmoothingVoter(0.5)
    linear_voter = Linear_Predictor_Voter()
    weighted_average_voter = Weighted_average_voter()

    # Podstawowa tabelka
    basic_signals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    dist1_signals = [1.5, 1.9, 3.6, 4.4, 5.4, 6.2, 7.1, 8.3, 9.8, 10.6]  # Zmienic na zaburzone
    dist2_signals = [1.8, 2.5, 3.3, 4.2, 5.8, 6.1, 7.9, 8.2, 9.3, 10.1]  # Zmienic na zaburzone
    dist3_signals = [1.2, 2.3, 3.2, 4.6, 5.5, 6.9, 7.7, 8.4, 9.8, 10.4]

    # Tablice z wynikami poszczególnych algorytmów
    majority_out = []
    smoothing_out = []
    weighted_out = []
    linear_out = []

    signal_generator.set_signals(basic_signals)
    for i in range(0, 10):
        readings = dist3_signals[i], dist1_signals[i], dist2_signals[i]

        # Głosowanie więszkościowe
        majority_voter.read_input(readings)
        majority_voter.vote()
        majority_out.append(majority_voter.get_output())

        # Głosowanie wygładzające
        smoothing_voter.read_input(readings)
        smoothing_voter.vote()
        smoothing_out.append(smoothing_voter.get_output())

        #Glosowanie weight
        weighted_average_voter.read_input(readings)
        weighted_average_voter.vote()
        weighted_out.append(weighted_average_voter.get_output())

        #Glosowanie_liniowe
        linear_voter.read_input(readings)
        linear_voter.vote()
        linear_out.append(linear_voter.get_output())

    print("Wiekszosciowe: ", majority_out)
    print("Wygladzajace: ", smoothing_out)
    print("Wazone: ", weighted_out)
    print("Liniowe: ", linear_out)

# Symuluj liczba próbek w okresie, liczba okresów
def simulate(samples, periods, delta, threshold):
    # Inicjalizacja instancji obiektów
    signal_generator = SignalGenerator(samples, periods)
    sensor1 = Sensor(delta)
    sensor2 = Sensor(delta)
    sensor3 = Sensor(delta)
    
    majority_voter = MajorityVoter()
    smoothing_voter = SmoothingVoter(0.5)
    linear_voter = Linear_Predictor_Voter()
    weighted_average_voter = Weighted_average_voter()

    # Tablice z wynikami poszczególnych algorytmów
    majority_out = []
    smoothing_out = []
    weighted_out = []
    linear_out = []

    signal_generator.generate_signal()
    signal = signal_generator.get_signal()
    for sig in signal:
        # Odczyt sygnałów
        sensor1.read_input(sig)
        sensor2.read_input(sig)
        sensor3.read_input(sig)
        # Zaburzanie sygnałów
        sensor1.distort_signal()
        sensor2.distort_signal()
        sensor3.distort_signal()
        # Tablica z odczytami
        readings = [sensor1.get_output(),sensor2.get_output(),sensor3.get_output()]
        # Głosowanie więszkościowe
        majority_voter.read_input(readings)
        majority_voter.vote()
        majority_out.append(majority_voter.get_output())

        # Głosowanie wygładzające
        smoothing_voter.read_input(readings)
        smoothing_voter.vote()
        smoothing_out.append(smoothing_voter.get_output())

        #Glosowanie weight
        weighted_average_voter.read_input(readings)
        weighted_average_voter.vote()
        weighted_out.append(weighted_average_voter.get_output())

        #Glosowanie_liniowe
        linear_voter.read_input(readings)
        linear_voter.vote()
        linear_out.append(linear_voter.get_output())

    majority_good = 0
    majority_bad = 0
    smoothing_good = 0
    smoothing_bad = 0
    weighted_good = 0
    weighted_bad = 0
    linear_good = 0
    linear_bad = 0

    for i in range(len(signal)):
         # Głosowanie więszkościowe
    
        if(majority_out[i] is not None):
            if(abs(signal[i] - majority_out[i]) <= threshold):
                majority_good += 1
            else:
                majority_bad += 1
        else:
            majority_bad += 1

        # Głosowanie wygładzające
        if(smoothing_out[i] is not None):
            if(abs(signal[i] - smoothing_out[i]) <= threshold):
                smoothing_good += 1
            else:
                smoothing_bad += 1
        else:
            smoothing_bad += 1

        #Glosowanie weight
        if(abs(signal[i] - weighted_out[i]) <= threshold):
            weighted_good += 1
        else:
            weighted_bad += 1

        #Glosowanie_liniowe
        if(abs(signal[i] - linear_out[i]) <= threshold):
            linear_good += 1
        else:
            linear_bad += 1

    n_of_readings = len(signal)
    majority_availabilty = majority_good / n_of_readings
    smoothing_availabilty = smoothing_good / n_of_readings
    weighted_availabilty = (weighted_good / n_of_readings)
    lineary_availabilty = linear_good / n_of_readings
    
    print("majority: ",majority_availabilty, sep=" ")
    print("smoothing: ",smoothing_availabilty, sep=" ")
    print("weighted: ",weighted_availabilty, sep=" ") 
    print("linear: ",lineary_availabilty, sep=" ")


    # Dla różnego próbkowania
    
    # Dla 100 próbek
    # 10 okresów, 100 próbek

    # 100 okresów, 100 próbek

    # 1000 okresów, 100 próbek

    # Dla 1000 próbek
    # 10 okresów, 1000 próbek

    # 100 okresów, 1000 próbek

    # 1000 okresów, 1000 próbek



main()

