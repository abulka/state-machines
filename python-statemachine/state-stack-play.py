from statemachine import StateMachine, State  # https://pypi.org/project/python-statemachine/ 

class TrafficLightMachine(StateMachine):
    green = State('Green', initial=True)
    yellow = State('Yellow')
    red = State('Red')

    broken = State('Broken')
    buzzing = State('Buzzing whilst broken')
    sparking = State('Sparking whilst broken')

    slowdown = green.to(yellow)
    stop = yellow.to(red)
    go = red.to(green)

    # throw_rock = any.to(broken)
    throw_rock = broken.from_(
        green, yellow, red
    )
    def throw_rock_push(self):
        self.stack.append(self.current_state)
        self.throw_rock()
    evening = broken.to(buzzing)
    powersurge = broken.to(buzzing) | buzzing.to(sparking)
    day = buzzing.to(broken) | sparking.to(broken)
    # fixed = pop to last good traffic light state

    def __init__(self):
        StateMachine.__init__(self, model=None, state_field='state', start_value=None)
        self.stack = []
    def pop(self):
        if len(self.stack) == 0:
            raise RuntimeError("No previous state to pop to")
        self.current_state = self.stack.pop()

t = TrafficLightMachine()
t.slowdown()
t.stop()
t.go()
t.slowdown()

# t.throw_rock()
t.throw_rock_push()
assert t.current_state == t.broken
t.evening()
assert t.current_state == t.buzzing

# print(t.current_state)
# print(t.green)
# print(t.current_state.value)
# print(t.current_state_value)

# Aha can force current state
# t.current_state = t.green

print(t.current_state.value)
# print(t.stack)
t.pop()
print(t.current_state.value)
assert t.current_state == t.yellow
