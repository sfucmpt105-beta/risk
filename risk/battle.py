import random

import risk
import board.territory as Territory

from risk.errors.battle import *

_MIN_ATTACK_ARMIES = 2

CAPTURED = True

def dice_roll_sequence(att_troop_num, def_troop_num):
    att_dice_num, def_dice_num = \
        _get_attack_and_defend_rolls(att_troop_num, def_troop_num)       
    #roll
    attacker_rolls = [random.randint(1,6) for _ in range(att_dice_num)]
    defender_rolls = [random.randint(1,6) for _ in range(def_dice_num)]
    attacker_rolls.sort(reverse=True)
    defender_rolls.sort(reverse=True)
    
    risk.logger.debug("Attacker Rolls: %s" % attacker_rolls)
    risk.logger.debug("Defenders Tolls: %s" % defender_rolls)
    
    #--calculate losses--
    #find number of pairs of dice to compare (lowest of choices to roll)
    pairs_to_compare = min(att_dice_num, def_dice_num)

    #subtract troops
    for j in xrange(pairs_to_compare):
        if attacker_rolls[j] <= defender_rolls[j]:
            att_troop_num -= 1
        else:
            def_troop_num -= 1

    return att_troop_num, def_troop_num

def _get_attack_and_defend_rolls(attack_armies, defend_armies):
    attack_dice_rolls, defend_dice_rolls = 1, 1
    if (attack_armies > 3):
        attack_dice_rolls = 3
    elif (attack_armies == 3):
        attack_dice_rolls = 2

    if (defend_armies > 1):
        defend_dice_rolls = 2
    return attack_dice_rolls, defend_dice_rolls


def attack(origin, target):
    risk.logger.debug("Attempting to attack %s from %s" % \
        (target.name, origin.name))
    _validate_attack_plan_or_fail(origin, target)
    att_troop_num = origin.armies
    def_troop_num = target.armies
    
    #battle to the death version
    while _have_sufficient_armies(att_troop_num, def_troop_num):
        att_troop_num, def_troop_num = \
            dice_roll_sequence(att_troop_num, def_troop_num)
        risk.logger.debug("Attacker Troops: %s" % att_troop_num)
            risk.logger.debug("Defender Troops: %s" % def_troop_num)

    origin.set_troops(att_troop_num)
    target.set_troops(def_troop_num)
    
    if def_troop_num > 0:
        risk.logger.debug("Attack failed!")
        return not CAPTURED
    else:
        risk.logger.debug("Territory captured!")
        target.owner = origin.owner
        #target.armies = 1
        #origin.armies -= 1
        return CAPTURED

def _validate_attack_plan_or_fail(origin, target):
    if not origin.is_neighbour(target):
        risk.logger.error("Those territories aren't neighbours!")
        raise NonNeighbours(origin, target)
    if origin.owner == target.owner:
        risk.logger.error("Can't attack yourself")
        raise AttackingThyself(origin, target)
    if not origin.armies >= _MIN_ATTACK_ARMIES:
        risk.logger.error("You don't have enough troops to attack!")
        raise InsufficientAttackingArmies(origin)

def _have_sufficient_armies(attacker_armies, defender_armies):
    return attacker_armies >= _MIN_ATTACK_ARMIES and defender_armies > 0

if __name__ == '__main__':
    import risk
    from risk.player import HumonRiskPlayer
    from risk.board.territory import Territory
    test_player1 = HumonRiskPlayer('playa0')
    test_player2 = HumonRiskPlayer('playa1')

    t0 = Territory('winterfell')
    t0.armies = 10
    t1 = Territory('kings_landing')
    t1.armies = 10
    t1.owner = test_player2
    t2 = Territory('riverrun')
    t2.armies = 10
    t2.owner = test_player1

    t2.add_neighbour(t1)

    try:
        attack(t0, t2)
    except NonNeighbours:
        pass
    else:
        raise RuntimeError('Expected error here...')
    
    attack(t2, t1)
    
    t1.armies = 1
    t1.owner = test_player1
    t2.artmies = 10
    t2.owner = test_player2
    try:
        attack(t1, t2)
    except InsufficientAttackingArmies:
        pass
    else:
        raise RuntimeError('Expected error here...')
