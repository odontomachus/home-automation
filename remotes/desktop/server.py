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

run(host='localhost', port=8090)
