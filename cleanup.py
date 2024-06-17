# Contains all functions that deal with stop word removal.
import re
from collections import Counter
from document import Document


def remove_symbols(text_string: str) -> str:
    """
    Removes all punctuation marks and similar symbols from a given string.
    Occurrences of "'s" are removed as well.
    :param text:
    :return:
    """

    # TODO: Implement this function. (PR02)

    # Remove "'s"
    text_string = re.sub(r"'s\b", '', text_string)
    # Remove punctuation and similar symbols, excluding apostrophes within words
    text_string = re.sub(r'[^\w\s\']', '', text_string)
    return text_string


def is_stop_word(term: str, stop_word_list: list[str]) -> bool:
    """
    Checks if a given term is a stop word.
    :param stop_word_list: List of all considered stop words.
    :param term: The term to be checked.
    :return: True if the term is a stop word.
    """
    term = remove_symbols(term).lower()
    return term.lower() in stop_word_list


def remove_stop_words_from_term_list(term_list: list[str], stop_word_list: list[str]) -> list[str]:
    #stop_word_list parameter was added because in my opinion this is more optimal then reading stop word file inside of the function
    #In the case of reusing this function for example in a for loop with several term lists is is more computationaly expencive to read stop word file every time
    """
    Takes a list of terms and removes all terms that are stop words.
    :param term_list: List that contains the terms
    :param stop_word_list: List that contains the stop words
    :return: List of terms without stop words
    """

    no_stop_terms = [remove_symbols(term) for term in term_list if not is_stop_word(term, stop_word_list)]
    return no_stop_terms

def filter_collection(collection: list[list], stop_word_list: list[str]):
    #stop_word_list parameter was added because in my opinion this is more optimal then reading stop word file inside of the function
    #In the case of reusing this function for example in a for loop with several term lists is more computationaly expencive to read stop word file every time
    """
    For each document in the given collection, this method takes the term list and filters out the stop words.
    Warning: The result is NOT saved in the documents term list, but in an extra field called filtered_terms.
    :param collection: Document collection to process
    """
    # Hint:  Implement remove_stop_words_from_term_list first and use it here.
    # TODO: Implement this function. (PR02)
    for terms_list in collection:
        filtered_terms = remove_stop_words_from_term_list(terms_list, stop_word_list)
    return filtered_terms



def load_stop_word_list(raw_file_path: str) -> list[str]:
    """
    Loads a text file that contains stop words and saves it as a list. The text file is expected to be formatted so that
    each stop word is in a new line, e.g. like englishST.txt
    :param raw_file_path: Path to the text file that contains the stop words
    :return: List of stop words
    """
    # TODO: Implement this function. (PR02)
    with open(raw_file_path, 'r') as file:
        stop_words = [line.strip() for line in file if line.strip()]
    return stop_words

def create_stop_word_list_by_frequency(collection: list[Document], high_freq_cutoff: float = 0.01, low_freq_cutoff: float = 0.01) -> list[str]:
    """
    Uses the method of J. C. Crouch (1990) to generate a stop word list by finding high and low frequency terms in the
    provided collection.
    :param collection: Collection to process
    :param high_freq_cutoff: High frequency cutoff as a percentage (0.01 means top 1%)
    :param low_freq_cutoff: Low frequency cutoff as a percentage (0.01 means bottom 1%)
    :return: List of stop words
    """
    term_counter = Counter()
    for document in collection:
        term_counter.update(document.terms)

    total_terms = sum(term_counter.values())
    term_frequencies = {term: count / total_terms for term, count in term_counter.items()}

    # Sort terms by frequency
    sorted_terms = sorted(term_frequencies.items(), key=lambda item: item[1], reverse=True)

    # Determine high frequency and low frequency thresholds
    num_terms = len(sorted_terms)
    high_freq_threshold = int(num_terms * high_freq_cutoff)
    low_freq_threshold = int(num_terms * low_freq_cutoff)

    high_freq_terms = [term for term, _ in sorted_terms[:high_freq_threshold]]
    low_freq_terms = [term for term, _ in sorted_terms[-low_freq_threshold:]]

    stop_words = set(high_freq_terms + low_freq_terms)
    return list(stop_words)

def main():
    list1 = load_stop_word_list("raw_data/aesopa10.txt")
    list2 = load_stop_word_list('raw_data/englishST.txt')
    print(filter_collection([list1], list2))

if __name__ == "__main__":
    main()