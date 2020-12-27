from ReadFiles import readFiles
from PreProcessing1 import preProcessing
from Indexer import indexer
from PhraseQuery import phraseQuery
from QueryPreProcessing import prepareQuery
import json
import time


def saveOnDisk(path, data):
    file = open(path, "w")
    json.dump(data, file)
    file.close


def loadFromDisk(path):
    data = None
    with open(path, "r") as fp:
        data = json.load(fp)
    return data


def readQueryFromUser():
    query = input()
    return query


def main():
    query = readQueryFromUser()
    query = prepareQuery(query)
    if query == False:
        print("Wrong syntax!!")
        return

    list_query = query

    # read files from disk
    files = readFiles("files/")

    # run preprocessing on files and save result on disk in data/data.json
    data = preProcessing(files)
    saveOnDisk("data/data.json", data)

    # load the tokens and result from data.json file
    data = loadFromDisk("data/data.json")

    # pass the result to Indexer to create the auxiliary table and save it on disk
    indexer("data/auxiliary table.json", data)

    # load the auxliliary from disk
    auxliliary_table = loadFromDisk("data/auxiliary table.json")

    start = time.time()

    # pass the phrase query which enterd by user and auxlliary table to the phrasequery to get result
    result = phraseQuery(auxliliary_table, list_query)

    end = time.time()

    print(result)
    print("Time taken is: ", (end - start))


if __name__ == "__main__":
    main()