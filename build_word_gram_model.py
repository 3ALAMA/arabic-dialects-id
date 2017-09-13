import nltk
import os
import glob
import feature_extraction
from nltk.metrics.scores import f_measure, precision, recall
import collections
import sys
import argparse
import pickle

parser = argparse.ArgumentParser(description='build word gram model')
parser.add_argument('-t', '--train-dir', type=str,
                    help='training directory.', required=True)
parser.add_argument('-m', '--model', type=str,
                    help='model file.', required=True)
parser.add_argument('-o', '--order', type=int,
                    help='n-gram', required=True)
parser.add_argument('-c', '--cut-freq', type=int,
                    help='cut frequency', required=True)


def build_model(train_directory, ngram_order, cut_freq_max, model_file_name):
    train = list()
    labels = os.listdir(train_directory)
    for label in labels:
        files = glob.glob(train_dir + label + "/*")
        for file in files:
            text = open(file).read().strip()
            train.append((text, label))

    train_set = feature_extraction.prepare_data(dataset=train, order=ngram_order, selection='gt', max=cut_freq_max)
    # train_set, test_set = feature_extraction.prepare_train_test(dataset=all_data, selection='top', max=2000,
    # split_indx=indx)

    print('training ...')
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('training is done ... save the model ...')
    with open(model_file_name, mode='wb') as model_saver:
        pickle.dump(classifier, model_saver)
    print('model written successfully!')


# python build_word_gram_model.py -t Train_Filter_Corpus/ -o 2 -c 7 -m word_gram_models/Train_Filter_model_2g
# python build_word_gram_model.py -t Train_Filter_Corpus/ -o 1 -c 7 -m word_gram_models/Train_Filter_model_1g
# python build_word_gram_model.py -t train_multidialect_arabic/conversations/ -o 2 -c 3 -m word_gram_models/multidialect_model_2g
# python build_word_gram_model.py -t train_multidialect_arabic/conversations/ -o 1 -c 3 -m word_gram_models/multidialect_model_1g
# python build_word_gram_model.py -t Train_Padic/conversation/ -o 2 -c 5 -m word_gram_models/padic_model_2g
# python build_word_gram_model.py -t Train_Padic/conversation/ -o 1 -c 5 -m word_gram_models/padic_model_1g


if __name__ == '__main__':
    args = parser.parse_args()
    train_dir = args.train_dir
    model_name = args.model
    n = args.order
    c = args.cut_freq
    build_model(train_directory=train_dir, ngram_order=n, cut_freq_max=c, model_file_name=model_name)