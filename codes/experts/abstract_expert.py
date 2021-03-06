import pickle

import numpy as np


class AbstracExpert:
    LABELS = {'a', 'c', 'd', 'e', 'f', 'g', 'h', 'l', 'p', 'r'}

    def __init__(self, name):
        self.model = None
        self.name = name
        self.label2ind = {}
        self.ind2label = {}
        for i, label in enumerate(self.LABELS):
            self.label2ind[label] = i
            self.ind2label[i] = label

    def labels_2_one_hot_vectors(self, labels):
        one_hot_vectors = np.zeros((len(labels), len(self.LABELS)), np.float32)
        label_inds = [self.label2ind[label] for label in labels]
        one_hot_vectors[list(range(len(label_inds))), label_inds] = 1.0
        return one_hot_vectors

    def one_hot_vector_2_label(self, one_hot_vector):
        ind = np.argmax(one_hot_vector)
        label = self.ind2label[ind]
        return label

    def train(self, X, G):
        raise NotImplementedError

    def suggest(self, x):
        raise NotImplementedError

    def calculate_offline_loss(self, X, G):
        G_hat = [self.suggest(x) for x in X]

        G = np.array(G)
        loss = (G != G_hat)
        cumulative_loss = np.cumsum(loss) / list(range(1, len(G_hat)+1))

        return cumulative_loss

    def save_model(self):
        with open('trained_models/{0}.model'.format(self.name), 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self):
        with open('trained_models/{0}.model'.format(self.name), 'rb') as f:
            self.model = pickle.load(f)
