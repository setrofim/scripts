"""
You have won a game show and are into the bonus round. Host shows you
three doors and tells you that behind one of them there is a brand new car;
behind the others there are goats. You objective is to pick the the car. You
choose a door. The host the opens a *different* door revealing a goat. He then
asks you if you would like to siwch or to stay with the door you have originally
guessed.

Is it in your interest to switch?

"""
from random import randrange, choice

# 1. setup doors (identify the winning one)
# 2. make a guess
# 3. open a non-winning door
# 4. switch/don't switch
# 5. result: True if won, False other wise
def playround(switch):
    winning_door = randrange(3)
    guessed_door = randrange(3)
    open_door = choice(list(set(range(3)) - set([winning_door]) - set([guessed_door])))
    other_door = (set(range(3)) - set([guessed_door]) - set([open_door])).pop()
    if switch:
        return other_door == winning_door
    else:
        return guessed_door == winning_door


def play(nrounds, switch):
    win_count = 0
    for i in xrange(nrounds):
        if playround(switch):
            win_count += 1
    return win_count


def mean(values):
    return sum(values, 0.0) / len(values)


if __name__ == '__main__':
    print "average switched wins:", mean([play(100, True) for i in range(100)])
    print "average stayed wins  :", mean([play(100, False) for i in range(100)])
