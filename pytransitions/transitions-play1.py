from transitions import Machine  # https://github.com/pytransitions/transitions
# Set up logging; The basic log level will be DEBUG
import logging
logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
logging.getLogger('transitions').setLevel(logging.INFO)

class TrafficLight(object):
    pass

t = TrafficLight()

states=['green', 'yellow', 'red', 'broken', 'buzzing', 'sparking']
transitions = [
    ['slowdown',    'green',    'yellow'],
    ['stop',        'yellow',   'red'],
    ['go',          'red',      'green'],
    ['throw_rock2',  '*',       'broken'],
    ['throw_rock',  ['green', 
                     'yellow',
                     'red'],    'broken'],
    ['evening',      'broken',  'buzzing'],
    ['day',         ['sparking', 
                     'buzzing'], 'broken'],

    # cannot do this, must use 'add_transition' calls for this multi stuff
    # 
    # ['powersurge',  ['broken', 
    #                  'buzzing'], ['buzzing', 
    #                               'sparking']],
]
# transitions = [
#     { 'trigger': 'slowdown',    'source': 'green',          'dest': 'yellow'},
#     { 'trigger': 'stop',        'source': 'yellow',         'dest': 'red'},
#     { 'trigger': 'go',          'source': 'red',            'dest': 'green'},
#     { 'trigger': 'throw_rock',  'source': '*',              'dest': 'broken'}
# ]

machine = Machine(t, states=states, transitions=transitions, initial='green')

# Transitioning from multiple states via the same trigger - pity can't specify this in the transitions structure
machine.add_transition('powersurge', ['broken'], 'buzzing')
machine.add_transition('powersurge', 'buzzing', 'sparking')

# this is not needed - figured out how to do it in the transition data structure directly
# machine.add_transition('day', 'sparking', 'broken')
# machine.add_transition('day', 'buzzing', 'broken')

print(t.state)
assert t.state == 'green'
print(machine.get_state(t.state))

t.slowdown()
t.stop()
print(t.state)
assert t.state == 'red'

t.throw_rock()
assert t.state == 'broken'

# quick way to set state
t.to_green()
assert t.state == 'green'
t.to_broken()
assert t.state == 'broken'

# same test as in state-demo2-stack
# t.throw_rock_push()
# t.throw_rock()
assert t.state == 'broken'
t.evening()
assert t.state == 'buzzing'
t.day()
assert t.state == 'broken'

# test two power surges in a row
t.powersurge()
assert t.state == 'buzzing'
t.powersurge()
assert t.state == 'sparking'
