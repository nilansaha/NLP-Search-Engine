from bs4 import BeautifulSoup
import re
import urllib
import urllib2
import time

def search(query, noOfPages):
    pages = noOfPages
    start = 0
    results = []
    for i in range(pages):
        search_term = urllib.quote(query)
        url = "http://www.google.com/search?q=" + search_term +"&start=" + str(start)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url).read()

        soup = BeautifulSoup(response, "lxml")
        mydivs = soup.find_all("h3", attrs={'class' : 'r'})
        length_of_results = len(mydivs)
        if start == 0:
            start = length_of_results + 1
        else:
            start = start + length_of_results + 1
        for i in mydivs:
            try:
                div = str(i.a['href'])
                text = i.text
                inner = []
                div = re.search('url\?q=(.*)&sa=', div)
                div = div.group(1)
                url = urllib2.unquote(div)
                inner.append(text)
                inner.append(url)
                results.append(inner)
            except:
                print "Error parsing url"
    return results