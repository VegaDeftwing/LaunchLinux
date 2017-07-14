#   0   1   2   3   4   5   6   7      8
# +---+---+---+---+---+---+---+---+
# |0/0|1/0|   |   |   |   |   |   |         0
# +---+---+---+---+---+---+---+---+
#
# +---+---+---+---+---+---+---+---+  +---+
# |0/1|   |   |   |   |   |   |   |  |   |  1
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |   |   |   |  |   |  2
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |5/3|   |   |  |   |  3
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |   |   |   |  |   |  4
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |   |   |   |  |   |  5
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |4/6|   |   |   |  |   |  6
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |   |   |   |  |   |  7
# +---+---+---+---+---+---+---+---+  +---+
# |   |   |   |   |   |   |   |   |  |8/8|  8
# +---+---+---+---+---+---+---+---+  +---+
import alsaaudio
import sys
import launchpad_py as launchpad
from pygame import time
from subprocess import call
import psutil
import i3

#Launchpad init
lp = launchpad.Launchpad();
lp = launchpad.LaunchpadMk2()


if lp.Check( 0, "mk2" ):
    lp = launchpad.LaunchpadMk2()
    if lp.Open( 0, "mk2" ):
        print("Launchpad Mk2")
        mode = "Mk2"
        lp.Reset()

single = 0
mpdstate = 1

def opendev():
    i3.workspace("Dev")
    i3.workspace("Atom")
    i3.workspace("GitKraken")
    return
# def opensecure:
#     i3.workspace("Atom")
#     i3.workspace("Atom")
#     i3.workspace("Atom")

def openchat():
    i3.workspace("GenChat")
    i3.workspace("GenChat2")
    i3.workspace("Telegram")

def openweb():
    i3.workspace("Vivaldi")
    i3.workspace("Telegram")
    i3.workspace("Atom")

def getworkspacelist():
    workspaces = i3.get_workspaces()
    workspacelist = ['default']
    for workspace in workspaces:
            name = workspace['name']
            workspacelist.append(name)
    return (workspacelist)

def verification(name):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        #print p.name()
        if p.name() == name:
            return ("running")

# print verification("vivaldi-bin")
# print verification("meh")

def getvol():
    m = alsaaudio.Mixer()
    vol = m.getvolume()
    return vol


def displayvol():
    vol = getvol()
    vol = int(vol[0])
    y = vol / 10.8
    if vol < 40:
        r = 0
        g = vol
        b = vol
    if vol > 40 and vol < 66:
        r = (vol - 50) * vol
        g = (vol - 40) * 15
        b = vol - int(vol / 1.2)
    if vol > 66:
        r = vol * vol
        g = 50  -  (vol / 2)
        b =  vol / 6 - (vol  /  7)
    if vol < 13:
        y = 0
    y = int(9 - y)

    if vol == 100:
        y = 0
        r = 255
        g = 0
        b = 0

    for i in range (int(y) , 9):
        lp.LedCtrlXY( 0, i, r, g, b )
    if int(y) != 0:
        for j in range (0, int(y)):
            lp.LedCtrlXY( 0, j, 0, 0, 0 )

def updatevol():
    bs = lp.ButtonStateXY()
    #if bs.count(0) > 1:
    if len(bs) > 1:
        if bs[0] == 0 and bs[2] == 127:
            m = alsaaudio.Mixer()
            newvol = 8 - bs[1]
            newvol = newvol * 12.5
            m.setvolume(int(newvol))
            #print newvol
            # if newvol == 100:
            #     lp.LedCtrlString( "!", 255, 0, 0, 0 )
            #     lp.Reset()
            # if newvol == 0:
            #     lp.LedCtrlString( "X", 0, 0, 255, 0 )
            #     lp.Reset()
        #print bs[0]
        #print bs[1]
        if bs[0] == 1 and bs[1] == 8 and bs[2] == 127:
            if mpdstate == 1:
                call(["mpc", "pause"])
                lp.LedCtrlXY( 1, 8, 0, 0, 0 )
                mpdstate = 0
            else:
                call(["mpc", "play"])
                lp.LedCtrlXY( 1, 8, 0, 255, 50 )
                mpdstate = 1

        if bs[0] == 1 and bs[1] == 7 and bs[2] == 127:
            call(["mpc", "next"])
            lp.LedCtrlXY( 1, 7, 0, 0, 255 )
        if bs[0] == 1 and bs[1] == 7 and bs[2] == 0:
            lp.LedCtrlXY( 1, 7, 0, 0, 0 )
        if bs[0] == 1 and bs[1] == 6 and bs[2] == 127:
            call(["mpc", "prev"])
            lp.LedCtrlXY( 1, 6, 0, 0, 255 )
        if bs[0] == 1 and bs[1] == 6 and bs[2] == 0:
            lp.LedCtrlXY( 1, 6, 0, 0, 0 )

        if bs[0] == 1 and bs[1] == 5 and bs[2] == 127:
            if single == 0:
                call(["mpc", "single","on"])
                lp.LedCtrlXY( 1, 5, 255, 0, 255 )
                single = 1
            else:
                call(["mpc", "single","off"])
                lp.LedCtrlXY( 1, 5, 0, 0, 0 )
                single = 0

def testopen():
    workspacelist = getworkspacelist()
    if "Atom" in workspacelist:
        lp.LedCtrlXY( 6, 6, 0, 255, 0 )
    else:
        lp.LedCtrlXY( 6, 6, 0, 0, 0 )

    if "Dev" in workspacelist:
        lp.LedCtrlXY( 7, 6, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 7, 6, 0, 0, 0 )

    if "GitKraken" in workspacelist:
        lp.LedCtrlXY( 5, 6, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 5, 6, 0, 0, 0 )

    if "Vivaldi" in workspacelist:
        lp.LedCtrlXY( 6, 8, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 6, 8, 0, 0, 0 )

    if "Telegram" in workspacelist:
        lp.LedCtrlXY( 7, 8, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 7, 8, 0, 0, 0 )

    if "GenChat" in workspacelist:
        lp.LedCtrlXY( 5, 8, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 5, 8, 0, 0, 0 )

    if "GenChat2" in workspacelist:
        lp.LedCtrlXY( 6, 7, 0, 0, 255 )
    else:
        lp.LedCtrlXY( 6, 7, 0, 0, 0 )

lastvol = 0

while 1:
    time.wait(50)
    bs = lp.ButtonStateXY()
    if getvol != lastvol:
        displayvol()

    lastvol = getvol()

    updatevol()
    
    if len(bs) > 1:
        if bs[0] == 6 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("Atom")
    testopen()
