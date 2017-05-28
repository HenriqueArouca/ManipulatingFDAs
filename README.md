
                                       
   Author: Henrique Matheus S. Arouca  
   E-mail: henriquechanry28@gmail.com  
  					


Algorithm in python language, that makes the most important functions of a 
Finte Deterministic Automaton;

Class AFD:
								List Of Functions:
                                                                                                                                                        
   ->  Load                 |  -> minimum            |   -> intersection  |  -> deleteState       |  -> getInitialState     |  -> getAlphabet           
   ->  Save                 |  -> complement         |   -> difference    |  -> addTransition     |  -> getFinalState       |  -> toString              
   ->  statesEquivalents    |  -> multMachines       |   -> move          |  -> deleteTransition  |  -> getNotFinalStates   |  -> removeTransitivity    
   ->  afdEquivalents       |  -> union              |   -> addState      |  -> renumber          |  -> getNextState        |  -> lastX                 
                                                                                                                               -> setPendence            


Class State:
     Atribbutes : 
           ID
           Initial
           Final
Class with all gets and sets needed,and fuction toString.
 
-----------------------------------------------------------------------------------------------------------

Class Transition:
     Atribbutes : 
           Source
           Target
           Consumes
Class with all gets and sets needed, and function toString.
