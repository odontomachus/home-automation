#!/usr/bin/python
from bottle import get, run, redirect
import app

a = app.App()

@get('/')
def index():
    global a
    status = a.status()
    color = "green" if status else "red"
    template = """
    <span style="background-color:{color};display:block;float:left;width:10px;height:1em;margin:0 8px;"></span>
    Switch light <a href="/switch">here</a>
    """.format(color=color)
    return template

@get('/switch')
def switch():
    global a
    a.toggle()
    redirect("/")

# Run in background
if __name__=="__main__":
    import os
    import sys
    pid = os.fork()
    if (pid == 0):
        os.chdir("/")
        os.setsid()
        os.umask(0)
        pid2 = os.fork()
        if (pid2 == 0):  # Second child
            run(host='0.0.0.0', port=8090)
        else:
            sys.exit()    #First child exits for decoupling
    else:
        sys.exit()   # Parent exits
