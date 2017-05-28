#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

"""
   Author: Henrique Matheus S. Arouca
   E-mail: henriquechanry28@gmail.com

"""

from State import *
from Transition import *
from equivaleceTable import*

class AFD():

    def __init__(self):
        self.stateList      = []    
        self.transitionList = []

    def load(self,fileName):
        file = open(fileName, 'r') 
        text = file.readlines()
        line = 0
        
        tempStateIDLine = ""
        tempTransitionFromLine     = ""
        tempTransitionToLine       = ""
        tempTransitionConsumesLine = ""

        tempStateID    = ""
        tempStateInit  = False
        tempStateFinal = False         

        tempTransitionFrom      = ""
        tempTransitionTo        = ""
        tempTransitionConsumes  = ""

        for x in text:
            if(text[line].find("id=") != -1):
                tempStateIDLine = text[line]
                for i in tempStateIDLine:
                    if(i.isdigit()):
                        tempStateID = tempStateID + i
                    elif(i == "n"):
                        break   

            elif(text[line].find("<initial/>") != -1):
                tempStateInit = True

            elif(text[line].find("<final/>") != -1):
                tempStateFinal = True

            elif(text[line].find("</state>") != -1):
                self.addState(tempStateID,tempStateInit,tempStateFinal)
                tempStateID    = ""
                tempStateInit  = False
                tempStateFinal = False

            elif(text[line].find("from>") != -1):
                tempTransitionFromLine = text[line]

                for x in xrange(0,len(tempTransitionFromLine)):
                    if(tempTransitionFromLine[x].isdigit()):
                        tempTransitionFrom = tempTransitionFrom + tempTransitionFromLine[x]
                    elif((tempTransitionFromLine[x] == "<")and(tempTransitionFromLine[x+1] == "/")):
                        break                

            elif(text[line].find("to>") != -1):
                tempTransitionToLine = text[line]
                for x in xrange(0,len(tempTransitionToLine)):
                    if(tempTransitionToLine[x].isdigit()):
                        tempTransitionTo = tempTransitionTo + tempTransitionToLine[x]
                    elif((tempTransitionToLine[x] == "<")and(tempTransitionToLine[x+1] == "/")):
                        break

            elif(text[line].find("read>") != -1):
                tempTransitionConsumesLine = text[line]
                for x in xrange(0,len(tempTransitionConsumesLine)):
                    if(tempTransitionConsumesLine[x] == ">"):
                        j = x+1
                        while(tempTransitionConsumesLine[j] != "<"):
                            tempTransitionConsumes = tempTransitionConsumes + tempTransitionConsumesLine[j]
                            j = j + 1
                        break    

            elif(text[line].find("</transition>") != -1):
                self.addTransition(tempTransitionFrom,tempTransitionTo,tempTransitionConsumes)
                tempTransitionFrom      = ""
                tempTransitionTo        = ""
                tempTransitionConsumes  = ""

            line = line + 1         

        file.close()

        #Function that load the file in the model of JFLAP (.jff) and create lists of transitions and states of a automaton

    def save(self,fileName):
        file = open(fileName, 'w')

        text = [] 
        text.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.0.--><structure>&#13;\n') 
        text.append('<type>fa</type>&#13;\n') 
        text.append(' <automaton>&#13;\n')          

        for x in self.stateList: #Write States
            text.append('<state id="' + x.getId() + '" name="q' + x.getId() +'">&#13;\n')
            text.append('      <x>0.0</x>&#13;\n')
            text.append('      <y>0.0</y>&#13;\n')
            
            if(x.getInitial()):
                text.append('  <initial/>&#13;\n')


            if(x.getFinal()):
                text.append('  <final/>&#13;\n')

            text.append('</state>&#13;\n')


        text.append('<!--The list of transitions.-->&#13;\n')
       
        for x in self.transitionList: # Write Transitions
            text.append('<transition>&#13;\n')
            text.append('    <from>'+ str(x.getSource()) +'</from>&#13;\n')
            text.append('    <to>'+ str(x.getTarget()) +'</to>&#13;\n')
            text.append('    <read>'+ str(x.getConsumes()) +'</read>&#13;\n')
            text.append('</transition>&#13;\n') 

        text.append(' </automaton>&#13;\n')
        text.append('</structure>\n')   
        
        file.writelines(text) 
        file.close()

        #Function that takes the two lists of transitions and states and saves in a file with a model of JFLAP (.jff)

    def statesEquivalents(self):
        equivalentsList    =  []
        pendencesList      =  [] 
        alphabet           =  self.getAlphabet()
        firstState         = ""
        secondState        = ""
        tempNextFirst      = ""
        tempNextSecond     = ""
    
        for i in self.stateList:
            for j in self.stateList:
                if(i.getId() == j.getId()):
                    pass  #Not verify the state with yourself

                elif(((i.getFinal())and(not j.getFinal()))or((not i.getFinal())and(j.getFinal()))): #A final state and one not final, never be equivalents
                    tempConcat      = str(i.getId()) + "-"+ str(j.getId())
                    tempEquivalence = EquivaleceTable(tempConcat,False)
                    pendencesList.append(tempEquivalence)
                    tempEquivalence = None
                    tempConcat      = ""

                else: #Just completing a table for further analysis
                    tempConcat      = str(i.getId())+ "-" + str(j.getId())
                    tempEquivalence = EquivaleceTable(tempConcat,True)
                    pendencesList.append(tempEquivalence)        
                    tempEquivalence = None
                    tempConcat      = ""
       
        pendencesList = self.removeTransitivity(pendencesList,2)

        for i in pendencesList:            
            for j in alphabet:
                firstState , secondState = i.getIds().split("-")

                tempNextFirst  = self.getNextState(firstState,j)
                tempNextSecond = self.getNextState(secondState,j)
                
                if(str(tempNextFirst) == str(tempNextSecond)):
                    pass #It is not necessary to check the states with themselves

                elif(not i.getEquivalence()):
                    pass #If the state is already false about your equivalence, is not necessary to put into the pendence list   
 
                elif(self.setPendence(pendencesList,str(tempNextFirst),str(tempNextSecond))):                    
                    tempConcat  = str(tempNextFirst) + "-"+ str(tempNextSecond)
                    i.setList(tempConcat)
                    tempConcat  = ""

                else:
                    i.setEquivalence(False)
                    break  #If here is already false, don't need to look the other characters of the alphabet 

        pendencesList = self.LastX(pendencesList)  

        for x in pendencesList:
            if(x.getEquivalence()):
                equivalentsList.append(x.getIds()) 

        return equivalentsList           
        
        #Function that makes and returns a list of equivalent states, this list is made with states that with all characters
        #arrive on the same state, and when don't have aparent equivalence, the function creates a list of pendences, and if in the end 
        #the states that are not in it also go to a equivalent state list.

    def afdEquivalents(self,machine2):
        initialM1   = ""
        initialM2   = ""
        initialList = []
        machine3    = AFD()
        equivalentS = []
        firstState  = ""
        secondState = ""

        for i in self.stateList:
            machine3.addState(i.getId(),i.getInitial(),i.getFinal())

        for i in machine2.stateList:
            machine3.addState(i.getId(),i.getInitial(),i.getFinal())   #Treating the FDA's as one 
        
        for i in self.transitionList:
            machine3.addTransition(i.getSource(),i.getTarget(),i.getConsumes())

        for i in machine2.transitionList:
            machine3.addTransition(i.getSource(),i.getTarget(),i.getConsumes())

        machine3.renumber(0)

        initialList = machine3.getInitialState()
        initialM1   = initialList[0]
        initialM2   = initialList[1]

        equivalentS = machine3.statesEquivalents()

        for i in equivalentS:
            firstState,secondState = i.split("-")

            if(((firstState == str(initialM1))and(secondState == str(initialM2)))or((secondState == str(initialM1))and(firstState== str(initialM2)))):
                return True #the FDAs are equivalent

            firstState  = ""
            secondState = ""     

        return False #The FDAs are not equivalents

        #Function that returns True if the FDAs are equivalent or returns False if they are not
        #This Function take two automatons and assumes that they are one, then runs the states equivalents algorithm and in the end checks if
        #the both initial states are equivalent, if answer is yes, the FDAs are equivalent                    

    def minimum(self):
        firstState            = ""
        secondState           = "" 
        statesEquivalentsList = []
        statesToDeleteList    = []   

        statesEquivalentsList = self.statesEquivalents()
        
        for i in statesEquivalentsList:
            firstState,secondState = i.split("-")
            statesToDeleteList.append(firstState)

            for j in self.transitionList:
                if(str(j.getTarget()) == firstState):
                    j.setTarget(secondState)
                for l in self.stateList:
                    if(l.getId() == firstState):
                        if(l.getInitial()):
                            for k in self.stateList:
                                if(str(k.getId()) == secondState): 
                                    k.setInitial(True)    

        for x in statesToDeleteList:
            self.deleteState(x) #After the targets were tidied and adjusted, the state and the source transition can be deleted too

       #Function that implements the algothm of Moore to minimization of automaton                 

    def complement(self):
        machine2 = AFD()
        machine2.stateList = self.stateList
        machine2.transitionList = self.transitionList         

        for x in machine2.stateList:
            if(x.getFinal() == True):
                x.setFinal(False)
            elif(x.getFinal() == False):
                x.setFinal(True)

        return machine2  

        #Function that returns a another machine with a same states and transions, but where is final state now is no more,
        #and where was not final state now is         
    
    def multMachines(self,machine2,algorithm):
        machine3           = AFD()
        concatIdStates     = ""
        concatTargetStates = ""
        tempInitial        = False
        finalStatesList    = []
        alphabet           = self.getAlphabet() 
        targetI            = ""
        targetJ            = ""

        for i in self.stateList:
            for j in machine2.stateList:
                #Creat States

                concatIdStates = i.getId() + j.getId()
                if((i.getInitial())and(j.getInitial())):
                    tempInitial = True
                machine3.addState(concatIdStates, tempInitial, False)

                #Defines the final states for each algoritm 

                if(algorithm == "union"):
                    if((i.getFinal())or(j.getFinal())):
                        finalStatesList.append(concatIdStates)
                elif(algorithm == "intersection"):
                    if((i.getFinal())and(j.getFinal())):
                        finalStatesList.append(concatIdStates)
                elif(algorithm == "difference"):
                    if((i.getFinal())and(not j.getFinal())):
                        finalStatesList.append(concatIdStates)

                #Creat transitions

                for x in alphabet:
                    targetI = self.getNextState(i.getId(),x)
                    targetJ = machine2.getNextState(j.getId(),x)
                    
                    concatTargetStates = str(targetI) + str(targetJ) 

                    machine3.addTransition(concatIdStates, concatTargetStates, x)

                concatIdStates     = ""
                concatTargetStates = ""
                tempInitial        = False  

        return machine3,finalStatesList

        #Function that multiply every state on the two automatons, and returns the new machine with a new states and transitions, 
        #and also a list with a final states depending on the algorithm
    

    def union(self,machine2):
        machine3,finalStatesList = self.multMachines(machine2,"union")

        for i in machine3.stateList:
            for x in finalStatesList:
                if(str(i.getId()) == x):
                    i.setFinal(True) 

        return machine3 

        #Funcion that makes a union of two automaton    

    def intersection(self,machine2):
        machine3 = AFD()
        machine3,finalStatesList = self.multMachines(machine2,"intersection")
                  
        for i in machine3.stateList:
            for x in finalStatesList:
                if(str(i.getId()) == x):
                    i.setFinal(True)            

        return machine3 

        #Funcion that makes a intersection of two automaton

    def difference(self,machine2):
        machine3,finalStatesList = self.multMachines(machine2,"difference")

        for i in machine3.stateList:
            for x in finalStatesList:
                if(str(i.getId()) == x):
                    i.setFinal(True) 

        return machine3 

        #Funcion that makes a difference of two automaton

    def move(self, initial, word):
        actualState = initial

        for i in xrange(0,len(word)):
            actualState = self.getNextState(actualState,word[i])

        for j in self.stateList:
            if(str(j.getId()) == str(actualState)):
                if(j.getFinal()):
                    return True #Word is Accept in the Language
                else:
                    return False #Word Not Accept in the Language

        #Funcition that walks in the automaton with a word, and in the end says whether the word  is accept because stopped in a final state or
        #does not accept because stopped on the not final state                             
             

    def addState(self, ide, initial, final):
        self.stateList.append(State(ide,initial,final))

        #Function that insert a element on the last position of the list of States

    def deleteState(self,ide):
        self.stateList = [x for x in self.stateList if x.getId() != str(ide)]
        
        for i in self.transitionList:
            for j in self.transitionList:
                if(str(j.getSource()) == str(ide)):        #Made necessary two iterations because on delete one transition the element changes your position
                    self.transitionList.remove(j)         #So it's need restart a sweep on the list

                if(str(j.getTarget()) == str(ide)):
                    self.transitionList.remove(j)

        #Function that removes an element from a StateList, subscribing the list without the element that if wants to delete,
        #Then it deletes all transitions that corresponds to that state

    def addTransition(self,source,target,consume):
        self.transitionList.append(Transition(source,target,consume))

        #Function that insert a element on the last position of the list of Transitions
    
    def deleteTransition(self,source,target,consume):
        source  = str(source)
        target  = str(target)
        
        for i in self.transitionList:
            if((str(i.getSource()) == source)and(str(i.getTarget()) == target)and(i.getConsumes() == consume)):
                self.transitionList.remove(i) 
        
        #Function that removes an element from a TransitionList, if the source, target and consumes are the same

    def removeTransitivity(self,List,typeS):
        firstStateI   = ""
        secondStateI  = ""
        firstStateJ   = ""
        secondStateJ  = ""
        existenceFlag = False
        key           = ""

        if(typeS == 1): #Type 1: Standard string list, the list contains only one field, that are the states
            for i in List:
                firstStateI, secondStateI = i.split("-")
            
                for j in List:
                    firstStateJ, secondStateJ = j.split("-")
                
                    if((firstStateI == secondStateJ)and(secondStateI == firstStateJ)):
                       existenceFlag = True
                       key           = j        

                if(existenceFlag):
                    List.remove(key)
                    existenceFlag = False
                    key           = ""

        elif(typeS == 2): #Type 2: Standard equivalence list, the list contains more then one fields, why that is need to Walk through them, with get function
            for i in List:
                firstStateI, secondStateI = i.getIds().split("-")
            
                for j in List:
                    firstStateJ, secondStateJ = j.getIds().split("-")
                
                    if((firstStateI == secondStateJ)and(secondStateI == firstStateJ)):
                        existenceFlag = True
                        key           = j        

                if(existenceFlag):
                    List.remove(key)
                    existenceFlag = False
                    key           = ""
        

        return List         

        #Function that removes the transitivity in the list of statesEquivalents or pendencesList, depending on type,
        #and returns this new list                   

    def renumber(self,initiation):
        oldNumberList = []
        newNumberList = []
        contNewList   = initiation    

        for i in xrange(0,len(self.stateList)):
            newNumberList.append(str(contNewList))
            contNewList = contNewList + 1

        contNewList = initiation   

        for i in xrange(0,len(self.stateList)):
                oldNumberList.append(self.stateList[i].getId())
                self.stateList[i].setId(contNewList)
                contNewList = contNewList + 1           

        for i in self.transitionList:
            for j in xrange(0,len(oldNumberList)):
                if(str(i.getSource()) == str(oldNumberList[j])):
                    i.setSource(str(newNumberList[j]))

                if(str(i.getTarget()) == str(oldNumberList[j])):
                    i.setTarget(str(newNumberList[j]))    


        #Function that renumber the states of the automaton, starting from a number given on parameter

    def LastX(self,pendencesList):

        for i in pendencesList:
            for j in i.getListA():
                for k in pendencesList:
                    if(k.getIds() == j):
                        if(not k.getEquivalence()):
                            for l in pendencesList:
                                if(l.getIds() == i.getIds()):
                                    l.setEquivalence(False)
        return pendencesList 

        #Function that mark all the states that still have a pendence list, whose states are not equivalents

    def setPendence(self,pendencesList,firstState,secondState):
        firstStateList  = ""
        secondStateList = ""

        if(int(firstState) > int(secondState)):
            firstState,secondState = secondState,firstState  

        for i in pendencesList:
            firstStateList, secondStateList = i.getIds().split("-") 

            if((str(firstState) == firstStateList)and(str(secondState) == secondStateList)):
                if(i.getEquivalence()):
                    return True  

                else:         
                    return False 

        #Function that set in the list of pendences the states that has the possibility be equivalents or not
        #returns true If the states will enter the list, and false if they are not                

    def getInitialState(self):
        initialList = []

        for x in self.stateList:
            if(x.getInitial()):
                initialList.append(x.getId())

        return initialList        

        #Function that returns a list of a initial state id of the automaton
        #List because the FDA's equivalent algorithm        
    
    def getFinalState(self):
        finals = []

        for x in self.stateList:
            if(x.getFinal()):
                finals.append(x.getIde())

        return finals

        #Function that returns a list of final state id of the automaton

    def getNotFinalStates(self):
        notFinal = []

        for x in stateList:
            if(not (x.getFinal())):
                notFinal.append(x.getId())

        return notFinal
        
        #Function that returns a list of  not final state id of the automaton

    def getNextState(self,actualState,char):
        for i in self.transitionList:
            if((str(i.getSource()) == str(actualState))and(i.getConsumes() == char)):
                return i.getTarget()

        #Function the returns the next state where one must walk with a char, or returns error if has no path   

    def getAlphabet(self):
        alphabet = []

        for i in self.transitionList:
            alphabet.append(i.getConsumes())

        alphabet = list(set(alphabet)) #Removes the repeated characters
        
        return alphabet 

        #Function that returns the alphabet of the automaton without repeating characters
                 

    def toString(self):
        tempState      = ""
        tempTransition = ""
        tempResult     = "------------------STATES-----------------\n"

        for x in self.stateList:
            tempState = tempState + x.toString()

        tempResult = tempResult + tempState + "\n---------------TRANSITIONS---------------\n"          

        for x in self.transitionList:
            tempTransition = tempTransition + x.toString()

        tempResult = tempResult + tempTransition + "\n"

        return tempResult  

        #Funtion to debug and see if the dates has been created on the list of States and Transitions           
                            

#Class that make functions envolving FDAs, manipuling two list for that:  statesList (List of all states in one automaton, using the attributes 
#                                                                                      of class State)
#                                                                         transitionList (List of all transitions in on automato using the attributes
#                                                                                          of class transitions)