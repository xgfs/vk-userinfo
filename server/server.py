# -*- coding: utf-8 -*-

import sys, traceback
import json
import re
import os
from flask import Flask, render_template, request

import suggest

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            uid = int(request.form['uid'])
            print uid
            if uid < 1 or uid > 1000000:
               raise Exception()
            results = suggest.suggest(uid)
        except:
            errors.append(
                "Input error! User id is integer from 1 to 1000000."
            )
            return render_template('index.html', errors=errors)
    
    return render_template('index.html', errors=errors, results=results)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1488)

