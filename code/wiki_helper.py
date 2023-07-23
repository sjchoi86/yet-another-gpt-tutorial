
import requests
from bs4 import BeautifulSoup

def wiki_search(entity       = "President of South Korea",
                min_char_len            = 100, # minimum number of characters in a paragraph
                first_k                 = 5,   # 'first_k' paragraphs to be included
                top_m_excluding_first_k = 3,   # get 'top_m' exluding 'first_k' making the total 'k+m'
                VERBOSE                 = True
            ):
    """
        This function return a number of paragraphs for searching an entity in Wikipedia
    """
    # First, search `en.wikipedia.org` to get page
    entity_       = entity.replace(" ", "+")
    search_url    = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    response_text = requests.get(search_url).text
    soup          = BeautifulSoup(response_text, features="html.parser")
    result_divs   = soup.find_all("div", {"class": "mw-search-result-heading"})
    
    if result_divs:  # entity mismatch occurs
        # Get related wiki pages
        results = []
        for div in result_divs:
            link   = div.find('a')
            title  = link.text
            url    = link['href']
            result = {'title': title, 'url': url}
            results.append(result)
        
        # Use the first matched wiki page
        entity_new    = results[0]['title']
        search_url    = f"https://en.wikipedia.org/w/index.php?search={entity_new}"
        response_text = requests.get(search_url).text
        soup          = BeautifulSoup(response_text, features="html.parser")
        page          = [p.get_text().strip() for p in soup.find_all("p") + soup.find_all("ul")]
        
        if VERBOSE: # Debug print
            print ("entity:[%s] mismatched. use [%s] instead."%(entity,entity_new))
    else:
        page = [p.get_text().strip() for p in soup.find_all("p") + soup.find_all("ul")]
        
        if VERBOSE: # Debug print
            print ("entity:[%s] matched."%(entity))
    # Then, clean some strings
    def clean_str(p):
        p = p.replace('\\', '/') # <= Debug using GPT and it works!
        p_encode = p.encode()
        p_decode = p_encode.decode("unicode-escape")
        p_encode2 = p_decode.encode('latin1')
        p_decode2 = p_encode2.decode('utf-8')
        return p_decode2
    page_clean = ""
    for p in page:
        page_clean += clean_str(p)
        if not p.endswith('\n'):
            page_clean += '\n'
    paragraphs = page_clean.split("\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    if VERBOSE:
        print (" We have total [%d] paragraphs."%(len(paragraphs)))
        
    # Second, get some paragraphs
    paragraphs_filtered = [p for p in paragraphs if len(p) >= min_char_len]
    paragraphs_first_k  = paragraphs_filtered[:first_k]
    praagraphs_remain   = paragraphs_filtered[first_k:]
    paragraphs_sorted   = sorted(praagraphs_remain,key=len,reverse=True)
    paragraphs_top_m    = paragraphs_sorted[:top_m_excluding_first_k]
    paragraphs_return   = paragraphs_first_k + paragraphs_top_m
    
    if VERBOSE: # Debug print
        print (" After filtering, we have [%d] and [%d] paragraphs returned (k:[%d] and m:[%d])"%
           (len(paragraphs_filtered),len(paragraphs_return),first_k,top_m_excluding_first_k
           ))
        
    # Return filtered paragraphs
    return paragraphs_return
