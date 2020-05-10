from statemachine import StateMachine, State  # https://pypi.org/project/python-statemachine/ 

class ParseObjCState(StateMachine):
    def __init__(self, model=None, state_field='state', start_value=None):
        StateMachine.__init__(self, model, state_field, start_value)
        self.stack = []

    def pop(self):
        if len(self.stack) == 0:
            raise RuntimeError("No previous state to pop")
        self.current_state = self.stack.pop()
    
    # States
    neutral = State('Neutral', initial=True)
    aclass = State('in a class definition')
    method = State('InMethod')
    function = State('InFunction')
    # var = State('InVariable')
    waiting_var_type = State('in variable waiting for type identifier')
    waiting_var_name = State('in variable waiting for variable name identifier')

    # Transitions
    _go_var = neutral.to(waiting_var_type) | method.to(waiting_var_type) | function.to(waiting_var_type)
    def go_var(self):
        self.stack.append(self.current_state)
        self._go_var()
    got_var_type = waiting_var_type.to(waiting_var_name)
    def got_var_name(self): self.pop()
    go_function = neutral.to(function) | method.to(function) | function.to(function)
    go_method = aclass.to(method)
    go_class = neutral.to(aclass)

# Test

state = ParseObjCState()
assert state.is_neutral
assert state.current_state == state.neutral
# simulate getting a variable then popping back
state.go_var()
assert state.is_waiting_var_type
state.got_var_type()
assert state.is_waiting_var_name
state.got_var_name()
assert state.is_neutral
# simulate encountering a function then a var within that
state.go_function()
state.go_var()
state.got_var_type()
state.got_var_name()
assert state.is_function  # note the stack popped us back!
