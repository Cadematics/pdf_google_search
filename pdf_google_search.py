import subprocess
import os
import sys
import requests
from google.google import search

config = {
    'base_path':'/Users/cadencemo/Desktop/simoFolder/pdfsearch',
    'pdf':True
}

folder = None
searches = None
search_folder = None
number_results = None

def parseArgs(obj):
    globals()['folder'] = obj[1]
    globals()['number_results'] = int(obj[2])
    globals()['searches'] = obj[3:]

def setTopLevelFolder():
    globals()['top_level_folder'] = \
        os.path.join(config.get('base_path'), 'pysearch_results')
    try:
        assert(os.path.exists(top_level_folder))
    except AssertionError:
        os.makedirs(top_level_folder)

def setSearchFolder(foldername):
    globals()['search_folder'] = \
        os.path.join(top_level_folder, foldername)
    try:
        assert(os.path.exists(search_folder))
    except AssertionError:
        os.makedirs(search_folder)

def runQuery(searches, search_folder, number_results):
    print ('searches: ', searches)
    print ('search folder: ', search_folder)
    print ('number of results: ', number_results)
    for query in searches:
        print ("query", query )
        if config.get('pdf'):
            query += ' filetype:pdf'
            print ("CURRENTLY QUERYING", query)
        #print "search(query, stop=number_results)", search(query, stop=number_results)

        for url in search(query, number_results):
            name = (url.link).split('/')[-1]
            print (name[-4:])
            if name[-4:] == '.pdf':
                print ('url: {}'.format(url.link))
                path = os.path.join(search_folder, name)
                try:
                    assert(os.path.exists(path))
                except:
                    with open(path, 'wb') as f:
                        response = None
                        try:
                            response = requests.get(url.link)
                            print ("response: {}".format(response))
                        except:
                            pass
                        if response:
                            #print path
                            f.write(response.content)
    subprocess.check_call(
        "open %s"%(search_folder), 
        shell=True, 
        stdout=subprocess.PIPE, 
        stdin=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

if __name__ == '__main__':
    setTopLevelFolder()
    parseArgs(sys.argv)
    setSearchFolder(folder)
    print (search_folder)
    runQuery(searches, search_folder, number_results)





