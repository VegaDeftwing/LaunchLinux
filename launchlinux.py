!/usr/bin/python2
# coding: latin-1

#   0   1   2   3   4   5   6   7      8
# +---+---+---+---+---+---+---+---+
# |0/0|1/0|2/0|3/0|4/0|5/0|6/0|7/0|         0
# +---+---+---+---+---+---+---+---+
#
# +---+---+---+---+---+---+---+---+  +---+
# |0/1|1/1|2/1|3/1|4/1|5/1|6/1|7/1|  |8/1|  1
# +---+---+---+---+---+---+---+---+  +---+
# |0/2|1/2|2/2|3/2|4/2|5/2|6/2|7/2|  |8/2|  2
# +---+---+---+---+---+---+---+---+  +---+
# |0/3|1/3|2/3|3/3|4/3|5/3|6/3|7/3|  |8/3|  3
# +---+---+---+---+---+---+---+---+  +---+
# |0/4|1/4|2/4|3/4|4/4|5/4|6/4|7/4|  |8/4|  4
# +---+---+---+---+---+---+---+---+  +---+
# |0/5|1/5|2/5|3/5|4/5|5/5|6/5|7/5|  |8/5|  5
# +---+---+---+---+---+---+---+---+  +---+
# |0/6|1/6|2/6|3/6|4/6|5/6|6/6|7/6|  |8/6|  6
# +---+---+---+---+---+---+---+---+  +---+
# |0/7|1/7|2/7|3/7|4/7|5/7|6/7|7/7|  |8/7|  7
# +---+---+---+---+---+---+---+---+  +---+
# |0/8|1/8|2/8|3/8|4/8|5/8|6/8|7/8|  |8/8|  8
# +---+---+---+---+---+---+---+---+  +---+

#TODO: don't use pygame time, it's huge.
import alsaaudio
import sys
import launchpad_py as launchpad
from pygame import time
from subprocess import call
import psutil
import i3

print("Starting LaunchLinux, a python based hardware linux control panel using the Novation Launchpad")
print("Version 2.2")
print("Project by VegaDeftwing")
print("Launchpad.py by FMMT666")
print("Special Thanks to FMMT66 for helping me with a facepalm moment.")
print("i3 python by Ziberna")

#### VERSION HISTORY ####
# 1.0 intital creation, volume only
# 1.1 added MPD control, uploaded to GitHub
# 2.0 added i3 control
# 2.1 improved i3 control
# 2.2p removed mpd control temporarily,
#       setup TODOs and NOTEs for further
#       advancement, some code moved, meh

### TODO: put config vars here, inc workspace and active modules

#State Tracking, inital state config
single = 0
mpdstate = 1

#Launchpad init
lp = launchpad.Launchpad();
lp = launchpad.LaunchpadMk2()
if lp.Check( 0, "mk2" ):
    lp = launchpad.LaunchpadMk2()
    if lp.Open( 0, "mk2" ):
        mode = "Mk2"
        lp.Reset()

print("Launchpad Mk2 opened, I hope?")

#Workspace groups to be opened by corosponding launch arrows,
#if you change the function name be sure to change it where it's called too!

def opendev():
    i3.workspace("Dev")
    i3.workspace("Atom")
    i3.workspace("GitKraken")
    print("Dev Workspaces Opened")

# def opensecure:
#     i3.workspace("Atom")
#     i3.workspace("Atom")
#     i3.workspace("Atom")

def openchat():
    i3.workspace("GenChat")
    i3.workspace("GenChat2")
    i3.workspace("Telegram")
    print("Chat Workspaces Opened")

def openweb():
    i3.workspace("Vivaldi")
    i3.workspace("Telegram")
    i3.workspace("GenChat")
    print("Web Workspaces Opened")

#Get names of workspaces that are open
def getworkspacelist():
    workspaces = i3.get_workspaces()
    workspacelist = ['default']
    for workspace in workspaces:
            name = workspace['name']
            workspacelist.append(name)
    return (workspacelist)

#Get the number associtated with the open workspaces
# NOTE: i3-msg will return -1 for all unnamed workspaces
# so the list can and probably will contain multiple '-1's
def getworkspacenumlist():
    workspaces = i3.get_workspaces()
    workspacenumlist = ['default']
    for workspace in workspaces:
            num = workspace['num']
            workspacenumlist.append(num)
    return (workspacenumlist)

### Verify a progarm is running
# def verification(name):
#     for pid in psutil.pids():
#         p = psutil.Process(pid)
#         #print p.name()
#         if p.name() == name:
#             return ("running")

#Get the current volume of the system using alsaaudio
def getvol():
    m = alsaaudio.Mixer()
    vol = m.getvolume()
    return vol

# TODO: This code is a mess, and still has ligting issues at low volums

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

# TODO:
#def gettemp():
#def displaytemp():
# NOTE: reuse code from display vol and try to paramaterize
# for easy gradiants and more customizeablity, including x pos

# TODO:
# NOTE: display the following using a single 'pixel'
# and the built in launchpad colors so we get decent speed
# def CPUusage():
# def RAMusage():

def updatevol(bs):
    if len(bs) > 1:
        if bs[0] == 0 and bs[2] == 127:
            m = alsaaudio.Mixer()
            newvol = 8 - bs[1]
            newvol = newvol * 12.5
            m.setvolume(int(newvol))

            ################################################
            #TODO: Make MPD control less awful,            #
            # paramaterize using a new 'MDP' funciton      #
            # and pass in the plays and the pause          #
            # possibly make a seperate 'button' funcion    #
            # for the entire program so I don't have       #
            # to have so many redundant if's to check if   #
            # the button isn't active to set it to off,    #
            # storing these as local states would be much  #
            # faster, but, I worry that lights may 'stick' #
            ################################################

        # if bs[0] == 1 and bs[1] == 8 and bs[2] == 127:
        #     if mpdstate == 1:
        #         call(["mpc", "pause"])
        #         lp.LedCtrlXY( 1, 8, 0, 0, 0 )
        #         mpdstate = 0
        #     else:
        #         call(["mpc", "play"])
        #         lp.LedCtrlXY( 1, 8, 0, 255, 50 )
        #         mpdstate = 1
        #
        # if bs[0] == 1 and bs[1] == 7 and bs[2] == 127:
        #     call(["mpc", "next"])
        #     lp.LedCtrlXY( 1, 7, 0, 0, 255 )
        # if bs[0] == 1 and bs[1] == 7 and bs[2] == 0:
        #     lp.LedCtrlXY( 1, 7, 0, 0, 0 )
        # if bs[0] == 1 and bs[1] == 6 and bs[2] == 127:
        #     call(["mpc", "prev"])
        #     lp.LedCtrlXY( 1, 6, 0, 0, 255 )
        # if bs[0] == 1 and bs[1] == 6 and bs[2] == 0:
        #     lp.LedCtrlXY( 1, 6, 0, 0, 0 )
        #
        # if bs[0] == 1 and bs[1] == 5 and bs[2] == 127:
        #     if single == 0:
        #         call(["mpc", "single","on"])
        #         lp.LedCtrlXY( 1, 5, 255, 0, 255 )
        #         single = 1
        #     else:
        #         call(["mpc", "single","off"])
        #         lp.LedCtrlXY( 1, 5, 0, 0, 0 )
        #         single = 0

def testopen():
    workspacelist = getworkspacelist()
    workspacenumlist = getworkspacenumlist()

    #TODO: using a button state test from above,
    # set all of these checks into a function so we're not redundantly turring the light off,
    # or, at least if we are, refactoring is easier

    if "Atom" in workspacelist:
        lp.LedCtrlXY( 6, 6, 0, 255, 25 )
    else:
        lp.LedCtrlXY( 6, 6, 0, 0, 0 )

    if "Dev" in workspacelist:
        lp.LedCtrlXY( 7, 6, 255, 0, 140 )
    else:
        lp.LedCtrlXY( 7, 6, 0, 0, 0 )

    if "GitKraken" in workspacelist:
        lp.LedCtrlXY( 5, 6, 20, 0, 131 )
    else:
        lp.LedCtrlXY( 5, 6, 0, 0, 0 )

    if "Vivaldi" in workspacelist:
        lp.LedCtrlXY( 6, 8, 255, 0, 0 )
    else:
        lp.LedCtrlXY( 6, 8, 0, 0, 0 )

    if "Telegram" in workspacelist:
        lp.LedCtrlXY( 5, 8, 00, 215, 255 )
    else:
        lp.LedCtrlXY( 5, 8, 0, 0, 0 )

    if "GenChat" in workspacelist:
        lp.LedCtrlXY( 7, 8, 86, 66, 255 )
    else:
        lp.LedCtrlXY( 7, 8, 0, 0, 0 )

    if "GenChat2" in workspacelist:
        lp.LedCtrlXY( 6, 7, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 6, 7, 0, 0, 0 )

    if 1 in workspacenumlist:
        lp.LedCtrlXY( 2, 6, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 2, 6, 0, 0, 0 )

    if 2 in workspacenumlist:
        lp.LedCtrlXY( 3, 6, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 3, 6, 0, 0, 0 )

    if 3 in workspacenumlist:
        lp.LedCtrlXY( 4, 6, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 4, 6, 0, 0, 0 )

    if 4 in workspacenumlist:
        lp.LedCtrlXY( 2, 7, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 2, 7, 0, 0, 0 )

    if 5 in workspacenumlist:
        lp.LedCtrlXY( 3, 7, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 3, 7, 0, 0, 0 )

    if 6 in workspacenumlist:
        lp.LedCtrlXY( 4, 7, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 4, 7, 0, 0, 0 )

    if 7 in workspacenumlist:
        lp.LedCtrlXY( 2, 8, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 2, 8, 0, 0, 0 )

    if 8 in workspacenumlist:
        lp.LedCtrlXY( 3, 8, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 3, 8, 0, 0, 0 )

    if 9 in workspacenumlist:
        lp.LedCtrlXY( 4, 8, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 4, 8, 0, 0, 0 )

    if 10 in workspacenumlist:
        lp.LedCtrlXY( 1, 1, 66, 164, 255 )
    else:
        lp.LedCtrlXY( 1, 1, 0, 0, 0 )

lastvol = 0

while 1:
    time.wait(50)
    bs = lp.ButtonStateXY()
    if getvol() != lastvol:
        displayvol()

    lastvol = getvol()

    updatevol( bs )


    #TODO: Define workspace names at top of file
    #TODO: move this mess into it's own function
    if len(bs) > 1:
        if bs[0] == 6 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("Atom")
        if bs[0] == 5 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("GitKraken")
        if bs[0] == 7 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("Dev")
        if bs[0] == 6 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("Vivaldi")
        if bs[0] == 5 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("Telegram")
        if bs[0] == 7 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("GenChat")
        if bs[0] == 6 and bs[1] == 7 and bs[2] == 127:
            i3.workspace("GenChat2")

        if bs[0] == 2 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("1:1")
        if bs[0] == 3 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("2:2")
        if bs[0] == 4 and bs[1] == 6 and bs[2] == 127:
            i3.workspace("3:3")
        if bs[0] == 2 and bs[1] == 7 and bs[2] == 127:
            i3.workspace("4:4")
        if bs[0] == 3 and bs[1] == 7 and bs[2] == 127:
            i3.workspace("5:5")
        if bs[0] == 4 and bs[1] == 7 and bs[2] == 127:
            i3.workspace("6:6")
        if bs[0] == 2 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("7:7")
        if bs[0] == 3 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("8:8")
        if bs[0] == 4 and bs[1] == 8 and bs[2] == 127:
            i3.workspace("9:9")
        # if bs[0] == 6 and bs[1] == 7 and bs[2] == 127:
        #     i3.workspace("10")

    testopen()

#The progams really should never actually get here, so, if it does...
print("Huston, We have a problem.")
