import logging

from librosa import cqt
from librosa.feature import melspectrogram

from util import load_dataset, fcall, save_data

from tqdm import tqdm

def prepare_CQT(data):
    data = cqt(y = data['samples'], sr = data['sampling_rate'])
    return data

def prepare_Mel_spectrogram(data):
    data = melspectrogram(y = data['samples'], sr = data['sampling_rate'])
    return data

@fcall
def preprocess_dataset(args):
    dataset = load_dataset(args["raw_dataset"])
    for index in tqdm(range(len(dataset))):
        dataset[index]['cqt'] = prepare_CQT(dataset[index])
        dataset[index]['Mel'] = prepare_Mel_spectrogram(dataset[index])
    save_data(dataset, 'mp3_preprocessed.pickle')
    return dataset