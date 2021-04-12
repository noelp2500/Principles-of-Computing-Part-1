# Yahtzee
# Author - Noel Pereira
# Submission - http://www.codeskulptor.org/#user47_h4UDnzP50xau3MU.py

####################################################################

"""
    Planner for Yahtzee
    Simplifications:  only allow discard and roll, only score against upper level
    """

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
        Iterative function that enumerates the set of all sequences of
        outcomes of given length.
        """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
        Compute the maximal score for a Yahtzee hand according to the
        upper section of the Yahtzee score card.
        
        hand: full yahtzee hand
        
        Returns an integer score
        """
    dice_scores = {}
    for dice in hand:
        dice_scores[dice] = dice_scores.get(dice,0) + dice
    return max(dice_scores.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
        Compute the expected value based on held_dice given that there
        are num_free_dice to be rolled, each with num_die_sides.
        
        held_dice: dice that you will hold
        num_die_sides: number of sides on each die
        num_free_dice: number of dice to be rolled
        
        Returns a floating point expected value
        """
    outcomes = [dummy_x for dummy_x in range(1, num_die_sides+1)]           # possible outcome
    free_roll = gen_all_sequences(outcomes, num_free_dice)                  # possible hand by free dice
    score_roll = [score(dummy_x + held_dice) for dummy_x in free_roll]      # scores of hand
    return sum(score_roll)/float(num_die_sides**num_free_dice)

def check_subset(hold_temp, hold_dice, hand):
    """
        A simple helper function for gen_all_holds,
        hold_dice: dice tends to hold
        hold_temp: new hold with hold_dice
        hand: full yahtzee hand
        return True if the new hold is a subset of hand
        """
    count_hand_dice = 0  # count the number of hold dice occured in hand
    count_hold_dice = 0  # count the number of hold dice occured in hold
    for dice in hand:
        if dice == hold_dice:
            count_hand_dice += 1
    for dice in hold_temp:
        if dice == hold_dice:
            count_hold_dice += 1

    if count_hold_dice > count_hand_dice:
        return False
    return True

def gen_all_holds(hand):
    """
        Generate all possible choices of dice from hand to hold.
        
        hand: full yahtzee hand
        
        Returns a set of tuples, where each tuple is dice to hold
        """
    all_hold = set([()])
    hold_new = set([tuple([dummy_dice]) for dummy_dice in hand])
    all_hold.update(sorted(hold_new))
    
    for dummy_idx in range(len(hand)):
        hold_prev = hold_new.copy()
        hold_new = set()
        for hold in hold_prev:
            for dice in hand:
                hold_temp = tuple(sorted([dice] + list(hold)))  # add new dice in hold
                if check_subset(hold_temp, dice, hand):         # check the new hold in a subset of full hand
                    hold_new.add(hold_temp)
        all_hold.update(hold_new)
    return all_hold

def strategy(hand, num_die_sides):
    """
        Compute the hold that maximizes the expected value when the
        discarded dice are rolled.
        
        hand: full yahtzee hand
        num_die_sides: number of sides on each die
        
        Returns a tuple where the first element is the expected score and
        the second element is a tuple of the dice to hold
        """
    all_hold = gen_all_holds(hand)
    best_expected_value = float('-inf')
    best_hold = tuple()
    
    print all_hold
    for held_dice in all_hold:
        num_free_dice = len(hand) - len(held_dice)
        temp_value = expected_value(held_dice, num_die_sides, num_free_dice)
        if temp_value > best_expected_value:
            best_expected_value = temp_value
            best_hold = tuple(held_dice)
    return (best_expected_value, best_hold)


#def run_example():
#    """
#        Compute the dice to hold and expected score for an example hand
#        """
#    num_die_sides = 6
#    hand = (1, 1, 1, 5, 6)
#    hand_score, hold = strategy(hand, num_die_sides)
#    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


#run_example()

