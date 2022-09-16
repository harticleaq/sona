import os
import numpy as np
import json
import librosa
import torch
import soundfile as sf
import warnings
def rms(x):
    return np.sqrt(np.mean(np.square(x), axis=-1))

def dir_contains_files(path):
    file_list = os.listdir(path)
    if not len(file_list)==0:
        return True
    else:
        return False
def l1_l2_loss(y_true, y_pred, l1_weight, l2_weight):
    loss = 0

    if l1_weight != 0:
        loss += l1_weight*torch.nn.L1Loss()(y_true, y_pred)

    if l2_weight != 0:
        loss += l2_weight * torch.nn.MSELoss()(y_true, y_pred)

    return loss

def compute_receptive_field_length(dilation,stacks,filter_length,target_field):
    length = 0
    for i in dilation:
        length += i
    length *= 2
    length *= stacks
    length += target_field
    return length

def load_wav(wav_path, desired_sample_rate):
    sequence, _ = librosa.load(wav_path, sr = desired_sample_rate)
    return sequence

def get_subsequence_with_speech_indices(full_sequence):
    signal_magnitude = np.abs(full_sequence)

    chunk_length = 800

    chunks_energies = []
    for i in range(0, len(signal_magnitude), chunk_length):
        chunks_energies.append(np.mean(signal_magnitude[i:i + chunk_length]))

    threshold = np.max(chunks_energies) * .1

    onset_chunk_i = 0
    for i in range(0, len(chunks_energies)):
        if chunks_energies[i] >= threshold:
            onset_chunk_i = i
            break

    termination_chunk_i = len(chunks_energies)
    for i in range(len(chunks_energies) - 1, 0, -1):
        if chunks_energies[i] >= threshold:
            termination_chunk_i = i
            break

    num_pad_chunks = 4
    onset_chunk_i = np.max((0, onset_chunk_i - num_pad_chunks))
    termination_chunk_i = np.min((len(chunks_energies), termination_chunk_i + num_pad_chunks))

    return [onset_chunk_i*chunk_length, (termination_chunk_i+1)*chunk_length]

def snr_db(rms_amplitude_A, rms_amplitude_B):
    return 20.0*np.log10(rms_amplitude_A/rms_amplitude_B)

def write_wav(x, filename, sample_rate):

    if type(x) != np.ndarray:
        x = np.array(x)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        sf.write(filename, x, sample_rate)

