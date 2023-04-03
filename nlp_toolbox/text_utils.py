from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from tqdm import tqdm
import re

def stem(text):
    porter = PorterStemmer()
    words = [porter.stem(word) for word in word_tokenize(text)]
    return ' '.join(words), len(words)

def lemmatize(text):
    lmtzr = WordNetLemmatizer()
    words = [lmtzr.lemmatize(word) for word in word_tokenize(text)]
    return ' '.join(words), len(words)


def split_in_sentences(df, text_column, target_column, abv_list=None):
    """Split every paragraph into sentences by '.' and keeps the target of the paragraph.
    A list of abbreviations that are followed by a '.' that do not  

    Args:
        df (pandas.DataFrame): containing a column with text/paragraphs
        text_column (str): name of column in df containing the paragraph
        target_column (str): name of column in df containing the target
        abv (list): _description_

    Returns:
        df (pandas.DataFrame): input DataFrame with a new column 'type' 
        and the sentences concatenated
    """
    if abv_list is None:
        abv_list = ['no', 'fig', 'in', 'inc', 'v', 'ft', 'www']
    df['type'] = 'paragraph'
    for text, target in tqdm(df[[text_column,target_column]].values):
        ## Helping the tokenizer understand abbreviations for splitting sentences
        punkt_param = PunktParameters()
        punkt_param.abbrev_types = set(abv_list)
        tokenizer = PunktSentenceTokenizer(punkt_param)
        sentences = tokenizer.tokenize(re.sub(r'\.(?=[^ \W\d])', '. ', text))
        for sent in sentences:
            df.loc[df.shape[0]] = [sent, target, 'sentence']
    print(f'Dataframe shape (after sentences splitting): {df.shape}')
    df = df.drop_duplicates()
    return df