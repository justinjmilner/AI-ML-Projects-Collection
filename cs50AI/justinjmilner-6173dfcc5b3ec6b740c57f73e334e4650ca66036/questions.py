import nltk
import sys
import os
import string
import math
import itertools

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)
    print('\n')

def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:
            files[file] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = []
    stopwords = set(nltk.corpus.stopwords.words("english"))
    p = string.punctuation
    temp_tokens = nltk.word_tokenize(document.lower())

    # Filter stopwords and punctuation tokens
    for token in temp_tokens:
        if token in stopwords:
            continue
        if all(char in p for char in token):
            continue
        tokens.append(token)

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Count each word in the corpus
    word_count = {}
    document_count = 0
    for document in documents:
        document_count += 1
        for word in documents[document]:
            if word not in word_count:
                word_count[word] = 0
            elif word_count[word] == document_count:
                continue
            word_count[word] += 1

    # Calculate idf value for the word
    n = len(documents)
    idf = {}
    for word in word_count:
        idf[word] = math.log(n/word_count[word])

    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Initiate an empty dictionary for files
    ranking = {
        filename: 0
        for filename in files
    }

    # Determine TF-IDF ranking
    for word in query:
        for file in files:
            tf = files[file].count(word)
            ranking[file] += tf * idfs[word]

    # Sort file rankings
    ranked_dict = dict(itertools.islice((sorted(ranking.items(),
                       key=lambda item: item[1], reverse=True)), n))

    return ranked_dict


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Initiate empty dictionary for sentences
    ranking = {
        sentence: 0
        for sentence in sentences
    }

    # Add IDF values to sentences
    for word in query:
        for sentence in sentences:
            if word in sentences[sentence]:
                ranking[sentence] += idfs[word]

    # Calculate query term density
    max_idf = max(ranking.values())
    qtd_ranking = {}
    for sentence in ranking:
        if ranking[sentence] == max_idf:
            for word in query:
                tf = sentences[sentence].count(word)
                if sentence not in qtd_ranking:
                    qtd_ranking[sentence] = 0
                qtd_ranking[sentence] += (tf / len(sentence))

    # Sort top sentences
    top_ranking = dict(itertools.islice((sorted(qtd_ranking.items(),
                         key=lambda item: item[1], reverse=True)), n))

    return top_ranking


if __name__ == "__main__":
    main()
