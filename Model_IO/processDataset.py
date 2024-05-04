import pandas as pd
import numpy as np
from scipy.fft import fft
from scipy.stats import kurtosis, skew
from scipy.signal import find_peaks
from scipy.stats import entropy


def sliding_window_with_timestamp(data, window_size, stride):
    timestamps = data["timestamp"].values
    values = data["Value"].values
    for i in range(0, len(timestamps) - window_size + 1, stride):
        window_timestamps = timestamps[i : i + window_size]
        window_values = values[i : i + window_size]
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
    return (
        mean,
        max_val,
        std_dev,
        rms,
        kurt,
        skewness,
        peak_to_peak,
        np.mean(abs_diff_signal),
    )


def compute_zero_crossing_rate(signal):
    zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
    return len(zero_crossings) / (len(signal) - 1)


def compute_entropy(signal):
    return entropy(np.abs(signal))


def compute_spectral_features(fft_result, sampling_rate):
    freq_bins = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)
    spectral_centroid = np.sum(freq_bins * np.abs(fft_result)) / np.sum(
        np.abs(fft_result)
    )
    spectral_spread = np.sqrt(
        np.sum(((freq_bins - spectral_centroid) ** 2) * np.abs(fft_result))
        / np.sum(np.abs(fft_result))
    )

    # Calculate weighted mean and standard deviation
    weighted_mean = np.sum(freq_bins * np.abs(fft_result)) / np.sum(np.abs(fft_result))
    weighted_std = np.sqrt(
        np.sum(((freq_bins - weighted_mean) ** 2) * np.abs(fft_result))
        / np.sum(np.abs(fft_result))
    )

    # Calculate skewness using the weighted mean and standard deviation
    spectral_skewness = np.sum(
        ((freq_bins - weighted_mean) / weighted_std) ** 3 * np.abs(fft_result)
    ) / np.sum(np.abs(fft_result))

    # Calculate kurtosis using the weighted mean and standard deviation
    spectral_kurtosis = np.sum(
        ((freq_bins - weighted_mean) / weighted_std) ** 4 * np.abs(fft_result)
    ) / np.sum(np.abs(fft_result))
    return spectral_centroid, spectral_spread, spectral_skewness, spectral_kurtosis


def process_window(start_timestamp, end_timestamp, window_values):
    fft_result = compute_fft(window_values)
    statistics = compute_statistics(window_values)
    zero_crossing_rate = compute_zero_crossing_rate(window_values)
    entropy_value = compute_entropy(window_values)
    spectral_centroid, spectral_spread, spectral_skewness, spectral_kurtosis = (
        compute_spectral_features(fft_result, 125)
    )
    alpha_power, beta_power, gamma_power, delta_power, theta_power = (
        compute_eeg_frequency_bands(fft_result, 125)
    )
    return (
        start_timestamp,
        end_timestamp,
        fft_result,
        *statistics,
        zero_crossing_rate,
        entropy_value,
        spectral_centroid,
        spectral_spread,
        spectral_skewness,
        spectral_kurtosis,
        alpha_power,
        beta_power,
        gamma_power,
        delta_power,
        theta_power,
    )


def adjust_window_parameters(window_duration, sampling_rate):
    window_size = int(window_duration * sampling_rate)
    stride = window_size // 2
    return window_size, stride


def process_data_with_sliding_window(df, window_duration, sampling_rate):
    window_size, stride = adjust_window_parameters(window_duration, sampling_rate)
    results = []
    timestamps = df["timestamp"].values
    for i, (window_timestamps, window_values) in enumerate(
        sliding_window_with_timestamp(df, window_size, stride)
    ):
        start_timestamp = window_timestamps[0]
        end_timestamp = window_timestamps[-1]
        result = process_window(start_timestamp, end_timestamp, window_values)
        results.append(result)
    return results


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


def generate_model_input(df):
    window_duration = 1
    sampling_rate = 125
    results = process_data_with_sliding_window(
        df, window_duration, sampling_rate=sampling_rate
    )

    result_df = pd.DataFrame(
        results,
        columns=[
            "Start Timestamp",
            "End Timestamp",
            "FFT Result",
            "Mean",
            "Max",
            "Standard Deviation",
            "RMS",
            "Kurtosis",
            "Skewness",
            "Peak-to-Peak",
            "Abs Diff Signal",
            "Zero Crossing Rate",
            "Entropy",
            "Spectral Centroid",
            "Spectral Spread",
            "Spectral Skewness",
            "Spectral Kurtosis",
            "Alpha Power",
            "Beta Power",
            "Gamma Power",
            "Delta Power",
            "Theta Power",
        ],
    )
    fft_columns = [f"FFT_{i}" for i in range(125)]
    fft_data = pd.DataFrame(result_df["FFT Result"].tolist(), columns=fft_columns)
    result_df = pd.concat([result_df.drop("FFT Result", axis=1), fft_data], axis=1)
    
    optimized = [
        "FFT_101",
        "Spectral Spread",
        "Kurtosis",
        "FFT_98",
        "FFT_26",
        "Max",
        "Spectral Skewness",
        "FFT_24",
        "FFT_4",
        "Beta Power",
        "Abs Diff Signal",
        "FFT_70",
        "FFT_1",
        "FFT_2",
        "FFT_5",
        "FFT_103",
        "Start Timestamp",
        "FFT_121",
        "FFT_100",
        "FFT_25",
        "FFT_120",
        "Entropy",
        "FFT_22",
        "FFT_55",
        "RMS",
        "FFT_123",
        "FFT_27",
        "Standard Deviation",
        "End Timestamp",
        "Zero Crossing Rate",
        "Skewness",
        "Peak-to-Peak",
        "Delta Power",
    ]
    return result_df[optimized]
