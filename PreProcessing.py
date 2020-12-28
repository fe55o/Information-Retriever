from nltk.corpus import stopwords
import nltk
import string


def removePunc(files):
    for i in range(len(files)):
        files[i] = files[i].translate(
            str.maketrans(string.punctuation, " " * len(string.punctuation))
        )
    return files


def tokenization(files):
    for i in range(len(files)):
        files[i] = nltk.word_tokenize(files[i])
    return files


def givePositions(files):
    i = 0
    j = 0
    pos = 0
    for i in range(len(files)):
        for j in range(len(files[i])):
            if len(files[i][j]) != 0:
                pos += 1
            files[i][j] = [files[i][j], pos]
    return files


def normalize(files):
    stop_words = stopwords.words("english")
    for i in range(len(files)):
        for j in range(len(files[i])):
            token = files[i][j]
            token = token.lower()
            if token not in stop_words and token.isalpha():
                files[i][j] = token
            else:
                files[i][j] = ""
    return files


def flatten(files):
    result = []
    doc_id = 0
    for i in range(len(files)):
        for j in range(len(files[i])):
            if len(files[i][j][0]) != 0:
                files[i][j] = [files[i][j][0], doc_id, files[i][j][1]]
                result.append(files[i][j])
        doc_id += 1
    return result


def preProcessing(files):
    files = removePunc(files)
    files = tokenization(files)
    files = normalize(files)
    files = givePositions(files)
    files = flatten(files)
    return files
