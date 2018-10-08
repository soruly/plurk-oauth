import sys
sys.path.append('plurk_oauth/')
from PlurkAPI import PlurkAPI
import getopt
import json
import urllib2
import opencc

def usage():
    print '''Help Information:
    -h: Show help information
    '''

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    file = open('API.keys', 'r+')
    data = json.load(file)
    plurk = PlurkAPI(data["CONSUMER_KEY"], data["CONSUMER_SECRET"])
    if data.get('ACCESS_TOKEN'):
        plurk.authorize(data["ACCESS_TOKEN"],data["ACCESS_TOKEN_SECRET"])
    else:
        plurk.authorize()
        data["ACCESS_TOKEN"] = plurk._oauth.oauth_token['oauth_token']
        data["ACCESS_TOKEN_SECRET"] = plurk._oauth.oauth_token['oauth_token_secret']
        json.dump(data,file)

    qualifier = ':'
    request = urllib2.Request('https://v1.hitokoto.cn', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    response = urllib2.urlopen(request)
    data = json.loads(response.read().decode('utf-8'))
    content = opencc.convert(data['hitokoto'] + " [emo76]\n -- " + data['from'], config='s2t.json')
    content = content.encode('utf-8')
    source = 'http://hitokoto.cn/?id=' + str(data['id'])
    
    response = plurk.callAPI('/APP/Timeline/plurkAdd', {'content': content, 'qualifier': qualifier})
    response = plurk.callAPI('/APP/Responses/responseAdd', {'plurk_id' : response['plurk_id'], 'content': source, 'qualifier': ':'})

