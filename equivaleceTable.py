#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

"""
   Author: Henrique Matheus S. Arouca
   E-mail: henriquechanry28@gmail.com

"""

class EquivaleceTable():
     
    __ids         = ""
    __equivalence = False
    __listP       = None     

    def __init__(self,ids,equivalence):
        self.setIds(ids)
        self.setEquivalence(equivalence)        
        self.__listP = []

    def getIds(self):
        return self.ids

    def setIds(self,ids):
        self.ids = ids

    def getEquivalence(self):
        return self.equivalence

    def setEquivalence(self,equivalence):
        self.equivalence = equivalence

    def getListA(self):
    	return self.__listP #returns list without pipes

    def getList(self):
    	tempList = ""
    	for x in self.__listP:
    		tempList = tempList + "-" + " || " +x
        return tempList

    def setList(self,element):
    	firstState,secondState = element.split("-")

    	if(int(firstState) > int(secondState)):
    		firstState, secondState = secondState,firstState
    		element = str(firstState) + "-" + str(secondState)

        self.__listP.append(element)       

    def clearPendenceList(self):
    	self.__listP = None

    
    def toString(self):    	
        return "Ids: " + self.getIds() + " Equivalence: " + str(self.getEquivalence()) + " List: " + self.getList() + "\n"
         
#Class that correspondes to equivalence table of algorithm of equivalence  of states, with attributes: 
#                                                                 Identifications (Number or Char that represents the states)
#                                                                 Equivalence     (Boolean attribute that defines if the states is equivalent or not)
#                                                                 List            (List of pendences, attribute that contains the states pendences for analisys)
#All the atribbutes are private, and can be acessed only with the functions gets and sets

