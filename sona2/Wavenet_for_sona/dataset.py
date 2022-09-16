from Wavenet_for_sona import util
import os
import numpy as np
import torch

class sonaDataset():
    def __init__(self,config,model):
        self.model = model
        self.path = config['dataset']['path']
        self.sample_rate = config['dataset']['sample_rate']
        self.file_paths = {'train': {'clean': [], 'noisy': []}, 'test': {'clean': [], 'noisy': []}}
        self.sequences = {'train': {'clean': [], 'noisy': []}, 'test': {'clean': [], 'noisy': []}}
        self.voice_indices = {'train': [], 'test': []}
        self.regain_factors = {'train': [], 'test': []}
        self.batch_size = config['training']['batch_size']
        self.noise_only_percent = config['dataset']['noise_only_percent']
        self.regain = config['dataset']['regain']
        self.extract_voice = config['dataset']['extract_voice']
        self.in_memory_percentage = config['dataset']['in_memory_percentage']
        self.num_sequences_in_memory = 0


    def load_dataset(self):
        print('loading sonaDataset...')

        for Set in ['train', 'test']:
            for condition in ['clean', 'noisy']:

                current_directory = os.path.join(self.path, condition + '_' + Set + 'set_wav')
                sequences, file_paths, speech_onset_offset_indices, regain_factors = self.load_directory(current_directory, condition)

                self.file_paths[Set][condition] = file_paths
                self.sequences[Set][condition] = sequences

                if condition == 'clean':
                    self.voice_indices[Set] = speech_onset_offset_indices
                    self.regain_factors[Set] = regain_factors

        return self

    def load_directory(self, directory_path, condition):

        filenames = [filename for filename in sorted(os.listdir(directory_path)) if filename.endswith('.wav')]
        file_paths = []
        speech_onset_offset_indices = []
        regain_factors = []
        sequences = []

        for filename in filenames:
            filepath = os.path.join(directory_path, filename)

            if condition == 'clean':

                sequence = util.load_wav(filepath , self.sample_rate)
                sequences.append(sequence)
                self.num_sequences_in_memory += 1
                regain_factors.append(self.regain / util.rms(sequence))
                if self.extract_voice:
                    speech_onset_offset_indices.append(util.get_subsequence_with_speech_indices(sequence))
            else:

                sequence = util.load_wav(filepath , self.sample_rate)
                sequences.append(sequence)
                self.num_sequences_in_memory += 1
            file_paths.append(filepath)

        return sequences, file_paths, speech_onset_offset_indices, regain_factors

    def get_random_batch_generator(self,Set):
        if Set not in ['train', 'test']:
            raise ValueError("Argument SET must be either 'train' or 'test'")

        while True:
            sample_indices = np.random.randint(0, len(self.sequences[Set]['clean']), self.batch_size)
            # sample_indices = np.array(range(len(self.sequences[Set]['clean'])))
            # sample_indices =  np.append(sample_indices,sample_indices)

            condition_inputs = []
            batch_inputs = []
            batch_outputs_1 = []
            batch_outputs_2 = []

            for i, sample_i in enumerate(sample_indices):

                while True:

                    speech = np.array(self.sequences[Set]['clean'][sample_i])
                    noisy = np.array(self.sequences[Set]['noisy'][sample_i])
                    noise = noisy - speech

                    if self.extract_voice:
                        speech = speech[self.voice_indices[Set][sample_i][0]:self.voice_indices[Set][sample_i][1]]

                    speech_regained = speech * self.regain_factors[Set][sample_i]
                    noise_regained = noise * self.regain_factors[Set][sample_i]
                    if len(speech_regained) < self.model.input_length:

                        sample_i = np.random.randint(0, len(self.sequences[Set]['clean']))
                    else:
                        break

                offset = np.squeeze(np.random.randint(0, len(speech_regained) - self.model.input_length, 1))

                speech_fragment = speech_regained[offset:offset + self.model.input_length]
                noise_fragment = noise_regained[offset:offset + self.model.input_length]

                Input = noise_fragment + speech_fragment
                output_speech = speech_fragment
                output_noise = noise_fragment

                if self.noise_only_percent > 0:
                    if np.random.uniform(0, 1) <= self.noise_only_percent:
                        Input = output_noise #Noise only
                        output_speech = np.array([0] * self.model.input_length) #Silence

                batch_inputs.append(Input)
                batch_outputs_1.append(output_speech)
                batch_outputs_2.append(output_noise)

            batch_inputs = np.array(batch_inputs, dtype='float32')
            batch_outputs_1 = np.array(batch_outputs_1, dtype='float32')
            batch_outputs_2 = np.array(batch_outputs_2, dtype='float32')

            batch_outputs_1 = batch_outputs_1[:, self.model.get_padded_target_field_indices()]
            batch_outputs_2 = batch_outputs_2[:, self.model.get_padded_target_field_indices()]

            batch = {'data_input': batch_inputs, 'condition_input': condition_inputs}, {
                'data_output_1': batch_outputs_1, 'data_output_2': batch_outputs_2}

            yield batch

class denoising_dataset(torch.utils.data.IterableDataset):
    def __init__(self, generator):
        self.generator = generator
    def __iter__(self):
        return self.generator
