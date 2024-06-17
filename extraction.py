# Contains functions that deal with the extraction of documents from a text file (see PR01)

import json

from document import Document

import re

def extract_collection(source_file_path: str) -> list[Document]:
    """
    Loads a text file (aesopa10.txt) and extracts each of the listed fables/stories from the file.
    :param source_file_name: File name of the file that contains the fables
    :return: List of Document objects
    """
    catalog = []  # This dictionary will store the document raw_data.


    # TODO: Implement this function. (PR02)

    with open(source_file_path, "r") as file:
        whole_text = file.read()

    # Locate the first fable
    start_match = re.search(r'\n\n\n\n  The Cock and the Pearl', whole_text)
    start_index = start_match.start()
    whole_text = whole_text[start_index:]

    # Split the text into fables
    fables = re.split(r'\n{3}(.*?)\n{2}(.*?)', whole_text, flags=re.DOTALL)
    filtered_list = [item for item in fables if item.strip()]

    # Extract title, raw text and terms
    for i in range(0, len(filtered_list),2):
        title = filtered_list[i].strip()
        raw_text = filtered_list[i + 1].replace('\n', ' ').strip()
        terms = raw_text.split()

        # Create a dictionary for each fable
        document = {
            'document_id': i // 2,
            'title': title,
            'raw_text': raw_text,
            'terms': terms
        }
        catalog.append(document)

    return catalog

def save_collection_as_json(collection: list[Document], file_path: str) -> None:
    """
    Saves the collection to a JSON file.
    :param collection: The collection to store (= a list of Document objects)
    :param file_path: Path of the JSON file
    """

    serializable_collection = []
    for document in collection:
        serializable_collection += [{
            'document_id': document.document_id,
            'title': document.title,
            'raw_text': document.raw_text,
            'terms': document.terms,
            'filtered_terms': document.filtered_terms,
            'stemmed_terms': document.stemmed_terms
        }]

    with open(file_path, "w") as json_file:
        json.dump(serializable_collection, json_file)


def load_collection_from_json(file_path: str) -> list[Document]:
    """
    Loads the collection from a JSON file.
    :param file_path: Path of the JSON file
    :return: list of Document objects
    """
    try:
        with open(file_path, "r") as json_file:
            json_collection = json.load(json_file)

        collection = []
        for doc_dict in json_collection:
            document = Document()
            document.document_id = doc_dict.get('document_id')
            document.title = doc_dict.get('title')
            document.raw_text = doc_dict.get('raw_text')
            document.terms = doc_dict.get('terms')
            document.filtered_terms = doc_dict.get('filtered_terms')
            document.stemmed_terms = doc_dict.get('stemmed_terms')
            collection += [document]

        return collection
    except FileNotFoundError:
        print('No collection was found. Creating empty one.')
        return []

print(extract_collection('raw_data/aesopa10.txt'))