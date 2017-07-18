#!/usr/bin/python2
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
import os

print("Starting LaunchLinux, a python based hardware linux control panel using the Novation Launchpad")
print("Version 2.3")
print("Project by VegaDeftwing")
print("Launchpad.py by FMMT666")
print("Special Thanks to FMMT66 for helping me with a facepalm moment.")
print("i3 python by Ziberna")

#### VERSION HISTORY ####
# 1.0 intital creation, volume only
# 1.1 added MPD control, uploaded to GitHub
# 2.0 added i3 control
# 2.1 improved i3 control
# 2.2.2 updated with wal control, refactoring
# 2.3 Added CPU and RAM



### TODO: put config vars here, inc workspace and active modules


#Launchpad init
lp = launchpad.Launchpad();
lp = launchpad.LaunchpadMk2()
if lp.Check( 0, "mk2" ):
    lp = launchpad.LaunchpadMk2()
    if lp.Open( 0, "mk2" ):
        mode = "Mk2"
        lp.Reset()

print("Launchpad Mk2 opened, I hope?")

#State Tracking, inital state config
single = 0
lastvol = 0
lp.LedCtrlXY( 7, 5, 10, 10, 10 )
lp.LedCtrlXY( 1, 8, 0, 20, 100 )
lp.LedCtrlXY( 1, 7, 0, 0, 10 )
lp.LedCtrlXY( 1, 6, 0, 0, 10 )
lp.LedCtrlXY( 1, 5, 0, 20, 0 )
lp.LedCtrlXY( 1, 4, 20, 0, 0 )


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
    y = vol / 11.1
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
    if vol < 11:
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
            lp.LedCtrlXY( 0, j, 0, 0, 10 )

# TODO:
#def gettemp():
#def displaytemp():
# NOTE: reuse code from display vol and try to paramaterize
# for easy gradiants and more customizeablity, including x pos

# TODO:
# NOTE: display the following using a single 'pixel'
# and the built in launchpad colors so we get decent speed

def displayRAM():
    RAM = psutil.virtual_memory()
    RAM = RAM[2]
    RAM = int(RAM)
    if RAM < 30:
        r = 0
        g = RAM * 2
        b = RAM * 7
    if RAM > 30 and RAM < 62:
        r = RAM / 2
        g = RAM * 4
        b = RAM * 2
    if RAM > 62:
        r = RAM * 2
        g = 200 - RAM * 2
        b = 0
    if RAM > 90:
        r = 255
        g = 0
        b = 0
    lp.LedCtrlXY( 2, 1, r, g, b )

def displayCPU():
    CPU = psutil.cpu_percent(interval=1)
    CPU = int(CPU)
    if CPU < 30:
        r = CPU
        g = CPU * 2 + 10
        b = CPU * 7 + 10
    if CPU > 30 and CPU < 62:
        r = (CPU - 50) * CPU
        g = (CPU - 40) * 15
        b = CPU - int(CPU / 1.2)
    if CPU > 66:
        r = CPU * 2
        g = 200 - CPU * 2
        b = 0
    if CPU > 98:
        r = 255
        g = 0
        b = 0
    lp.LedCtrlXY( 1, 1, r, g, b )

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
def mpdctrl(bs):
    if len(bs) > 1:
        if bs[0] == 1 and bs[1] == 8 and bs[2] == 127:
            call(["mpc", "toggle"])
            lp.LedCtrlXY( 1, 8, 0, 20, 100 )

        if bs[0] == 1 and bs[1] == 7 and bs[2] == 127:
            call(["mpc", "next"])
            lp.LedCtrlXY( 1, 7, 0, 0, 255 )
            time.wait(50)

        if bs[0] == 1 and bs[1] == 7 and bs[2] == 0:
            lp.LedCtrlXY( 1, 7, 0, 0, 10 )

        if bs[0] == 1 and bs[1] == 6 and bs[2] == 127:
            call(["mpc", "prev"])
            lp.LedCtrlXY( 1, 6, 0, 0, 255 )
            time.wait(50)

        if bs[0] == 1 and bs[1] == 6 and bs[2] == 0:
            lp.LedCtrlXY( 1, 6, 0, 0, 10 )

        if bs[0] == 1 and bs[1] == 5 and bs[2] == 127:
            call(["mpc", "single","on"])
            lp.LedCtrlXY( 1, 5, 0, 20, 0 )
            single = 1
        if bs[0] == 1 and bs[1] == 4 and bs[2] == 127:
            call(["mpc", "single","off"])
            lp.LedCtrlXY( 1, 4, 20, 0, 0 )
            single = 0

def testworkspace(workspace, xpos, ypos, red, green, blue):

    workspacelist = getworkspacelist() + getworkspacenumlist()

    if workspace in workspacelist:
        lp.LedCtrlXY( xpos, ypos, red, green, blue )
    else:
        lp.LedCtrlXY( xpos, ypos, 0, 5, 5 )

def testopen():
    workspacelist = getworkspacelist()
    workspacenumlist = getworkspacenumlist()

    #Test workspace by name
    testworkspace("Atom",6,6,0,255,25)
    testworkspace("Dev",7,6,255,0,140)
    testworkspace("GitKraken",5,6,20,0,131)
    testworkspace("Vivaldi",6,8,255,0,0)
    testworkspace("Telegram",5,8,0,215,255)
    testworkspace("GenChat",7,8,86,66,255)
    testworkspace("GenChat2",6,7,66,164,255)
    #Testing worspace numbers
    testworkspace(1,2,6,66,164,255)
    testworkspace(2,3,6,66,164,255)
    testworkspace(3,4,6,66,164,255)
    testworkspace(4,2,7,66,164,255)
    testworkspace(5,3,7,66,164,255)
    testworkspace(6,4,7,66,164,255)
    testworkspace(7,2,8,66,164,255)
    testworkspace(8,3,8,66,164,255)
    testworkspace(9,4,8,66,164,255)
    #testworkspace(10,2,6,66,164,255)

def workspaceswitcher(workspace, xpos, ypos):
    if bs[0] == xpos and bs[1] == ypos and bs[2] == 127:
        i3.workspace(workspace)


#TODO: Define workspace names and pos on LP at top of file

def workspaceswitch(bs):
    if len(bs) > 1:
        workspaceswitcher("Atom",6,6)
        workspaceswitcher("GitKraken",5,6)
        workspaceswitcher("Dev",7,6)
        workspaceswitcher("Vivaldi",6,8)
        workspaceswitcher("Telegram",5,8)
        workspaceswitcher("GenChat",7,8)
        workspaceswitcher("GenChat2",6,7)
        workspaceswitcher("1:1",2,6)
        workspaceswitcher("2:2",3,6)
        workspaceswitcher("3:3",4,6)
        workspaceswitcher("4:4",2,7)
        workspaceswitcher("5:5",3,7)
        workspaceswitcher("6:6",4,7)
        workspaceswitcher("7:7",2,8)
        workspaceswitcher("8:8",3,8)
        workspaceswitcher("9:9",4,8)
        #workspaceswitcher("10:10",6,6)

def wal(bs):
    if len(bs) > 1:
        posx = 7
        posy = 5
        if bs[0] == posx and bs[1] == posy and bs[2] == 127:
            #os.system("wal -i /run/media/vega/RAID/Pictures/wal")
            #TODO: Change this from using wal.sh to wal.py. For some reason
            # the python version crashes everything
            lp.LedCtrlXY( posx, posy, 255, 0, 0 )
            call(["wal.sh", "-i", "/run/media/vega/RAID/Pictures/wal"])
            print("##############################")
            print("NEW COLORS SET")
            print("##############################")
            lp.LedCtrlXY( posx, posy, 10, 10, 10 )

### MAIN LOOP
### This is where the buton state (bs) is retrived in order
### to pass it into everything else
### the wait time can be adjusted in order to make the progam use
### more or less CPU, with the trade off being responsiveness
### there is a test to see if we even need to update the volume
### which, if you're crazy and want to remove the delay entirely
### could be taken out with time.wait for super fast response
### I noticetd that sometimes doing things like this could crash the
### program though, so, you're millage may varry. using the default
### of 50 for the wait should be perfectly responsive for most people
### though.
i = 0

while 1:
    time.wait(50)
    bs = lp.ButtonStateXY()

    if getvol() != lastvol:
        displayvol()

    lastvol = getvol()

    updatevol(bs)
    mpdctrl(bs)
    wal(bs)
    workspaceswitch(bs)
    testopen()

    #CPU and RAM display takes a lot of time and can add a lot of latency, this helps
    if i == 50:
        displayRAM()
    if i == 100:
        displayCPU()
        i = 0

    i = i + 1


#The progams really should never actually get here, so, if it does...
print("Huston, We have a problem.")
