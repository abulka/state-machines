# State Machine Experiments

[python-statemachine · PyPI](https://pypi.org/project/python-statemachine/) <- this is the one I'm using, see subdir `python-statemachine`

## 1. python-statemachine - library

https://pypi.org/project/python-statemachine/ 

Reporting state values

```python
print('machine is', t)
print('state is', t.current_state)  # big fat object
print('state (succinct) is', t.current_state.value) # nice short string e.g. 'red'
```

force setting a state
using the transition that lists all possibilities, e.g. emergencyA is one solution
but for brute force just re-init

```python
t = TrafficLightMachine()
print(t.current_state.value)

t = TrafficLightMachine(start_value='yellow')
print(t.current_state.value)
```

## My github issue comment

https://github.com/fgmacedo/python-statemachine/pull/254#issuecomment-625625776

This is a nice - thanks. Presumably its just nicer syntax for doing what you can already do with the `|` approach? 

Some doco on reverse transitions would be nice in the readme, as it was hard wading through pages of issues (having all those auto bot issues in there makes for a lot of noise in the issues) and finding any doco, which is only found in this particular issue, at the moment. 

Also, I feel that some more prominent readme doco on the transition from multiple states `|` approach would be beneficial. Currently there is no documentation, only some code examples found the advanced topics on callbacks and mixins. I actually initially missed out on knowing about the important `|` approach since I had no immediate use for the advanced topics and didn't read them!

Finally, I wonder if something like

```python
cancel = cancelled.from_any()
```
is possible?  Perhaps its not desirable from a state machine computer science point of view? Anyway, I have a situation where I need to do an emergency reset of the state to something specific, and have to currently list all the possible states to transition from, which are all the states. I couldn't be bothered with that so I simply re-initialised the state machine e.g. `t = TrafficLightMachine()` which might be seen as a hack, so `cancelled.from_any()` would be nice!

## push pop

Using the `python-statemachine` library


```python
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
t.day()
assert t.current_state == t.broken

# test two power surges in a row
t.powersurge()
assert t.current_state == t.buzzing
t.powersurge()
assert t.current_state == t.sparking

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
```


# 2. transitions - library

https://github.com/pytransitions/transitions

This is pretty good, but even though it supports nested states, to get out of a nested state you need to trigger into some **specific** state - which is not push pop.  Want to pop to whatever the previous state was, not to a specific state.

Hacked it anyway in a similar way to my 'python-state-machine' library implementation.

```python
# 
# Can we simulate push pop?
# 

class TrafficLight2(object):
    def __init__(self):
        self.stack = []
        self.machine = None  # init later, so that can use 'set_state' method 
                             # which is not created on the model - it is only available on the machine.

    def pop(self):
        if len(self.stack) == 0:
            raise RuntimeError("No previous state to pop to")
        machine.set_state(self.stack.pop())  # need to do this via machine

    def throw_rock_push(self):
        self.stack.append(self.state)
        self.throw_rock()

t = TrafficLight2()

states=['green', 'yellow', 'red', {'name': 'broken', 'children': ['buzzing', 'sparking']}]
transitions = [
    ['slowdown',    'green',            'yellow'],
    ['stop',        'yellow',           'red'],
    ['go',          'red',              'green'],
    ['throw_rock',  '*',                'broken'],
    ['evening',      'broken',          'broken_buzzing'],
    ['day',         ['broken_sparking', 
                     'broken_buzzing'], 'broken'],

    # Since you have to specify a transition, and a specific
    # state to pop to, this is not a push/pop
    # at all, simply nested states.
    ['pop_broken',   'broken',          'green']
]

machine = Machine(t, states=states, transitions=transitions, initial='green')
t.machine = machine  # hack

# Transitioning from multiple states via the same trigger - pity can't specify this in the transitions structure
machine.add_transition('powersurge', 'broken', 'broken_buzzing')
machine.add_transition('powersurge', 'broken_buzzing', 'broken_sparking')

t.slowdown()
t.stop()
assert t.state == 'red'
# t.throw_rock()
t.throw_rock_push()  # this should push
assert t.state == 'broken'
t.evening()
assert t.state == 'broken_buzzing'
t.day()
assert t.state == 'broken'

# test two power surges in a row
t.powersurge()
t.powersurge()
assert t.state == 'broken_sparking'

# attemmpt
t.pop()
assert t.state == 'red'
print(t.state)
```

# other links re state-machines

[python simple state machine - Google Search](https://www.google.com/search?q=python+simple+state+machine&oq=python+simple+state+machine&aqs=chrome..69i57.3903j0j4&sourceid=chrome&ie=UTF-8)

[StateMachine — Python 3 Patterns, Recipes and Idioms](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html)

[FEAT - Reverse transitions on StateMachine by romulorosa · Pull Request #84 · fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine/pull/84)

[Add support for reverse transtitions by fgmacedo · Pull Request #254 · fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine/pull/254)

[simple state machine implementation « Python recipes « ActiveState Code](http://code.activestate.com/recipes/577308-simple-state-machine-implementation/)

[Writing Maintainable Code Using State Machines in Python](https://www.zeolearn.com/magazine/writing-maintainable-code-using-sate-machines-in-python)

[yet another Python state machine (and why you might care) – \[citation needed\]](https://www.talyarkoni.org/blog/2014/10/29/yet-another-python-state-machine-and-why-you-might-care/comment-page-1/)

and there are heaps more...

