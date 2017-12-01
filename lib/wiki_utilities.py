import requests
from tqdm import tqdm

def get_wiki_data(url_api, params):
    
    '''This function gets data requested from a specified api url.
       url_api: a url to api such as "https://en.wikipedia.org/w/api.php?"
       params : a dictionary to setup the fetch request'''
    
    response = requests.get(url_api, params=params)
    return(response.json())

def get_wiki_pages(url_api, params, tree_depth):

    '''This function recursively gets all pages, from the top level and subcategories,
       for the specified category, in the params dictionary.       
       url_api: a url to api such as "https://en.wikipedia.org/w/api.php?"
       params : a dictionary to setup the fetch request'''
    
    # fetch data.
    data = get_wiki_data(url_api, params)
    
    # Pages in category.
    pages = [{'pageid':entry['pageid'], 'title':entry['title']} 
             for entry in data['query']['categorymembers'] if entry['ns']==0]

    # subcategories in this category
    sub_categories = [{'pageid':entry['pageid'], 'title':entry['title']}
                      for entry in data['query']['categorymembers'] if entry['ns']==14]
    
    
    # If there are subcategories in this category's page, also get their pages.
    if ((len(sub_categories) != 0) & (tree_depth != 0)):
        tree_depth -=1
        for category in sub_categories:
            
            # Update the category we want to fetch as this current subcategory
            params["cmtitle"] = category['title']
            
            # Recursively get all pages and subcategory pages for this 
            # current subcategory
            pgs = get_wiki_pages(url_api, params=params, tree_depth=tree_depth)
            
            # append all pages from this current subcategory
            pages += pgs            
        
    return(pages)

def get_wiki_full_category_page_list(category, tree_depth):
    
    '''This function gets the entire requested data, for a category.
       category : a wiki page category, such as "Category:machine_learning"'''

    # url address of site's api, which we want to scrape.
    url_api = "https://en.wikipedia.org/w/api.php?"

    params = {
    "action": "query",
    "format": "json",
    "list": "categorymembers",
    "cmtitle": category,
    "cmlimit": "max"}  
    
    full_page_list = get_wiki_pages(url_api, params, tree_depth)
    return(full_page_list)

def get_wiki_page_content(page_title, page_ID):
    
    '''This function extracts the content for the requested page.
       page_title : title of wiki page
       page_ID    : the id of the page"'''

    # url address of site's api, which we want to scrape.
    url_api = "https://en.wikipedia.org/w/api.php?"

    params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "titles": page_title,
    "exlimit": "max"
    }
    
    # extracts contents of the specified page.
    data = get_wiki_data(url_api, params) 
    page_content = data['query']['pages'][page_ID]['extract']
    
    return(page_content)

def get_wiki_full_category_content(category, tree_depth):
    
    '''This function gets the content for all the pages/subpages of the requested category.
       Top-level function. Call this function with a specified category.
       category : a wiki page category, such as "Category:machine_learning"'''
    
    # retrieve a list of dictionaries with all the pages and subpages related to this wiki category.
    entire_category_page_lst = get_wiki_full_category_page_list(category, tree_depth)
    
    # get the text of wiki pages and add them to that pages' dictionary, with key value 'text'
    for page_dict in tqdm(entire_category_page_lst):
        page_dict['text'] = get_wiki_page_content(page_dict['title'], str(page_dict['pageid']))

    return(entire_category_page_lst)

