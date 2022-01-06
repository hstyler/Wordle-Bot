import pandas as pd
import argparse
import os

def get_list(word_length, list_length):
    word_list_path = os.path.join(os.path.dirname(__file__), 'wordlist.csv')

    print("Looking for {} words of length {}".format(list_length, word_length))
    df = pd.read_csv(word_list_path)
    df = df[df.word.apply(lambda x: len(str(x))==word_length)]
    word_list = df.word.tolist()
    if len(word_list) < list_length:
        raise IndexError(len(word_list))
    else:
        return word_list[0:list_length]

# parser = argparse.ArgumentParser(description='Create a word list from the \'⅓ Million Most Frequent English Words on the Web\' dataset')
# parser.add_argument('word_length', metavar='Word Length', type=int, help='Length of word to generate list for')
# parser.add_argument('list_length', metavar='List Length', type=int, help='How many words to get')
# args = parser.parse_args()

# get_list(args.word_length, args.list_length)