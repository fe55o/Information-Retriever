import Indexer
import PhraseQuery
import PreProcessing
import json


def saveOnDisk(path, data):
    file = open(path, "w")
    json.dump(data, file)
    file.close


def loadFromDisk(path):
    data = None
    with open(path, "r") as fp:
        data = json.load(fp)
    return data


def main():
    list_query = ["Inforamtion", "Retrieval", "System"]

    # run preprocessing on files and save result on disk in data/data.json
    data = PreProcessing.run()
    saveOnDisk("data/data.json", data)

    # load the tokens and result from data.json file
    data = loadFromDisk("data/data.json")

    # pass the result to Indexer to create the auxiliary table and save it on disk
    Indexer.run("data/auxiliary table.json", data)

    # load the auxliliary from disk
    auxliliary_table = loadFromDisk("data/auxiliary table.json")

    # pass the phrase query which enterd by user and auxlliary table to the phrasequery to get result
    result = PhraseQuery.run(auxliliary_table, list_query)
    print(result)


# if __name__ == "__main__":
#    main()