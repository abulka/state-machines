# Hierarchical - https://github.com/pytransitions/transitions
from transitions.extensions import HierarchicalMachine as Machine

# Set up logging; The basic log level will be DEBUG
import logging
logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
logging.getLogger('transitions').setLevel(logging.INFO)

class TrafficLight(object):
    pass

t = TrafficLight()

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

# Transitioning from multiple states via the same trigger - pity can't specify this in the transitions structure
machine.add_transition('powersurge', 'broken', 'broken_buzzing')
machine.add_transition('powersurge', 'broken_buzzing', 'broken_sparking')


print(t.state)
assert t.state == 'green'
print(machine.get_state(t.state))

t.slowdown()
t.stop()
print(t.state)
assert t.state == 'red'

# same test as in state-demo2-stack
t.throw_rock()  # this should push
assert t.state == 'broken'
assert t.state == 'broken'
t.evening()
assert t.state == 'broken_buzzing'
t.day()
assert t.state == 'broken'

# test two power surges in a row
t.powersurge()
assert t.state == 'broken_buzzing'
t.powersurge()
assert t.state == 'broken_sparking'

# not really push pop at all
t.pop_broken()
assert t.state == 'green'
