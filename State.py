#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


"""
   Author: Henrique Matheus S. Arouca
   E-mail: henriquechanry28@gmail.com

"""

class State():
    __ide     = 0
    __initial = False
    __final   = False 

    def __init__(self, ide, initial, final):
        self.setId(ide)
        self.setInitial(initial)
        self.setFinal(final)

    def getId(self):
        return (self.ide)

    def setId(self,ide):
        self.ide = ide

    def getInitial(self):    
        return (self.initial) #TRUE to Initial or FALSE to not Initial (isInitial)

    def setInitial(self,initial):
        self.initial = initial 

    def getFinal(self):
        return (self.final)  #TRUE to Final or FALSE to not Final (isFinal)

    def setFinal(self,final):
        self.final = final

    def toString(self):
        return "State Id : " + str(self.getId()) + " Is Initial : " + str(self.getInitial()) + " Is Final : " + str(self.getFinal()) + "\n" 

#Class that correspondes to state of a one automaton, with attributes: Identification (Number or Char that represents the state)
#                                                                     Initial        (Boolean attribute that defines if state is initial or not)
#                                                                     Final          (Boolean attribute that defines if state is final or not)
#All the atribbutes are private, and can be acessed only with the functions gets and sets



