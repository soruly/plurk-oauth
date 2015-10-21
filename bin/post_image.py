import glob
import os
import sys
sys.path.append('plurk_oauth/')
from PlurkAPI import PlurkAPI
import getopt
import json

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

    search_dir = "/home/soruly/plurk/"
    os.chdir(search_dir)
    files = glob.glob('*')
    if len(files) > 0:
        files = [os.path.join(search_dir, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        for file in files:
            response = plurk.callAPI('/APP/Timeline/uploadPicture', {}, os.path.abspath(file))
            print response
            content = response['full']
            response = plurk.callAPI('/APP/Timeline/plurkAdd', {'content': content, 'qualifier': ':'})
            print response
            break
