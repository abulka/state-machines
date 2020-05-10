from transitions import Machine

class Matter(object):
    pass

lump = Matter()


# machine = Machine(model=lump, states=['solid', 'liquid', 'gas', 'plasma'], initial='solid')
# # Lump now has state!
# lump.state
# assert lump.state == 'solid'

# The states
states=['solid', 'liquid', 'gas', 'plasma']

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    { 'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
    { 'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas' },
    { 'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas' },
    { 'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma' }
]

# Initialize
machine = Machine(lump, states=states, transitions=transitions, initial='liquid')

# Now lump maintains state...
lump.state
assert lump.state == 'liquid'

# And that state can change...
lump.evaporate()
lump.state
assert lump.state == 'gas'
lump.trigger('ionize')
lump.state
assert lump.state == 'plasma'
