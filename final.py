import os
import pandas as pd
import numpy as np
import joblib
from scipy.fft import fft
from check import clean_csv
from scipy.stats import kurtosis, skew

def sliding_window_with_timestamp(data, window_size, stride):
    timestamps = data['timestamp'].values
    values = data['Value'].values
    for i in range(0, len(timestamps) - window_size + 1, stride):
        window_timestamps = timestamps[i:i+window_size]
        window_values = values[i:i+window_size]
        yield window_timestamps, window_values

def compute_fft(signal):
    return np.abs(fft(signal))

def compute_statistics(signal):
    mean = np.mean(signal)
    max_val = np.max(signal)
    std_dev = np.std(signal)
    rms = np.sqrt(np.mean(signal**2))
    kurt = kurtosis(signal)
    skewness = skew(signal)
    peak_to_peak = np.ptp(signal)
    abs_diff_signal = np.sum(np.abs(np.diff(signal)))
    return mean, max_val, std_dev, rms, kurt, skewness, peak_to_peak, np.mean(abs_diff_signal)

def compute_eeg_frequency_bands(fft_result, sampling_rate):
    freq_bins = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)
    alpha_band = (8, 12)
    beta_band = (12, 30)
    gamma_band = (30, 100)
    delta_band = (0.5, 4)
    theta_band = (4, 8)

    alpha_idx = np.where((freq_bins >= alpha_band[0]) & (freq_bins <= alpha_band[1]))[0]
    beta_idx = np.where((freq_bins >= beta_band[0]) & (freq_bins <= beta_band[1]))[0]
    gamma_idx = np.where((freq_bins >= gamma_band[0]) & (freq_bins <= gamma_band[1]))[0]
    delta_idx = np.where((freq_bins >= delta_band[0]) & (freq_bins <= delta_band[1]))[0]
    theta_idx = np.where((freq_bins >= theta_band[0]) & (freq_bins <= theta_band[1]))[0]

    alpha_power = np.sum(fft_result[alpha_idx])
    beta_power = np.sum(fft_result[beta_idx])
    gamma_power = np.sum(fft_result[gamma_idx])
    delta_power = np.sum(fft_result[delta_idx])
    theta_power = np.sum(fft_result[theta_idx])

    return alpha_power, beta_power, gamma_power, delta_power, theta_power

def process_window(start_timestamp, end_timestamp, window_values):
    fft_result = compute_fft(window_values)
    statistics = compute_statistics(window_values)
    alpha_power, beta_power, gamma_power, delta_power, theta_power = compute_eeg_frequency_bands(fft_result, 125)
    return start_timestamp, end_timestamp, fft_result, *statistics, alpha_power, beta_power, gamma_power, delta_power, theta_power

def adjust_window_parameters(window_duration, sampling_rate):
    window_size = int(window_duration * sampling_rate)
    stride = window_size // 2
    return window_size, stride

def process_data_with_sliding_window(df, window_duration, sampling_rate):
    window_size, stride = adjust_window_parameters(window_duration, sampling_rate)
    results = []
    timestamps = df['timestamp'].values
    for i, (window_timestamps, window_values) in enumerate(sliding_window_with_timestamp(df, window_size, stride)):
        start_timestamp = window_timestamps[0]
        end_timestamp = window_timestamps[-1]
        result = process_window(start_timestamp, end_timestamp, window_values)
        results.append(result)
    return results

def generate_model_input(df):
    
    window_duration = 1  # seconds, adjust according to your preference
    sampling_rate = 125  # Hz
    results = process_data_with_sliding_window(df, window_duration, sampling_rate=sampling_rate)
            
    result_df = pd.DataFrame(results, columns=['Start Timestamp', 'End Timestamp', 'FFT Result', 'Mean', 'Max', 'Standard Deviation', 'RMS', 'Kurtosis', 'Skewness', 'Peak-to-Peak', 'Abs Diff Signal', 'Alpha Power', 'Beta Power', 'Gamma Power', 'Delta Power', 'Theta Power'])
    fft_columns = [f'FFT_{i}' for i in range(125)]
    result_df[fft_columns] = pd.DataFrame(result_df['FFT Result'].tolist())
    result_df.drop('FFT Result', axis=1, inplace=True)
    
    return result_df
model = joblib.load('model.pkl')
result = generate_model_input(clean_csv("./dataset/lefta.csv")).drop(columns=['Start Timestamp', "End Timestamp"])
print(model.predict([result.iloc[-1]]))