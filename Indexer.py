from operator import itemgetter
import json

# [[token, pag_id, pos]]
data = [
    ["hesham", 1, 1],
    ["ahmed", 2, 1],
    ["hesham", 2, 1],
    ["hesham", 1, 4],
    ["hesham", 1, 5],
]

# sort by term then docID then position
def sortData(data):
    data = sorted(data, key=itemgetter(0, 1, 2))
    # print("data: ", data)
    return data


# { "item" : { doc_id : [pos_id] },  }
def add_value_in_dict(dict, key, doc_id, term_pos):
    if len(key) == 0:
        return
    if key not in dict:
        dict[key] = {}
    if doc_id not in dict[key]:
        (dict[key])[doc_id] = []
    if term_pos not in (dict[key])[doc_id]:
        (dict[key])[doc_id].append(term_pos)
    return dict


# { "item" : { doc_id : [pos_id] },  }
def createIndexingTable(data):
    indexing_tabel = {}
    for item in data:
        indexing_tabel = add_value_in_dict(indexing_tabel, item[0], item[1], item[2])
    # print("table: ", indexing_tabel)
    return indexing_tabel


def saveOnDisk(indexing_table):
    file = open("C:/Users/hesha/Desktop/Information-Retriever/data/table.json", "w")
    json.dump(indexing_table, file)
    file.close


def run(data):
    data = sortData(data)
    indexing_table = createIndexingTable(data)
    saveOnDisk(indexing_table)
    print(indexing_table)
    print("Term frequency: ", len(indexing_table["hesham"]))


run(data)