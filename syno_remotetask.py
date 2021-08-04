#!/usr/bin/env python3
# v1.0
# -*- coding: utf-8 -*-
#


from flask import Flask, render_template, session, redirect,  request
from flask import send_file
from jinja2 import TemplateNotFound

import os
# from os import path
import json
import logging
import logging.handlers
import subprocess
from datetime import datetime

# ######################################################################################


def get_local_path():
    '''
    Get local filesystem path

    Parameters:
        -

    Returns:
        ret (string): path to local directory
    '''
    ret = ""

    try:
        ret = os.path.dirname(os.path.abspath(__file__))
    except Exception as err:
        pass
    return ret


def load_json(local_filename):
    '''
    [GENERAL] Load a JSON from local filesystem

    Parameters:
        local_filename (str): filename to be loaded

    Returns:
        ret (string): Cleaned HTML code or None if failed
    '''

    try:
        with open(local_filename, "r") as file:
            ret = json.load(file)
    except Exception as err:
        ret = None
    return ret


def log(message):
    f = open(get_local_path()+"/log.txt", 'a')
    message = "{time} {message}".format(time=str(datetime.now()), message=message)
    print(message, file=f)

# ######################################################################################

app = Flask(__name__)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    log("===== ROUTE: /                      =====")
    try:
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(path)
    except TemplateNotFound as err:
        try:
            # Serve the file (if exists) from app/templates/FILE.HTML
            path += ".html"
            return render_template(path)
        except Exception as err:
            return redirect("/")


@app.route('/<magickey>')
@app.route('/<magickey>/')
@app.route('/<magickey>/<identifier>')
def task(magickey="", identifier=0):
    log("===== ROUTE: /magickey/identifier   =====")

    found = False

    # reload config to get latest task ids
    config = load_json(get_local_path()+"/config.json")

    page = {}

    try:
        if magickey == config["server"]["magickey"]:
            tasks = config["tasks"]
            for taskid in tasks:
                if identifier == tasks[taskid]["identifier"]:
                    page["taskid"] = taskid
                    if tasks[taskid]["command"] != "":
                        log("Found command, executing...")
                        log("Executing: {}".format(tasks[taskid]["command"]))

                        process = subprocess.Popen(tasks[taskid]["command"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        # wait for the process to terminate
                        out, err = process.communicate()
                        errcode = process.returncode

                        log("Output (err={err}): {out}".format(err=errcode, out=out))
                    else:
                        log("Found task id '{id}', executing...".format(id=taskid))
                        # start task in taskmanager
                        # ...
                        process = subprocess.Popen(['synoschedtask', '--run', 'id={}'.format(taskid)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                        print(stdout, stderr)

                    log("Done.")
                    log("")
                    return render_template("task.html", page=page)
    except Exception as err:
        log("ERROR: {err}".format(err=getattr(err, 'message', repr(err))))
        log("ERROR: {err}".format(err=getattr(err, 'message', str(err))))
        pass

    return redirect("/")

# ######################################################################################


config = load_json(get_local_path()+"/config.json")

if __name__ == '__main__':
    app.run(debug=config["server"]["debug"], host=config["server"]["listen"], port=config["server"]["port"])