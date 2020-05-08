from statemachine import StateMachine, State  # https://pypi.org/project/python-statemachine/ 

# import os, django
# # Add django support - alternative technique
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gituml.settings")
# django.setup()

class TrafficLightMachine(StateMachine):
    green = State('Green', initial=True)
    yellow = State('Yellow')
    red = State('Red')

    slowdown = green.to(yellow)
    stop = yellow.to(red)
    go = red.to(green)

    # jump to red immediately - this is tedious, and requires multiple checks and calls
    emergency1 = green.to(red)
    emergency2 = yellow.to(red)

    # nicer way - using 'reverse transitions; - see https://github.com/fgmacedo/python-statemachine/pull/254 
    emergency = (
        green.to(red) |
        yellow.to(red) |
        red.to(red)
    )

t = TrafficLightMachine()
print(t.current_state)
assert t.current_state == TrafficLightMachine.green
assert t.current_state == t.green
assert t.is_green
assert not t.is_yellow
assert not t.is_red

# query states
print([s.identifier for s in t.states])
# ['green', 'red', 'yellow']


print([trans.identifier for trans in t.transitions])
# ['go', 'slowdown', 'stop']

# Call a transition
t.slowdown()
assert t.is_yellow
assert t.current_state == TrafficLightMachine.yellow
assert t.current_state == t.yellow
print(t.current_state)

# alternate way to call a transition, via a string message
t.run('stop')
assert t.is_red

# more advanced experiments - can we have multiple transitions going into the same state?
# This is horrible
t.go()
t.emergency1()
assert t.is_red

t.go()
t.slowdown()
assert t.is_yellow
if t.is_yellow:
    t.emergency2()
elif t.is_green:
    t.emergency1()
assert t.is_red

# nicer way - can be in any state, and call the emergency transition.
t.go()
assert t.is_green
t.emergency()
assert t.is_red

t.go()
t.slowdown()
assert t.is_yellow
t.emergency()
assert t.is_red

assert t.is_red
t.emergency()
assert t.is_red

print("done.")
