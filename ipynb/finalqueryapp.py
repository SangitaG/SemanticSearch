# Import my functions from 
import lib.wiki_utilities as wiki
import lib.mongo_utilities as mongo
import lib.general_utilities as gu

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import time
from IPython.core.display import display, HTML
import webbrowser

#*********** read pickled data. ************

# read the aggregate collection dataframe. 
BS_ML_collection_df = pd.read_pickle('data/BS_ML_collection_df.obj')

# read pickled document_term_matrix and tfidf transformer.
tfidf_vectorizer = gu.read_pickle_obj('data/tfidf_vectorizer_fit_transformed.obj')
document_term_matrix = gu.read_pickle_obj('data/document_term_matrix.obj')

# read pickled SVD transformed corpus and SVD transformer.
SVD = gu.read_pickle_obj('data/SVD_500_fit_transformed.obj')
SVD_corpus = gu.read_pickle_obj('data/SVD_corpus.obj')

# query app
def run_query_app():
    query = input("\nType wiki query(q to exit): ")
    while(query != 'q'):

        # encode query, svd query, calculate the cosine simiarity of query to
        # the corpus data
        tf_query = tfidf_vectorizer.transform([query])
        svd_query = SVD.transform(tf_query)
        cosine_sim_query_to_corpus = cosine_similarity(SVD_corpus, svd_query)

        # find the top 5 most similar pages for the query.
        ind = cosine_sim_query_to_corpus.argsort(axis = 0)[::-1]
        top5_pages = [ind[i][0] for i in range(5)]
        selected_pgs_df = BS_ML_collection_df.loc[top5_pages, :]
        page_titles = selected_pgs_df.title.values

        # display top 5 pages for the query, as weblinks.
        print("\n***** Here are the top 5 wiki page links for your query: *****\n")

        for pg_title in page_titles:
            pg_title_no_sp = pg_title.replace(' ', '_')

            url=("<a href='https://www.wikipedia.org/wiki/" +
                 pg_title_no_sp +
                 "' target='_blank'>" +
                 pg_title +
                 "</a>")

#           display(HTML(url))
#           display(pg_title)
            display("https://www.wikipedia.org/wiki/" +
                     pg_title_no_sp)
                
        time.sleep(0.1) # Time in seconds.    
        query = input("\nEnter wiki query(q to exit): ")

# run the final query app from the command line.
import os
os.system('clear')  # For Linux/OS X
run_query_app()