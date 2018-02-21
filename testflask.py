#!/usr/bin/env python3
__version__ = "1.0.0"
__author__ = "Ersin Akyuz"
__email__ = "eakyuz@gmx.net"
__description__ = "Python Github API Browser"

from flask import Flask

app = Flask(__name__)
@app.route("/retrieve", methods=['GET'])
def retrieve(search_term):
        return "Ada vapuru yandan carkli"
retrieve("ersin")
if __name__ == "__main__":
    app.run()

