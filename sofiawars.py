import requests
from lxml import html
import thread
from time import sleep

session = requests.session()

#LOGIN

domain="http://www.sofiawars.com"
result = session.post("http://www.sofiawars.com/", data={"action":"login","email":"123456"},headers=dict(referer=domain+"/login/"))

#ATTACK SOMEONE
def fight():
    result = session.post(domain+"/alley/search/type/", data={"type":"equal","werewolf":"0","nowerewolf":"1","__ajax":"1","return_url":"/alley/"},headers=dict(referer=domain+"/alley/"))
    tree = html.fromstring(result.content)
    elems = tree.find_class("num")
    mypower = [int(elems[i].text_content()) for i in range(1,8)]
    hispower = [int(elems[i].text_content()) for i in range(8,15)]
    enemyID = ""
    rescon = result.content
    for i in range(7):
        k = rescon[rescon.find("alleyAttack(")+12+i]
        if k.isdigit():
            enemyID=enemyID+k

    print "ID", enemyID
    mysum = 0
    hissum=0
    for i in mypower:
        mysum=mysum+i
    for i in hispower:
        hissum=hissum+i
    if mypower[0]>hispower[0] and mypower[1]>hispower[1] and (mypower[5]>hispower[5] or mypower[3]>hispower[3]) and mysum>hissum:
        result = session.post(domain+"/alley/", data={"action": 'attack', "player": enemyID, "werewolf": "0", "useitems": "0"},
                            headers=dict(referer=domain+"/alley/"))
    else:
        fight()
        return
        #ATTACK
    #    print enemyID
    #    print "attack him:"
    #    for i in hispower:
    #        print i   
    

#WORK FOR 8 HOURS
def work(time):
    result=session.post(domain+"/shaurburgers/", data={"action":"work","time":time,"__ajax":"1","return_url":"/shaurburgers/"},
                    headers=dict(referer=domain+"/shaurburgers/"))

def patrol(time):
    result=session.post(domain+"/alley/", data={"action":"patrol","time":time,"region":"0","__ajax":"1","return_url":"/shaurburgers/"},
                    headers=dict(referer=domain+"/alley/"))

def Twork():
    work(8)
    patrol(60)
    sleep(1800)
def Tfight():
    while 1:
        while 1:
            print "f"
            result = session.get("http://www.sofiawars.com/player/")
            hp = int(html.fromstring(result.content).get_element_by_id("currenthp").text_content())
            maxhp = int(html.fromstring(result.content).get_element_by_id("maxhp").text_content())
            if hp == maxhp:
                fight()
                sleep(600)
                break
            sleep(10)
thread.start_new_thread( Twork , ())
thread.start_new_thread( Tfight , () )


