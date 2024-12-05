
import json
import pickle
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

# This code operates on the malmo mod for minecraft. Besides the mission xml and mission running code,
# the AI functionality provided here has all been hand built by me

from builtins import range

import MalmoPython
import os
import sys
import time
from enum import Enum
from os.path import exists

import numpy.random
from numpy import square, sqrt, infty
import random

#Default values for various global variables
Reward = 0

SpecialistBoredom={"MoveSpecialist":0,"MineSpecialist":0,"CraftSpecialist":0}
BlockData = {}
SliceStateList = {} #Contains "slice": {"slice": slice,"stateval": stateval}
StateList = {} #Contains "state": {"state": state,"actions":{ "action1": action, "value": value of action}}
MoveActionList = {}
MoveBoredom = {"move":0,"jumpmove":0,"downmine":0,"forwardminemove":0,"upforwardminemove":0,"downforwardminemove":0} #Contains boredom values for all actions and options that exist, should probably store it off somewhere else
ChosenBoredom = {"1":0,"2":0,"3":0,"4":0} #Contains boredom values for choosing the same direction over and over
MoveMem = []
prev_life=20
StatesToEval=[]
selfslice = {}
world_map = {}
chosenState = ""
chosenAction = ""

inventory = {}
tools_list = ["wooden_pickaxe","stone_pickaxe","iron_pickaxe","diamond_pickaxe","shears"]
tool = "Hand"
target = ""
available_tools = {}
MineMove = {
    "front-2-left-diagonal":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0.3,0.3]
    },
    "front-2":{
        "directions":["look "],
        "value":[1],
        "duration":[0]
    },
    "front-2-right-diagonal":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.3,0.3]
    },
    "front-2-left":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0.3,0.5]
    },
    "down":{
        "directions":["look ","look "],
        "value":[1,1],
        "duration":[0,0]
    },
    "front-2-right":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.3,0.5]
    },
    "back-2-left-diagonal":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0.3,0.8]
    },
    "back-2":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.3,1]
    },
    "back-2-right-diagonal":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.3,0.8]
    },
    "front-1":{
        "directions":["look "],
        "value":[1],
        "duration":[0]
    },
    "front-1-right-diagonal":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.2,0.3]
    },
    "front-1-right":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0,0]
    },
    "back-1-right-diagonal":{
        "directions":["look ","turn "],
        "value":[1,1],
        "duration":[0.2,0.8]
    },
    "front-1-left-diagonal":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0.2,0.3]
    },
    "front-1-left":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0,0]
    },
    "back-1-left-diagonal":{
        "directions":["look ","turn "],
        "value":[1,-1],
        "duration":[0.2,0.8]
    },
    "back-1":{
        "directions":["look ","turn ","turn "],
        "value":[1,1,1],
        "duration":[0,0,0]
    },
    "front":{
        "directions":[],
        "value":[],
        "duration":[]
    },
    "front-right-diagonal":{
        "directions":["turn "],
        "value":[1],
        "duration":[0.3]
    },
    "front-right":{
        "directions":["turn "],
        "value":[1],
        "duration":[0]
    },
    "back-right-diagonal":{
        "directions":["turn "],
        "value":[1],
        "duration":[0.8]
    },
    "front-left-diagonal":{
        "directions":["move ","turn "],
        "value":[1,-1],
        "duration":[0,0]
    },
    "front-left":{
        "directions":["turn "],
        "value":[-1],
        "duration":[0]
    },
    "back-left-diagonal":{
        "directions":["move ","turn "],
        "value":[-1,-1],
        "duration":[1,0]
    },
    "back":{
        "directions":["turn ","turn "],
        "value":[1,1],
        "duration":[0,0]
    },
    "front+1":{
        "directions":["look "],
        "value":[-1],
        "duration":[0]
    },
    "front+1-right-diagonal":{
        "directions":["look ","turn "],
        "value":[-0.25,0.25],
        "duration":[1,1]
    },
    "front+1-right":{
        "directions":["look ","turn "],
        "value":[-1,1],
        "duration":[0,0]
    },
    "back+1-right-diagonal":{
        "directions":["look ","turn "],
        "value":[-0.25,0.75],
        "duration":[1,1]
    },
    "front+1-left-diagonal":{
        "directions":["look ","turn "],
        "value":[-0.25,-0.25],
        "duration":[1,1]
    },
    "front+1-left":{
        "directions":["look ","turn "],
        "value":[-1,-1],
        "duration":[0,0]
    },
    "back+1-left-diagonal":{
        "directions":["look ","turn "],
        "value":[-0.25,-0.75],
        "duration":[1,1]
    },
    "back+1":{
        "directions":["look ","turn ","turn "],
        "value":[-1,1,1],
        "duration":[0,0,0]
    },
    "up":{
        "directions":["look ","look "],
        "value":[-1,-1],
        "duration":[0,0]
    }
}
mining_target=0

learned_recipes = []
crafting_list = ["planks","stick"]
craftable = ""
crafting_textbook = [["wooden_pickaxe","stone_pickaxe"],["iron_ingot","shears","iron_pickaxe"],["diamond_pickaxe"],["gold_ingot","gold_block"]]

short_term_tasks = [["craftspecialist","stone_pickaxe","made stone_pickaxe"]]
long_term_tasks = []
prevObs = {}
complete_list = []

moveflag = False
mineflag = False
craftflag = False

#function that maintains mutually exclusive flags
def setFlag(flag):
    global moveflag
    global mineflag
    global craftflag
    moveflag = False
    mineflag = False
    craftflag = False
    if flag=="move":
        moveflag=True
    elif flag=="mine":
        mineflag=True
    elif flag=="craft":
        craftflag=True

# Functions to set global variables from withing functions
# (As python does not allow global variables to be directly modified unless explicitly defined
# and keeping track of them would become tedious)
def setChosenState(state):
    global  chosenState
    chosenState = state

def setChosenAction(action):
    global  chosenAction
    chosenAction = action

def setTool(t):
    global tool
    tool = t

def setTarget(t):
    global target
    target = t

def setCraftable(value):
    global  craftable
    craftable = value

def setPrevObs(obs):
    global  prevObs
    prevObs = obs

def getPrevLife():
    return prev_life

def setPrevLife(v):
    global prev_life
    prev_life=v

def getSelfslice():
    return selfslice

def setSelfslice(v):
    global selfslice
    selfslice=v

def getStatesToEval():
    return StatesToEval

def addToStatesToEval(v):
    global StatesToEval
    StatesToEval.append(v)

def clearStatesToEval():
    global StatesToEval
    StatesToEval=[]

# Loads data from files, if any exist
def loadData():
    global SpecialistBoredom
    global BlockData
    global SliceStateList
    global StateList
    global MoveActionList
    global MoveBoredom
    global ChosenBoredom
    global learned_recipes
    global crafting_list
    global crafting_textbook
    global world_map
    print("Loading data")
    if exists("C:/Users/pawan/Documents/RLMEMORY/SpecialistBoredom.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/SpecialistBoredom.pkl",'rb') as fp:
            SpecialistBoredom=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/BlockData.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/BlockData.pkl",'rb') as fp:
            BlockData=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/SliceStateList.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/SliceStateList.pkl",'rb') as fp:
            SliceStateList=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/StateList.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/StateList.pkl",'rb') as fp:
            StateList=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/MoveActionList.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/MoveActionList.pkl",'rb') as fp:
            MoveActionList=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/MoveBoredom.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/MoveBoredom.pkl",'rb') as fp:
            MoveBoredom=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/ChosenBoredom.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/ChosenBoredom.pkl",'rb') as fp:
            ChosenBoredom=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/WorldMap.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/WorldMap.pkl",'rb') as fp:
            world_map=pickle.load(fp)

    if exists("C:/Users/pawan/Documents/RLMEMORY/LearnedRecipes.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/LearnedRecipes.pkl",'rb') as fp:
            learned_recipes=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/CraftingList.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/CraftingList.pkl",'rb') as fp:
            crafting_list=pickle.load(fp)
    if exists("C:/Users/pawan/Documents/RLMEMORY/CraftingTextbook.pkl"):
        with open("C:/Users/pawan/Documents/RLMEMORY/CraftingTextbook.pkl",'rb') as fp:
            crafting_textbook=pickle.load(fp)

# Saves learned data to files
def saveData():
    global SpecialistBoredom
    global BlockData
    global SliceStateList
    global StateList
    global MoveActionList
    global MoveBoredom
    global ChosenBoredom
    global learned_recipes
    global crafting_list
    global crafting_textbook
    global world_map

    with open("C:/Users/pawan/Documents/RLMEMORY/SpecialistBoredom.pkl", 'wb') as fp:
        pickle.dump(SpecialistBoredom,fp)
        print("Saved SpecialistBoredom")

    with open("C:/Users/pawan/Documents/RLMEMORY/BlockData.pkl", 'wb') as fp:
        pickle.dump(BlockData,fp)
        print("Saved BlockData")
    with open("C:/Users/pawan/Documents/RLMEMORY/SliceStateList.pkl", 'wb') as fp:
        pickle.dump(SliceStateList,fp)
        print("Saved SliceStateList")
    with open("C:/Users/pawan/Documents/RLMEMORY/StateList.pkl", 'wb') as fp:
        pickle.dump(StateList,fp)
        print("Saved StateList")
    with open("C:/Users/pawan/Documents/RLMEMORY/MoveActionList.pkl", 'wb') as fp:
        pickle.dump(MoveActionList,fp)
        print("Saved MoveActionList")
    with open("C:/Users/pawan/Documents/RLMEMORY/MoveBoredom.pkl", 'wb') as fp:
        pickle.dump(MoveBoredom,fp)
        print("Saved MoveBoredom")
    with open("C:/Users/pawan/Documents/RLMEMORY/ChosenBoredom.pkl", 'wb') as fp:
        pickle.dump(ChosenBoredom,fp)
        print("Saved ChosenBoredom")
    with open("C:/Users/pawan/Documents/RLMEMORY/WorldMap.pkl", 'wb') as fp:
        pickle.dump(world_map,fp)
        print("Saved World Map")

    with open("C:/Users/pawan/Documents/RLMEMORY/LearnedRecipes.pkl", 'wb') as fp:
        pickle.dump(learned_recipes,fp)
        print("Saved LearnedRecipes")
    with open("C:/Users/pawan/Documents/RLMEMORY/CraftingList.pkl", 'wb') as fp:
        pickle.dump(crafting_list,fp)
        print("Saved CraftingList")
    with open("C:/Users/pawan/Documents/RLMEMORY/CraftingTextbook.pkl", 'wb') as fp:
        pickle.dump(crafting_textbook,fp)
        print("Saved CraftingTextbook")

# Enumerations for classification. Defines what items/blocks are perceived as by the system
class Block(Enum):
    unknown = 0
    liquid = 1
    safe = 2
    unsafe = 3

class MineType(Enum):
    unknown = 0
    cannot_mine = -1
    mine = 1

class CraftType(Enum):
    unknown = 0
    cannot_craft = -1
    craft = 1

#Basic item initialization
def block_init(x, y, z):
    blk = [x, y, z, Block.unknown, MineType.unknown, {}, [], CraftType.unknown, []]
    #Last known x,y,z location of block, Classification for move specialist,
    #Whether item is mineable, Precondition tool(s), Precondition block(s) (to mine), Whether item is craftable, precondition blocks (to craft)
    return blk

#Location setting
def block_loc_set(v,x,y,z):
    global  BlockData
    if BlockData[v][0]!=x:
        BlockData[v][0]=x
    if BlockData[v][1]!=y:
        BlockData[v][1]=y
    if BlockData[v][2]!=z:
        BlockData[v][2]=z

#Classification of block according to MoveSpecialist rules
def block_move_class(self,x,y,z,curHP,prevHP):
    global  BlockData
    stack=[]
    i=1
    rew=0
    for item in self:
        stack.append(item)
    for _ in self:
        v=stack.pop()
        if v not in BlockData.keys():
            rew+=5
            BlockData[v] = block_init(x,y,z)
        block_loc_set(v,x,y,z)
        if BlockData[v][3].value==Block.unknown.value:
            if curHP < prevHP:
                BlockData[v][3] = Block.unsafe
                rew+=9
            else:
                if i!=3:
                    BlockData[v][3] = Block.liquid
                    rew+=10
                else:
                    BlockData[v][3] = Block.safe
                    rew+=10
        i=i+1
    return rew-prevHP+curHP

#Value of a block as per MoveSpecialist
def move_block_val(blockType):
    if blockType==Block.unknown.value:
        return 10
    if blockType==Block.unsafe.value:
        return -5
    return 0

#Takes a flattened json of a 1 x 6 x 1 area and converts it into a format used to define the components of a
# 'state' for the MoveSpecialist
def move_slice_state_construct(slice):
    global BlockData
    global SliceStateList
    state=""
    stateval=0
    i=0
    for item in slice:
        i=i+1
        if item in BlockData.keys():
            blk = BlockData[item][3]
            state += str(blk.value)
            stateval+=move_block_val(blk.value)
        else:
            state += str(Block.unknown.value)
            stateval+=10
    stateval=stateval/i
    if state in SliceStateList.keys():
        return SliceStateList[state]
    SliceStateList[state]={
        "state":state,
        "stateval":stateval
    }
    return SliceStateList[state]

#Checks if the state exists within the system. If not, it generates it, adds it to the system and returns it
def move_state_construct(cur,wantednext):
    global StateList
    global SliceStateList
    global MoveActionList
    #print("Cur:" + cur["state"])
    #print("Wanted:" + wantednext["state"])
    state=cur["state"]+wantednext["state"]
    #print("State:"+state)
    if state in StateList.keys():
        for action in MoveActionList.keys():
            if action not in StateList[state]["actions"].keys():
                StateList[state]["actions"][action] = MoveActionList[action]
        return StateList[state]
    value = 10
    StateList[state]={
        "state": state,
        "actions":{
            "move": {
                "action": "move",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort":1
            },
            "jumpmove": {
                "action": "jumpmove",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort":2
            },
            "downmine": {
                "action": "request:down",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort": 1
            },
            "forwardminemove": {
                "action": "move:request:front-1:request:front",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort": 3
            },
            "upforwardminemove": {
                "action": "jumpmove:request:front:request:front+1:request:up",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort": 5
            },
            "downforwardminemove": {
                "action": "request:down:move:request:front-1:request:front",
                "value": value,
                "isOption": False,
                "familiarity": 0,
                "changeX": 0,
                "changeY": 0,
                "changeZ": 0,
                "changeXZ": 0,
                "effort": 4
            }
        }
    }
    #for action in MoveActionList.keys():
    #    StateList[state]["actions"][action] = MoveActionList[action]
    return StateList[state]

#Code that takes the evaluated direction, and modifies value accordingly.
#This function is part of the system that reduces 3D space evaluation into 2D space evaluation
def DirMap(chosen,xz):
    xmod = 0
    zmod = 0
    if chosen == 1:
        xmod = xz
    elif chosen == 2:
        zmod = xz
    elif chosen == 3:
        xmod = -xz
    elif chosen == 4:
        zmod = -xz
    return xmod,zmod

#Evaluation of the present world according to the MoveSpecialist
#And precalculates some of the data to be used if MoveSpecialist is chosen
def MoveEval(obs):
    cur_life = obs.get(u'Life',0)
    plife=getPrevLife()
    self=obs.get(u'self',0)
    x = int(obs.get(u'XPos',0))
    y = int(obs.get(u'YPos',0))
    z = int(obs.get(u'ZPos',0))
    block_move_class(self,x,y,z,cur_life,plife)
    setPrevLife(cur_life)
    setSelfslice(move_slice_state_construct(obs.get(u'slice_self',0)))
    sslice=getSelfslice()
    mappos=str(x)+":"+str(y)+":"+str(z)
    world_map[mappos]=sslice
    moveval=0
    clearStatesToEval()
    #statevls=[]
    for i in range(1,5):
        slice = move_slice_state_construct(obs.get(u'slice_'+str(i),0))
        addToStatesToEval(slice)
        xmod,zmod=DirMap(i,1)
        world_map[str(x + xmod) + ":" + str(y) + ":" + str(z + zmod)] = slice
        state = sslice["state"] + slice["state"]
        if state in StateList.keys():
            for action in StateList[state]["actions"].keys():
                moveval = max(moveval,StateList[state]["actions"][action]["value"] + slice["stateval"] + numpy.float64(1)/StateList[state]["actions"][action]["familiarity"])
        else:
            moveval = 10 + slice["stateval"]
        #statevls.append(slice["stateval"])
    #avgval=avgval/4
    #print("State vals: ")
    #print(statevls)
    #print("average value: "+str(avgval))
    return moveval

#Returns the default action taken by the MoveSpecialist
def defaultAction():
    global MoveBoredom
    return "move",0-MoveBoredom["move"],False,"move"

#Handles execution of an action if the MoveSpecialist is chosen to take an action
def MoveHandler(obs):
    global MoveMem
    global MoveBoredom
    global SliceStateList
    global StateList
    setFlag("move")
    seval = getStatesToEval()
    sfslice = getSelfslice()
    localStateList=[]
    for i in range(0,4):
        localStateList.append(move_state_construct(sfslice,seval[i]))
    chosen = 1
    chosenState = localStateList[0]
    chosenAction,chosenActionValue,isOption,chosenActionName=defaultAction()
    chosenList = []
    chosenList.append([chosen, chosenState, chosenAction, isOption, chosenActionName])
    i=0
    for local in localStateList:
        i=i+1
        pac,pacval,piO,pacnm=maxAction(local["actions"])
        if pacval==chosenActionValue:
            chosenList.append([i,local["state"],pac,piO,pacnm])
        elif pacval>chosenActionValue:
            chosenList.clear()
            chosenList.append([i, local["state"], pac, piO,pacnm])
            #chosen=i
            #chosenState=local["state"]
            #chosenAction=pac
            chosenActionValue=pacval-ChosenBoredom[str(chosen)]
            #isOption=piO
    selected = numpy.random.randint(-1,len(chosenList)-1) + 1
    chosen=chosenList[selected][0]
    chosenState=chosenList[selected][1]
    chosenAction=chosenList[selected][2]
    isOption=chosenList[selected][3]
    chosenActionName=chosenList[selected][4]
    if(isOption):
        ExecuteAction(chosenAction.split(":"))
    else:
        ConstructAction(chosenAction,chosen)
        #print("Construct: ")
        #print(construct)
        #ExecuteAction(construct)
    #LoopDetector(MoveMem)
    setPrevObs(obs)
    setChosenState(chosenState)
    setChosenAction(chosenActionName)
    #ModifyBoredom(chosenAction)
    #ModifyChosenBoredom(str(chosen))
    return 0

#Function that evaluates the action taken by the MoveSpecialist (MoveHandler)
def MovePostActionEval(new_obs):
    obs = prevObs
    x = int(new_obs.get(u'XPos', 0))
    y = int(new_obs.get(u'YPos', 0))
    z = int(new_obs.get(u'ZPos', 0))
    r = block_move_class(new_obs.get(u'self', 0), x, y,z, new_obs.get(u'Life', 0), getPrevLife()) + Distance(x, y, z, int(obs.get(u'XPos', 0)), int(obs.get(u'YPos', 0)), int(obs.get(u'ZPos', 0)))
    StateList[chosenState]["actions"][chosenAction]["value"] = (StateList[chosenState]["actions"][chosenAction]["value"] + r) / 2
    fam = StateList[chosenState]["actions"][chosenAction]["familiarity"] + 1
    StateList[chosenState]["actions"][chosenAction]["familiarity"] = fam
    StateList[chosenState]["actions"][chosenAction]["changeX"] = (abs(x) - abs(
        int(obs.get(u'XPos', 0))) + StateList[chosenState]["actions"][chosenAction]["changeX"] * (fam - 1)) / fam
    StateList[chosenState]["actions"][chosenAction]["changeY"] = (y -
        int(obs.get(u'YPos', 0)) + StateList[chosenState]["actions"][chosenAction]["changeY"] * (fam - 1)) / fam
    StateList[chosenState]["actions"][chosenAction]["changeZ"] = (abs(z) - abs(
        int(obs.get(u'ZPos', 0))) + StateList[chosenState]["actions"][chosenAction]["changeZ"] * (fam - 1)) / fam
    StateList[chosenState]["actions"][chosenAction]["changeXZ"] = abs((int(new_obs.get(u'ZPos', 0))) - abs(z) + abs(x) - abs(int(obs.get(u'XPos', 0))) + StateList[chosenState]["actions"][chosenAction]["changeXZ"] * (fam - 1)) / fam
    setFlag("")

#Part of the 'Boredom' Mechanism, a system to ensure that the same action is not repeatedly chosen.
#I believe move functions in this system have been deactivated though
def ModifyBoredom(chosenAction):
    global MoveBoredom
    MoveBoredom[chosenAction]=MoveBoredom[chosenAction]+0.2
    for key in MoveBoredom.keys():
        MoveBoredom[key]=max(MoveBoredom[key]-0.1, 0)

def ModifyChosenBoredom(chosen):
    global ChosenBoredom
    ChosenBoredom[chosen] = ChosenBoredom[chosen] + 0.4
    for key in ChosenBoredom.keys():
        ChosenBoredom[key] = max(ChosenBoredom[key] - 0.1, 0)

def ModifySpecialistBoredom(chosen):
    global SpecialistBoredom
    SpecialistBoredom[chosen] = SpecialistBoredom[chosen] + 0.4
    for key in SpecialistBoredom.keys():
        SpecialistBoredom[key] = max(SpecialistBoredom[key] - 0.1, 0)

#When a move is chosen by the MoveSpecialist, this function is used to translate it into the appropriate
#3D representation. It also breaks down the more complex actions for execution
def ConstructAction(chosenAction,chosen):
    construct=[]
    stack=[]
    temp=[]
    splitac=chosenAction.split(":")
    #print("split action: ")
    print(splitac)
    for action in splitac:
        temp.append(action)
        if action=="jump":
            temp.append("jump 0")
    request = False
    for action in temp:
        if "move" == action:
            if chosen==1:
                makeRequest("movespecialist",["move -1","","simplemove"],"did move -1")
                #construct.append(action.replace("move","move -1"))
                #stack.append("move 0")
            if chosen==2:
                makeRequest("movespecialist", ["strafe -1", "", "simplemove"], "did strafe -1")
                #construct.append(action.replace("move","strafe -1"))
                #stack.append("strafe 0")
            if chosen==3:
                makeRequest("movespecialist", ["move 1", "", "simplemove"], "did move 1")
                #construct.append(action.replace("move","move 1"))
                #stack.append("move 0")
            if chosen==4:
                makeRequest("movespecialist", ["strafe 1", "", "simplemove"], "did strafe 1")
                #construct.append(action.replace("move","strafe 1"))
                #stack.append("strafe 0")
        elif "jumpmove" == action:
            if chosen==1:
                makeRequest("movespecialist",["jumpmove -1","","simplemove"],"did jumpmove -1")
            if chosen==2:
                makeRequest("movespecialist", ["jumpstrafe -1", "", "simplemove"], "did jumpstrafe -1")
            if chosen==3:
                makeRequest("movespecialist", ["jumpmove 1", "", "simplemove"], "did jumpmove 1")
            if chosen==4:
                makeRequest("movespecialist", ["jumpstrafe 1", "", "simplemove"], "did jumpstrafe 1")
        elif action=="request":
            request=True
        elif request:
            if action=="up" or action == "down" or chosen==3:
                makeRequest("minespecialist",[action,"mine"],"mined "+action)
            elif chosen==4:
                makeRequest("minespecialist",[action+"-right","mine"],"mined "+action+"-right")
            elif chosen==1:
                action=action.replace("front","back")
                makeRequest("minespecialist",[action,"mine"],"mined "+action)
            elif chosen==2:
                makeRequest("minespecialist",[action+"-left","mine"],"mined "+action+"-left")
            request = False

    stack.clear()
    slen=len(stack)
    for _ in range(0,slen):
        action=stack.pop()
        construct.append(action)
    return construct

#Function that executes a given action
def ExecuteAction(instructionList):
    global MoveMem
    #resconstruct=""
    print("Actions received:")
    print(instructionList)
    for action in instructionList:
        agent_host.sendCommand(action)
        #resconstruct=resconstruct+action+":"
        time.sleep(0)
    #resconstruct=resconstruct[:-1]
    #MoveMem.append(resconstruct)
    #if len(MoveMem)>10:
    #    del MoveMem[0]
    #print("Movemem: ")
    #print(MoveMem)

#System that constructs move complex actions from trivial ones.
#It has been deactivated due to its extreme generative power
def ConstructOption(vals):
    global MoveActionList
    newOption=""
    for action in vals:
        newOption=newOption+action+":"
    newOption=newOption[:-1]
    if newOption not in MoveActionList.keys():
        MoveActionList[newOption]={
            "action":newOption,
            "value":5,
            "isOption":True,
            "familiarity": 0,
            "changeX": 0,
            "changeY": 0,
            "changeZ": 0,
            "changeXZ": 0
        }
        MoveBoredom[newOption]=0

#Calculates the most rewarding action for the MoveSpecialist from the given list
def maxAction(Actions):
    chosenAction,chosenActionValue,isOption,chosenActionName=defaultAction()
    for action in Actions.keys():
        pacval=Actions[action]["value"] - MoveBoredom[action]
        if pacval>chosenActionValue:
            chosenAction=Actions[action]["action"]
            chosenActionValue=pacval
            isOption=Actions[action]["isOption"]
            chosenActionName=action
    return chosenAction,chosenActionValue,isOption,chosenActionName

#Constructs the state as per the MineSpecialists' needs
def mine_state_construct(view):
    state=""
    #State = []
    for item in view:
        if item in BlockData.keys():
            state += str(BlockData[item][5])
            #State.append(BlockData[item][3])
        else:
            state += str(Block.unknown.value)
            #State.append(Block.unknown)
    if state in StateList.keys():
        return StateList[state]

#Central governing system of the AI
def super_controller(obs):
    if len(short_term_tasks)==0:
        learningHandler(obs)
    else:
        RequestHandler(obs)

#Specialist specifically tasked with learning things from the environment
def learningHandler(obs):
    print("Round Start")
    curInventory = getInventory()
    prevInventory = {}
    for key in curInventory.keys():
        prevInventory[key] = curInventory[key]
    setInventory(obs)
    print(prevInventory)
    print(curInventory)
    global Reward
    if moveflag:
        MovePostActionEval(obs)
    elif mineflag:
        MinePostActionEval(obs, target, prevInventory, curInventory)
    elif craftflag:
        Reward += CraftPostActionEval(craftable, prevInventory, curInventory)
    craftscore = CraftEval(prevInventory, curInventory) - SpecialistBoredom["CraftSpecialist"]
    movescore = MoveEval(obs) - SpecialistBoredom["MoveSpecialist"]
    minescore = MineEval(obs) - SpecialistBoredom["MineSpecialist"]
    print("Scores: Craft " + str(craftscore) + " Move " + str(movescore) + " Mine " + str(minescore))
    best = max(movescore, minescore, craftscore)
    if best == movescore:
        print("Chose Move")
        Reward += MoveHandler(obs)
        ModifySpecialistBoredom("MoveSpecialist")
    elif best == minescore:
        print("Chose Mine")
        Reward += MineHandler()
        ModifySpecialistBoredom("MineSpecialist")
    elif best == craftscore:
        print("Chose Craft")
        Reward += CraftHandler()
        ModifySpecialistBoredom("CraftSpecialist")

#System that detects repeated actions
def LoopDetector(Mem):
    pot=[]
    for i in range(0,len(Mem)-2):
        vl=Mem[i]
        st=i+2
        for j in range(st,len(Mem)):
            vl2=Mem[j]
            if vl==vl2:
                pot.append(j)
        for j in pot:
            val=[]
            l=0
            for k in range(0,len(Mem)-j):
                if Mem[i+k]==Mem[j+k]:
                    val.append(Mem[i+k])
                    l=l+1
                else:
                    break
            if l>1:
                ConstructOption(val)

def get_available_tools():
    global available_tools
    return available_tools

#Checks inventory and finds the first instance of a tool
def add_available_tools(obs):
    global available_tools
    available_tools.clear()
    for i in range(0, 40):
        item = obs['InventorySlot_' + str(i) + '_item']
        if item in tools_list and item not in available_tools.keys():
            available_tools[item] = i
        elif item not in tools_list and "Hand" not in available_tools.keys():
            available_tools["Hand"] = i

#Checks if given block can be mined or not
def can_mine(mineable):
    if 'air' in mineable:
        return False
    if 'water' in mineable:
        return False
    if 'lava' in mineable:
        return False
    return True

def getMiningTarget():
    global mining_target
    return mining_target

def setMiningTarget(val):
    global mining_target
    mining_target = val

#Checks if the target detected by grid analysis is also visible in ray analysis after
#head turning operations are completed
def can_see(target,direction):
    action = MineActionSelect(direction)
    cansee = False
    for i in range(0,len(action["directions"])):
        agent_host.sendCommand(action["directions"][i]+str(action["value"][i]))
        time.sleep(int(action["duration"][i]))
        agent_host.sendCommand(action["directions"][i] + str(0))
        time.sleep(1)
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        m = world_state.observations[-1].text
        obs = json.loads(m)
        if u'LineOfSight' in obs.keys():
            los = obs[u'LineOfSight']
            if los["type"]==target:
                cansee = True
    for i in range(0, len(action["directions"])):
        agent_host.sendCommand(action["directions"][i] + str(action["value"][i]*-1))
        time.sleep(int(action["duration"][i]))
        agent_host.sendCommand(action["directions"][i] + str(0))
        time.sleep(1)
    return cansee

#Evaluates the present world with respect to the MineSpecialists' standards
def MineEval(obs):
    global  BlockData
    setInventory(obs)
    curInventory = getInventory()
    add_available_tools(obs)
    mine_state = obs.get(u'mine_box',0)
    visible = [19,10,12,14,16,4,21,23,25,31]
    benchmark=0
    setMiningTarget(visible[0]+1)
    chosenmineable = ""
    loc = ""
    for value in visible:
        mineable = mine_state[value]
        if mineable not in BlockData.keys():
            BlockData[mineable] = block_init(obs.get(u'XPos', 0), obs.get(u'YPos', 0), obs.get(u'ZPos', 0))
        block_loc_set(mineable, obs.get(u'XPos', 0), obs.get(u'YPos', 0), obs.get(u'ZPos', 0))
        if can_mine(mineable):
            checked_tool_prereq = BlockData[mineable][5]
            pot = 0
            for tool in get_available_tools().keys():
                if tool not in checked_tool_prereq:
                    pot = 10
                    break
                elif mineable not in curInventory.keys():
                    pot = max(pot, 10+BlockData[mineable][5][tool])
                elif mineable not in tools_list: #and curInventory[mineable]<20
                    pot = max(pot, 2+BlockData[mineable][5][tool])
            if pot >= benchmark:
                benchmark = pot
                setMiningTarget(value+1)
                chosenmineable = mineable
                loc = value + 1
            print("chosen item and location")
            print(chosenmineable)
            print(loc)
    return benchmark

#Maps chosen grid segment to equivalent action
def MineActionSelect(target):
    if target==9:
        return MineMove["front-2-left-diagonal"]
    if target==8:
        return MineMove["front-2"]
    if target==7:
        return MineMove["front-2-right-diagonal"]
    if target==6:
        return MineMove["front-2-left"]
    if target==5:
        return MineMove["down"]
    if target==4:
        return MineMove["front-2-right"]
    if target==3:
        return MineMove["back-2-left-diagonal"]
    if target==2:
        return MineMove["back-2"]
    if target==1:
        return MineMove["back-2-right-diagonal"]
    if target==18:
        return MineMove["front-1-left-diagonal"]
    if target==17:
        return MineMove["front-1"]
    if target==16:
        return MineMove["front-1-right-diagonal"]
    if target==15:
        return MineMove["front-1-left"]
    if target==13:
        return MineMove["front-1-right"]
    if target==12:
        return MineMove["back-1-left-diagonal"]
    if target==11:
        return MineMove["back-1"]
    if target==10:
        return MineMove["back-1-right-diagonal"]
    if target==27:
        return MineMove["front-left-diagonal"]
    if target==26:
        return MineMove["front"]
    if target==25:
        return MineMove["front-right-diagonal"]
    if target==24:
        return MineMove["front-left"]
    if target==22:
        return MineMove["front-right"]
    if target==21:
        return MineMove["back-left-diagonal"]
    if target==20:
        return MineMove["back"]
    if target==19:
        return MineMove["back-right-diagonal"]
    if target==36:
        return MineMove["front+1-left-diagonal"]
    if target==35:
        return MineMove["front+1"]
    if target==34:
        return MineMove["front+1-right-diagonal"]
    if target==33:
        return MineMove["front+1-left"]
    if target==32:
        return MineMove["up"]
    if target==31:
        return MineMove["front+1-right"]
    if target==30:
        return MineMove["back+1-left-diagonal"]
    if target==29:
        return MineMove["back+1"]
    if target==28:
        return MineMove["back+1-right-diagonal"]
    return MineMove["front"]

#Checks if mined block was collected
def mineCalculate(prevInventory,curInventory):
    global BlockData
    minedblock = []
    for item in curInventory.keys():
        if item in prevInventory.keys():
            dif = curInventory[item] - prevInventory[item]
            if dif > 0:
                minedblock.append(item)
        else:
            minedblock.append(item)
    return minedblock

#Executes actions according to MineSpecialist
def Enactor(action, val, duration):
    cm1 = action + val
    cm2 = action + str(0)
    agent_host.sendCommand(cm1)
    time.sleep(duration)
    agent_host.sendCommand(cm2)

#Evaluates action taken by MineSpecialist
def MinePostActionEval(obs2,target,prevInventory,curInventory):
    global BlockData
    global complete_list
    if prevInventory == curInventory and tool not in BlockData[target][5].keys():
        BlockData[target][5][tool] = 0
    if prevInventory != curInventory:
        minedblock = mineCalculate(prevInventory, curInventory)
        BlockData[target][5][tool] = 10
        BlockData[target][4] = MineType.mine
        complete_list.append("learned "+target)
        for block in minedblock:
            if block not in BlockData.keys():
                BlockData[block] = block_init(0,0,0)
            BlockData[block][0] = int(obs2.get(u'XPos', 0))
            BlockData[block][1] = int(obs2.get(u'YPos', 0))
            BlockData[block][2] = int(obs2.get(u'ZPos', 0))
            if target not in BlockData[block][6]:
                BlockData[block][6].append(target)
                #BlockData[target][5][tool] = 10
    setTarget("")
    setFlag("")

#Control is given here from MineHandler to perform the chosen action
def MineActionExecutor(action,tool):
    global BlockData
    done=False
    for i in range(0,len(action["directions"])):
        Enactor(action["directions"][i],str(action["value"][i]),float(action["duration"][i]))
        time.sleep(1)
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        #print("New observations made")
        m = world_state.observations[-1].text
        obs = json.loads(m)
        if u'LineOfSight' in obs.keys():
            print("Line of sight found")
            los = obs[u'LineOfSight']
            cur_mine_state = obs.get(u'mine_box', 0)
            #print(los)
            target = los["type"]
            if "prop_variant" in los.keys():
                target = los["prop_variant"]
            setTarget(target)
            setTool(tool)
            dst = los["distance"]
            if target not in BlockData.keys():
                BlockData[target] = block_init(int(obs.get(u'XPos', 0)), int(obs.get(u'YPos', 0)), int(obs.get(u'ZPos', 0)))
            if tool not in BlockData[target][5].keys():
                    Enactor("attack ","1",0)
                    time.sleep(1)
            else: #if BlockData[target][5][tool] > 0
                Enactor("attack ","1",0)
                time.sleep(1)
                done = True
    for i in range(0, len(action["directions"])):
        Enactor(action["directions"][i],str(action["value"][i]*-1),float(action["duration"][i]))
        time.sleep(1)
    return done

#Control is given here when MineSpecialist is chosen
def MineHandler():
    setFlag("mine")
    action = MineActionSelect(getMiningTarget())
    r = 0
    num = numpy.random.randint(0,len(available_tools)+1) - 1
    ch = "Hand"
    n = 0
    for key in available_tools.keys():
        if n == num and key != "":
            ch = key
            break
        n += 1
    tl = ch
    agent_host.sendCommand("swapInventoryItems 0 " + str(available_tools[tl]))
    print("chosen action: ")
    print(action)
    MineActionExecutor(action,tl)
    agent_host.sendCommand("swapInventoryItems " + str(available_tools[tl]) + " 0")
    return 10

#A function that could have served as the guiding algorithm for the MoveSpecialist when given a target to go to
#It was not used in the end but kept, just in case
def EvalAction(state,dst,cur):
    chosen = Distance(dst[0],dst[1],dst[2],cur[0],cur[1],cur[2])
    for action in StateList[state]["ActionList"]:
        if not action["isOption"]:
            action["changeX"] = abs(action["changeX"])
            action["changeZ"] = abs(action["changeZ"])
            action["changeXZ"] = abs(action["changeX"]) + abs(action["changeZ"])
        pot = Distance(dst[0], dst[1], dst[2], cur[0] + action["changeX"], cur[1] + action["changeY"],cur[2] + action["changeZ"])
        if pot<chosen:
            chosen = pot
    return 100/chosen

#Calculates Euclidean distance
def Distance(dstx, dsty, dstz, x, y, z):
    dst = square(dstx - x)
    dst += square(dsty - y)
    dst += square(dstz - z)
    return sqrt(dst)

def getInventory():
    global inventory
    return inventory

#Function that calculates all the items in the inventory
def setInventory(obs):
    global inventory
    inventory.clear()
    for num in range (0,40):
        item = obs['InventorySlot_' + str(num) + '_item']
        amount = int(obs[u'InventorySlot_'+str(num)+'_size'])
        #print("Item: "+str(item)+", Number: "+str(amount))
        if item not in inventory.keys():
            inventory[item] = 0
        inventory[item] += amount

#This function calculates the crafting recipe of an item by checking the consumed ingredients
def recipeCalculate(craftable,prevInventory,curInventory):
    global BlockData
    recipe = {}
    for item in prevInventory.keys():
        if item in curInventory.keys():
            dif = prevInventory[item] - curInventory[item]
            if dif > 0:
                recipe[item] = dif
        else:
            recipe[item] = prevInventory[item]
    if craftable not in BlockData.keys():
        BlockData[craftable] = block_init(0,0,0)
    if recipe not in BlockData[craftable][8] and recipe!={}:
        BlockData[craftable][7] = CraftType.craft
        BlockData[craftable][8].append(recipe)

#This function checks if an item can be crafted given the current available materials
def can_craft(item, materials):
    global BlockData
    for recipe in BlockData[item][8]:
        valid = True
        for ingredient in recipe.keys():
            if ingredient in materials.keys():
                if materials[ingredient] < recipe[ingredient]:
                    valid = False
                    break
            else:
                valid = False
                break
        if valid:
            return valid
    return False

#Evalutes the present world with respect to the CraftSpecialist
def CraftEval(prevInventory,curInventory):
    craft_potential = 0
    for item in learned_recipes:
        if item not in curInventory.keys():
            if can_craft(item, curInventory):
                craft_potential += 10
        elif item not in tools_list and curInventory[item]<20:
            if can_craft(item, curInventory):
                craft_potential += 2
    if prevInventory!=curInventory:
        return len(crafting_list)*10+craft_potential
    return craft_potential

#Parent function to recipeCalculate
def get_Recipe(craftable, prevInventory,curInventory):
    global learned_recipes
    global  complete_list
    if prevInventory != curInventory and craftable in curInventory:
        print("recipe learned")
        recipeCalculate(craftable, prevInventory, curInventory)
        if craftable not in learned_recipes:
            learned_recipes.append(craftable)
            complete_list.append("learned " + craftable)
        return 10
    return 0

#Evaluation after crafting is done
def CraftPostActionEval(craftable,prevInventory,curInventory):
    print("In craft post action eval")
    x = get_Recipe(craftable, prevInventory,curInventory)
    setCraftable("")
    setFlag("")
    return x

#Where control is handed if CraftSpecialist is chosen
def CraftHandler():
    setFlag("craft")
    global BlockData
    global learned_recipes
    global crafting_list
    global crafting_textbook
    rew = 0
    #Stage 1, focused on learning new recipes
    for craftable in learned_recipes:
        if craftable in crafting_list:
            crafting_list.remove(craftable)
    if len(crafting_list) == 0:
        rew += 10
        if len(crafting_textbook) > 0:
            for craftable in crafting_textbook[0]:
                crafting_list.append(craftable)
            del crafting_textbook[0]
    could_craft = crafting_list
    #for craftable in crafting_list:
    #    if craftable not in BlockData.keys():
    #        BlockData[craftable] = block_init(0, 0, 0)
    #    agent_host.sendCommand("craft "+craftable)
    #    setCraftable(craftable)
    #    break

    #Stage 2, crafting what you know when you lack it
    for item in learned_recipes:
        curInventory = getInventory()
        if item not in curInventory.keys():
            if can_craft(item, curInventory):
                could_craft.append(item)
                #rew += 10
                #agent_host.sendCommand("craft "+item)
                #time.sleep(1)
                #get_Recipe(item, curInventory)
        elif item not in tools_list and curInventory[item] < 20:
            if can_craft(item, curInventory):
                could_craft.append(item)
                #rew += 2
                #agent_host.sendCommand("craft "+item)
                #time.sleep(1)
                #get_Recipe(item, curInventory)
    eps = 0.6
    l = len(could_craft)
    neps = (1 - eps)/l
    wtlst = [eps+neps]
    for _ in range(0,l-1):
        wtlst.append(neps)
    ch = random.choices(could_craft,weights=wtlst)
    ch = ch[0]
    agent_host.sendCommand("craft " + ch)
    print("Trying to craft: "+ch)
    setCraftable(ch)
    return rew

# request format [specialist requested, details, clear condition]
# System that coordinates tasks given to it
def RequestHandler(obs):
    global short_term_tasks
    global long_term_tasks
    global complete_list
    remove_list = []
    print("In Request Handler")
    if complete_list:
        for Request in short_term_tasks:
            if condition_cleared(Request[2]):
                remove_list.append(Request)
        for item in remove_list:
            short_term_tasks.remove(item)
        while len(short_term_tasks) < 5 and len(long_term_tasks) > 0:
            if condition_cleared(long_term_tasks[0][2]):
                long_term_tasks.pop(0)
            else:
                short_term_tasks.insert(0,long_term_tasks.pop(0))
        complete_list.clear()
    print("remaining short term tasks:")
    print(short_term_tasks)
    if len(short_term_tasks)>0:
        Accepted_task = short_term_tasks[-1]
        if Accepted_task[0] == "movespecialist":
            MoveRequestHandler(obs, Accepted_task[1])
        elif Accepted_task[0] == "minespecialist":
            MineRequestHandler(Accepted_task[1], obs)
        elif Accepted_task[0] == "craftspecialist":
            CraftRequestHandler(Accepted_task[1])
        elif Accepted_task[0] == "learningspecialist":
            learningHandler(obs)

#Subsystem to handle movement related tasks
def MoveRequestHandler(obs,details):
    global complete_list
    print("in move request handler")
    instruction = details[0]
    instructiondetails = details[1]
    task = details[2]
    if task == "simplemove":
        setPrevObs(obs)
        setFlag("move")
        print("Task is simple move")
        ExecuteAction([instruction])
        complete_list.append("did "+instruction)
    elif task == "search":
        print("Task is search")
        block = instruction
        if instructiondetails == "block":
            if MineSearch(block,obs)>-1:
                complete_list.append("found "+block)
                return
            else:
                instruction = [BlockData[instruction][0], BlockData[instruction][1], BlockData[instruction][2]]
        curloc = [int(obs.get("XPos",0)),int(obs.get("YPos",0)),int(obs.get("ZPos",0))]
        if instruction != curloc:
            print("Doing Request Evaluation")
            MoveRequestEval(obs, instruction)
        else:
            if MineSearch(block,obs)>-1:
                complete_list.append("found "+block)
            else:
                tx = random.choices([10,-10])
                ty = random.choices([1, 0, -1],[0.15,0.7,0.15])
                tz = random.choices([10, -10])
                block_loc_set(block,BlockData[block][0] + tx[0],
                BlockData[block][1] + ty[0],
                BlockData[block][2] + tz[0])

#The algorithm that guides navigation. It is an attempted implementation of A* Algorithm
def MoveRequestEval(obs, dst):
    cur_life = obs.get(u'Life',0)
    plife=getPrevLife()
    self=obs.get(u'self',0)
    x = int(obs.get(u'XPos',0))
    y = int(obs.get(u'YPos',0))
    z = int(obs.get(u'ZPos',0))
    block_move_class(self,x,y,z,cur_life,plife)
    setPrevLife(cur_life)
    setSelfslice(move_slice_state_construct(obs.get(u'slice_self',0)))
    sslice=getSelfslice()
    moveval=float('inf')
    clearStatesToEval()
    chosen = 1
    chosen_action = ""
    for i in range(1,5):
        slice = move_slice_state_construct(obs.get(u'slice_'+str(i),0))
        state = sslice["state"] + slice["state"]
        if state not in StateList.keys():
            move_state_construct(sslice,slice)
        for action in StateList[state]["actions"].keys():
            xmod, zmod = DirMap(i, StateList[state]["actions"][action]["changeXZ"])
            h = StateList[state]["actions"][action]["effort"]/(StateList[state]["actions"][action]["value"] + 1)
            g = Distance(dst[0],dst[1],dst[2],x+xmod,y,z+zmod)
            if (h+g)<moveval:
                chosen = i
                chosen_action = StateList[state]["actions"][action]["action"]
                moveval = h+g
                setChosenState(state)
                setChosenAction(action)
    if chosen_action!="":
        ConstructAction(chosen_action,chosen)

#Subsystem to handle mining requests
def MineRequestHandler(details,obs):
    global complete_list
    setInventory(obs)
    add_available_tools(obs)
    tomine = details[0]
    task = details[1]
    print("in mine request handler")
    #print("Target: ")
    #print(tomine)
    #print("Objective: ")
    #print(task)
    if task=="get":
        tominelist = BlockData[tomine][6]
        mineloc = -1
        for item in tominelist:
            if MineSearch(tomine, obs)>mineloc:
                mineloc = MineSearch(item, obs)
                tomine = item
        if mineloc==-1:
            tomine = random.choices(tominelist)
            tomine = tomine[0]
            makeRequest("movespecialist",[tomine,"block" ,"search"],"found "+tomine)
        else:
            if can_collect(tomine):
                action = MineActionSelect(mineloc)
                tl = viable_tool(tomine)
                agent_host.sendCommand("swapInventoryItems 0 " + str(available_tools[tl]))
                MineActionExecutor(action, tl)
                agent_host.sendCommand("swapInventoryItems " + str(available_tools[tl]) + " 0")
                complete_list.append("got "+tomine)
            else:
                tl = tool_target(tomine) #Remember to have an "unknown" and set up learner for that
                if tl=="":
                    makeRequest("learningspecialist",[],"learned "+str(tomine))
                else:
                    makeRequest("craftspecialist",tl,"made "+str(tl))
    elif task == "mine":
        #action = MineActionSelect(tomine)
        MineActionExecutor(MineMove[tomine], "Hand")
        complete_list.append("mined " + tomine)

#Function that checks if known collection tool for block exists
def tool_target(block):
    for key in BlockData[block][5].keys():
        if BlockData[block][5][key]==10:
            return key
    return ""

#Function that checks if the tool is present
def viable_tool(block):
    for tl in BlockData[block][5].keys():
        if tl in available_tools.keys() and BlockData[block][5][tl]==10:
            return tl

#Function that check if block can be collected
def can_collect(block):
    for tl in BlockData[block][5].keys():
        if tl in available_tools.keys() and BlockData[block][5][tl]==10:
            return True
    return False

#Function that looks for requested block to mine
def MineSearch(obj, obs):
    global BlockData
    mine_state = obs.get(u'mine_box', 0)
    visible = [19, 10, 12, 14, 16, 4, 21, 23, 25, 31]
    visiblestate=[]
    for value in visible:
        visiblestate.append(mine_state[value])
    if obj in visiblestate:
        return visiblestate.index(obj) + 1
    return -1

#Subsystem that handles crafting requests
def CraftRequestHandler(details):
    global complete_list
    tocraft = details
    curInventory = getInventory()
    print("in craft request handler")
    if tocraft in learned_recipes and can_craft(tocraft, curInventory):
        agent_host.sendCommand("craft "+tocraft)
        complete_list.append("made "+tocraft)
    elif tocraft not in learned_recipes:
        makeRequest("learningspecialist",[],"learned "+str(tocraft))
    else:
        neededIngredients = getNeededIngredients(tocraft, curInventory)
        for ingredient in neededIngredients:
            if BlockData[ingredient][4].value == MineType.mine.value:
                makeRequest("minespecialist",[ingredient,"get"],"got "+str(ingredient))
            if BlockData[ingredient][7].value == CraftType.craft.value:
                makeRequest("craftspecialist",ingredient,"made "+str(ingredient))

#Function to make requests to the system
def makeRequest(specialist ,details ,clearcon):
    global short_term_tasks
    global long_term_tasks
    request = [specialist,details,clearcon]
    short_term_tasks.append(request)
    while len(short_term_tasks)>5:
        long_term_tasks.append(short_term_tasks[0])
        short_term_tasks.remove(short_term_tasks[0])

#Function that calculates the ingredients missing from a recipe
def getNeededIngredients(item, materials):
    global BlockData
    ingredientsNeeded=[]
    for recipe in BlockData[item][8]:
        for ingredient in recipe.keys():
            if ingredient in materials.keys():
                if materials[ingredient] < recipe[ingredient]:
                    ingredientsNeeded.append(ingredient)
            else:
                ingredientsNeeded.append(ingredient)
    return ingredientsNeeded

#Function to check if request is completed
def condition_cleared(condition):
    if condition in complete_list:
        return True
    return False

agent_host = MalmoPython.AgentHost()