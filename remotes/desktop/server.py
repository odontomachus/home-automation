from bottle import get, run, template, redirect

import app

a = app.App()

@get('/')
def index():
    return 'Switch light <a href="/switch">here</a>'

@get('/switch')
def switch():
    a.toggle()
    redirect("/")

run(host='localhost', port=8090)
