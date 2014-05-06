import urllib
import json as m_json

def google(terms): # google <search term>
    '''Returns the link and the description of the first result from a google
    search
    '''
    #query = raw_input ( 'Query: ' )
    query=terms
    print "going to google %s" % query
    query = urllib.urlencode ( { 'q' : query } )
    response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
    json = m_json.loads ( response )
    results = json [ 'responseData' ] [ 'results' ]
    returnval=""
    for result in results:
        title = result['title']
        url = result['url']   # was URL in the original and that threw a name error exception
        #print ( title + '; ' + url )
        title=title.translate({ord(k):None for k in u'<b>'})
        title=title.translate({ord(k):None for k in u'</b>'})
        returnval += title + ' ; ' + url + '\n'
        
    print "returning %s" %returnval
    return returnval.encode('utf-8')
