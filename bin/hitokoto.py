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
    response = urllib2.urlopen('http://api.hitokoto.cn/?c=a&encode=json')
    data = json.loads(response.read().decode('utf-8'))
    content = opencc.convert(data['hitokoto'] + " [emo76]\n -- " + data['from'], config='s2t.json')
    content = content.encode('utf-8')
    source = 'http://hitokoto.cn/?id=' + str(data['id'])
    
    response = plurk.callAPI('/APP/Timeline/plurkAdd', {'content': content, 'qualifier': qualifier})
    response = plurk.callAPI('/APP/Responses/responseAdd', {'plurk_id' : response['plurk_id'], 'content': source, 'qualifier': ':'})

