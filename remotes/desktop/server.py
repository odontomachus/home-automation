#!/usr/bin/python
from bottle import get, run, redirect
import app

@get('/')
def index():
    global bedroom, livingroom
    livingroom_status = livingroom.status()
    bedroom_status = bedroom.status()
    livingroom_color = "green" if livingroom_status else "red"
    color_conv = lambda x: 'red' if x == 0 else "#00{:02x}00".format(x)
    bedroom_color = map(color_conv, bedroom_status)
    bedroom_toggle = "off" if bedroom_status == (0,0) else "on"

    template = """
    <p><span style="background-color:{livingroom_color};display:block;float:left;width:10px;height:1em;margin:0 8px;"></span>
    Switch light <a href="livingroom/switch">here</a></p>
    <p>Switch bed lamp <a href="bedroom/{bedroom_toggle}">here</a><p>
    <p><span style="background-color:{bedroom_left_color};display:block;float:left;width:10px;height:1em;margin:0 8px;"></span>
    <span style="background-color:{bedroom_right_color};display:block;float:left;width:10px;height:1em;margin:0 8px;"></span>
    Switch bed lamp <a href="bedroom/{bedroom_toggle}">here</a><p>
    """.format(livingroom_color=livingroom_color, bedroom_right_color=bedroom_right_color, bedroom_left_color=bedroom_left_color, bedroom_toggle=bedroom_toggle)
    return template

@get('livingroom/switch')
def switch():
    global livingroom
    livingroom.toggle()
    redirect("/")

@get('bedroom/on')
def switch():
    global bedroom
    bedroom.on()
    redirect("/")

@get('bedroom/off')
def switch():
    global bedroom
    bedroom.on()
    redirect("/")

@get('bedroom/<side:re:left|right>/<val:re:[0-2]?\d?\d>')
def switch(val):
    global bedroom
    bedroom.left(val)
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
            try:
                pidfile = os.environ['PIDFile']
            except KeyError as e:
                pidfile = '/var/run/lightswitch/lightswitch.pid'
            try:
                pidfd = os.open(pidfile,
                                os.O_CREAT | # create file
                                os.O_TRUNC | # truncate it, if it exists
                                os.O_WRONLY | # write-only
                                os.O_EXCL, # exclusive access
                                0o644) # file mode

            except Exception as e:
                print('Could not create pidfile {pidfile}'.format(pidfile=pidfile), file=sys.stderr)
                sys.exit(1)

            os.write(pidfd, bytes("{pid}\n".format(pid=os.getpid()), 'utf-8'))
            os.fsync(pidfd)
            global livingroom, bedroom
            livingroom = app.LivingRoomSwitch()
            bedroom = app.BedRoomSwitch()
            run(host='0.0.0.0', port=8090)
        else:
            sys.exit()    #First child exits for decoupling
    else:
        sys.exit()   # Parent exits
