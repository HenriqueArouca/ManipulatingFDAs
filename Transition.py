#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

"""
   Author: Henrique Matheus S. Arouca
   E-mail: henriquechanry28@gmail.com

"""

class Transition():
	__source   = ""
	__target   = ""
	__consumes = ""

	def __init__(self,source,target,consumes):
		self.setSource(source)
		self.setTarget(target)
		self.setConsumes(consumes)

	def getSource(self):
	    return (self.source)

	def setSource(self,source):
	    self.source = source

	def getTarget(self):
	    return (self.target)

	def setTarget(self,target):
	    self.target = target

	def getConsumes(self):
	    return (self.consumes)

	def setConsumes(self,consumes):
	    self.consumes = consumes

	def toString(self):
	    return "From : " + str(self.getSource()) + " to : " + str(self.getTarget()) + " read : " + str(self.getConsumes()) + "\n"                        	

#Class that correspondes to transiton of a one automaton, with attributes: Source  (Number or Char that represents the state Where the transition starts)
#																	      Target   (Number or Char that represents the state from the transition of arrival)
#																	      Consumes (Character read to walk on the automaton) 	
#All the atribbutes are private, and can be acessed only with the functions gets and sets
