# nltk.download("punkt")
# nltk.download("stopwords")
import PyPDF2
from PyPDF2 import PdfFileReader
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
import numpy as np
import ast

# from ast import literal_eval


def files():
    """

    return: list of files in the directory

    """
    directory = "files/"
    files_name = []
    for sample in os.listdir(directory):
        files_name.append(sample)
    return files_name


def order(files_list):
    """
    files_list: list of files we will work on

    return: ordered files_list
    """
    temp = 0
    str_temp = ""
    for i in range(len(files_list)):
        pdf = open("files/" + files_list[i], "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        if pdf_reader.numPages > temp:
            temp = pdf_reader.numPages
            str_temp = files_list[i]
            del files_list[i]
            files_list.insert(0, str_temp)
            # print("found"+ files_list[i])

    return files_list


def reading():
    """

    return: a dataframe with all the files in columns and the pages of each file in rows

    """

    print("=============in the reading =============")

    # files_list =[]
    files_list = files()
    # make the bigger document in the begenning of the list
    files_list = order(files_list)

    # creating a dataframe to hold the docs
    df = pd.DataFrame()  #

    for j in range(len(files_list)):
        page_list = []
        print(files_list[j])
        pdf = open("files/" + files_list[j], "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf)

        print("num of pages -> " + str(pdf_reader.numPages))

        for i in range(pdf_reader.numPages):
            page = pdf_reader.getPage(i)
            pdf_words = page.extractText()
            page_list.append(pdf_words)
            # print(page_list)
        df[files_list[j]] = pd.Series(page_list)

    # closing the pdf file
    pdf.close()
    return df


def normalize(df):
    """
    df: a dataframe of all the files

    return: normalized dataframe with pages index
    """
    print("=============in the normalize =============")
    df["pages"] = df.index
    # this cell runs only one time
    # if you want to run again go back from the previous cell

    files_list = files()
    stop = stopwords.words("english")
    for i in files_list:
        # convert to lower case
        df[i] = df[i].str.lower()
        # removing puncituations
        df[i] = df[i].str.replace("[^\w\s]", "")
        # convert to string
        df[i] = df[i].apply(str)
    return df


def expanding(df):
    """
    df: a normalized dataframe of all the files

    return: a dataframe with each row represent a line not page, and make lines index
    """
    print("=============in the expanding =============")
    new_df = pd.DataFrame()
    #    global word_list
    #    global index_list
    # loop on each column or file
    for i in range(len(df.columns) - 1):
        word_list = []
        index_list = []
        page_list = []
        index = 0
        print("in the file #" + str(i))
        print("===================================")
        # loope on each cell or page
        for j in range(len(df.index)):
            ptr = -1
            # print(j)
            if df.iloc[j][i] == "nan":
                break
            # loop on each element on the cell or character
            for k in range(len(df.iloc[j][i])):
                if df.iloc[j][i][k] == "\n":
                    index_list.append(index)
                    word_list.append(df.iloc[j][i][ptr + 1 : k])
                    page_list.append(df.iloc[j][len(df.columns) - 1])
                    ptr = k
                    index = index + 1
                    # print(k)

        new_df[str(i)] = pd.Series(word_list)
        new_df["file " + str(i) + " indexes"] = pd.Series(index_list)
        new_df["file " + str(i) + " page numbers"] = pd.Series(page_list)
        print("length of word_list " + str(i) + " is  ---> " + str(len(word_list)))

    return new_df


def tokenize(new_df):
    """
    new_df: dataframe of the files

    return: tokenized dataframe
    """
    print("=============in the tokenize=============")
    for i in range(0, 10, 1):
        new_df.loc[:][str(i)] = new_df.loc[:][str(i)].apply(str)
        new_df.loc[:][str(i)] = new_df.loc[:][str(i)].apply(nltk.word_tokenize)
        # new_df.loc[:][str(i)] = new_df.loc[:][str(i)].apply(lambda x: [item for item in x if item not in stop])
    return new_df


def return_term_list(new_df):
    """
    new_df: a dataframe of all the files

    return: list of lists containing each token with it's doc_id and token_id
    """
    print("=============in the return_term_list =============")
    all_terms_list = [[]]

    # loop on each file
    for i in range(0, len(new_df.columns), 3):
        # loope on each cell or page
        counter = 0
        for j in range(len(new_df.index)):
            if new_df.iloc[j][i] == ["nan"] or new_df.iloc[j][i] == []:
                continue
            for k in range(len(new_df.iloc[j][i])):
                term_list = []
                # term
                term_list.append(new_df.iloc[j][i][k])
                # doc_id
                term_list.append(i // 3)
                # token_pos in the document
                term_list.append(int(new_df.iloc[j][i + 1] + k + counter))
                if k == 1 and len(new_df.iloc[j][i]) == 2:
                    counter += 1
                elif k == len(new_df.iloc[j][i]) - 1:
                    counter += k
                # page_id
                # term_list.append(new_df.iloc[j][i+2])

                # append each term to the all_term_list
                all_terms_list.append(term_list)

    return all_terms_list


#        print(i)


def stop_words_removal(all_terms_list):
    """
    all_terms_list: list of lists containing all the terms in all the files

    return: list of lists after removing stop words
    """
    new_terms_list = [[]]
    print("=============in the stop_words_removal=============")
    stop = stopwords.words("english")

    for i in range(len(all_terms_list)):
        if all_terms_list[i] != []:
            if not all_terms_list[i][0] in stop:
                new_terms_list.append(
                    all_terms_list[i]
                )  # .apply(lambda x: [item for item in x if item not in stop])
    return new_terms_list


def run():
    """
    run all the functions in Pre-Processing
    """
    df = reading()
    df = normalize(df)
    df = expanding(df)
    df = tokenize(df)
    all_terms_list = return_term_list(df)
    all_terms_list = stop_words_removal(all_terms_list)
    return all_terms_list


# d = run()
# print(type(d[1][0]), type(d[1][1]), type(d[1][2]))