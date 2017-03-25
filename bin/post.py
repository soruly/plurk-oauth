import glob
import os
import sys
import time
sys.path.append('plurk_oauth/')
from PlurkAPI import PlurkAPI
import getopt
import json
import re
from random import randint

def usage():
    print '''Help Information:
    -h: Show help information
    '''
time.sleep(randint(0,0))
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
        content = ''
        sources = []
        files = [os.path.join(search_dir, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        for file in files:
            response = plurk.callAPI('/APP/Timeline/uploadPicture', {}, os.path.abspath(file))
            print response
            if len(content + response['full'] + ' ') >= 310:
                break
            content = content + response['full'] + ' '
            match_pixiv = re.findall(r'(\d+)_p\d+.*\.(?:jpg|png|bmp|gif)', file)
            match_twitter = re.findall(r'twitter\.com(\S+)status(\d+).*\.(?:jpg|png|bmp|gif)', file)
            print match_twitter
            if len(match_pixiv) > 0:
                sources.append('http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+match_pixiv[0])
            elif len(match_twitter) > 0:
                sources.append('https://twitter.com/'+match_twitter[0][0]+'/status/'+match_twitter[0][1])
            os.remove(file)
        response = plurk.callAPI('/APP/Timeline/plurkAdd', {'content': content, 'qualifier': ':'})
        print response
        for source in sources:
            response = plurk.callAPI('/APP/Responses/responseAdd', {'plurk_id' : response['plurk_id'], 'content': source, 'qualifier': ':'})
            print response
