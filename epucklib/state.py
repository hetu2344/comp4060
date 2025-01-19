from abc import ABC, abstractmethod

class State(ABC):
    
    _debug = False
    def __init__(self, controller, parent, debug=True):
        self.controller = controller  
        self.parent = parent  # stores all the state variables
        self._debug = debug
        
    @abstractmethod
    def enter(self):  #called every time state is entered.
        pass
    
    @abstractmethod
    def update(self):  #called every tick, a state transition to itself
        # manage the nagivator and access robot state in here.
        pass  ### IMPORTANT: returns the current state, e.g., self or new state transitioned to.
    
    @abstractmethod
    def leave(self):   #called when state is exited.
        pass
    
    def transition_to(self, to_state):  #does transition from current state to a new one, returning the new state
        if (self._debug): print ("entering: "+str(to_state.__class__))
        self.leave()
        to_state.enter()
        return to_state

###########################
## Example of how to make a state class:
# class State_MyState(state.State):
#     def enter(self):
#         pass
#
#     def update(self):
#         pass
#    
#     def leave(self):
#         pass

        
# To use this in your planner, I suggest creating each state of your system as a new class, inheriting the state ABC.
# Then, instantiate these in your planner setup, saving a local copy. This local copy becomes the reference you use to
# transition. For example, my planner setup has the following lines
#
# self.s_find_line = State_FindLine(self.controller, self)
# self.s_follow_line = State_FollowLine(self.controller, self)
#
# Where State_FindLine and State_FollowLine are implemented as classes in the planner file. In the planner update, 
# you simply manage the state and call update on it, e.g.,
#
# self.state = self.state.update()
# 
# Finally, you can implement state transitions within a state using:
# 
# self.transition_to(self.parent.s_follow_line)
# 
# the transition_to method calls the appropriate exit and enter functions

        
