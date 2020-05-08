# State Machine Experiments

[python-statemachine · PyPI](https://pypi.org/project/python-statemachine/) <- this is the one I'm using, see subdir `python-statemachine`


### other links re state-machines

[python simple state machine - Google Search](https://www.google.com/search?q=python+simple+state+machine&oq=python+simple+state+machine&aqs=chrome..69i57.3903j0j4&sourceid=chrome&ie=UTF-8)

[StateMachine — Python 3 Patterns, Recipes and Idioms](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html)

[FEAT - Reverse transitions on StateMachine by romulorosa · Pull Request #84 · fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine/pull/84)

[Add support for reverse transtitions by fgmacedo · Pull Request #254 · fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine/pull/254)

[simple state machine implementation « Python recipes « ActiveState Code](http://code.activestate.com/recipes/577308-simple-state-machine-implementation/)

[Writing Maintainable Code Using State Machines in Python](https://www.zeolearn.com/magazine/writing-maintainable-code-using-sate-machines-in-python)

[yet another Python state machine (and why you might care) – \[citation needed\]](https://www.talyarkoni.org/blog/2014/10/29/yet-another-python-state-machine-and-why-you-might-care/comment-page-1/)

## doco

reporting state values

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



