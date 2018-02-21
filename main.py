#!/usr/bin/env python3
__version__ = "1.0.0"
__author__ = "Ersin Akyuz"
__email__ = "eakyuz@gmx.net"
__description__ = "Python Github API Browser"
import json
from datetime import datetime
import requests
from flask import Flask, render_template, request
GIT_API_URL = 'https://api.github.com'
GIT_API_COMMIT_URL = 'https://api.github.com/repos/'
API_TOKEN = 'ENTERYOURAPIKEY'
MYHEADERS = {'Authorization': 'token %s' % API_TOKEN}
"""
I used my GitHub Token in MYHEADERS for unlimited calls.
requests and flask library needed for run the code. 
"""
app = Flask(__name__)
@app.route("/navigator", methods=['GET'])
def navigator():
    """
    Access to Github API and retrieve the latest commits
    """
    search_term = request.args.get('search_term', '')
    if len(search_term) > 0:
        url = "https://api.github.com/search/repositories?q=" + search_term + "&page=1&per_page=5&sort=updated&order=desc"
        try:
            my_request = requests.get(url, headers=MYHEADERS)
            dataj = json.loads(my_request.text)
            repodict = {}
            for idx, items in enumerate(dataj['items']):
                repodict[idx] = {}
                repodict[idx]['name'] = items['name']
                repodict[idx]['owner'] = items['name']
                repodict[idx]['url'] = items['owner']['url']
                repodict[idx]['order'] = idx + 1 #index
                repodict[idx]['avatar_url'] = items['owner']['avatar_url']
                repodict[idx]['login'] = items['owner']['login']
                repodict[idx]['updated_at'] = datetime.strptime(items['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
                repo_url = GIT_API_COMMIT_URL + items['owner']['login'] + "/" + items['name'] + "/commits"
                try:
                    repo_request = requests.get(repo_url, headers=MYHEADERS)
                    repo_data = json.loads(repo_request.text)
                    last_commit = repo_data[0]
                    repodict[idx]['sha'] = last_commit['sha']
                    repodict[idx]['commit_message'] = last_commit['commit']['message']
                    repodict[idx]['commit_author_name'] = last_commit['commit']['author']['name']
                except:
                    return "Error getting Repo Data"
        except:
            return "Error accessing Github API"
    else:
        return "Missing search_term<br/> " \
               "Usage: <a href='http://localhost:9876/navigator?search_term=arrow'>http://localhost:9876/navigator?search_term=arrow</a>"
    return render_template('template.html', search_term=search_term, items=repodict)
if __name__ == "__main__":
    app.run(port="9876")
