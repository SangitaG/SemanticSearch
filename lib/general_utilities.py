import pickle
import re
from tqdm import tqdm

# clean text.
def cleaner(text):
    TAG_RE = re.compile(r'<[^>]+>')
    text = TAG_RE.sub('', text)
    text = re.sub('\n', '', text)
                  
    return(text)

def clean_text(page_lst):
    for page in tqdm(page_lst):
        page['text'] = cleaner(page['text'])
    
    return(page_lst)

# pickle list of dictionaries for each page in the category: machine learning.
def pickle_obj(filename, objname):
    filehandler = open(filename,"wb")
    pickle.dump(objname,filehandler)

# read pickled list of dictionaries for each page in the category: machine learning.
def read_pickle_obj(filename):
    file = open(filename,'rb')
    object_content = pickle.load(file)
                            
    return(object_content)