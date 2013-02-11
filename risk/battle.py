import random
import board.territory as Territory


class Battle():
    def __init__(self,origin,target):
        self.origin= origin
        self.target= target
        #test values
        origin.set_ownership(1)
        origin.adjust_troops(10)
        target.set_ownership(2)
        target.adjust_troops(4)
        
    
    def dice_roll_sequence(self, att_troop_num, def_troop_num):
        
        #battle to the death version
        if (att_troop_num>3):
            att_dice_num = 3
        elif (att_troop_num == 3):
            att_dice_num = 2
        elif (att_troop_num == 2):
            att_dice_num = 1
        if (def_troop_num>1):
            def_dice_num = 2
        elif (def_troop_num == 1):
            def_dice_num = 1
            
        #roll
        attacker_rolls= [random.randint(1,6) for x in range(att_dice_num)]
        defender_rolls= [random.randint(1,6) for x in range(def_dice_num)]
        attacker_rolls.sort(reverse=True)
        defender_rolls.sort(reverse=True)
        
        print("Attacker Rolls: ", attacker_rolls)
        print("Defenders Tolls: ", defender_rolls)
        
        #--calculate losses--
        #find number of pairs of dice to compare (lowest of choices to roll)
        if (att_dice_num > def_dice_num):
            pairs_to_compare = def_dice_num
        elif (def_dice_num > att_dice_num):
            pairs_to_compare = att_dice_num
        #subtract troops
        for j in range(0,pairs_to_compare):
            if attacker_rolls[j] <= defender_rolls[j]:
                att_troop_num -= 1
            else:
                def_troop_num -= 1

        return att_troop_num, def_troop_num


    def attack(self):
        if self.origin.is_neighbour(self.target) == False:
            print("Those territories aren't neighbours!")
            return False
        if self.origin.owner == self.target.owner:
            print("Can't attack yourself")
            return False
        
        
        att_troop_num= self.origin.army_total
        def_troop_num= self.target.army_total
        
        #can't attack with only 1 army
        if (att_troop_num < 2):
            print("You don't have enough troops to attack!")
            return False

        while (att_troop_num > 1) and (def_troop_num > 0):
            att_troop_num,def_troop_num= self.dice_roll_sequence(att_troop_num, def_troop_num)
            print "Attacker Troops:", att_troop_num
            print "Defender Troops:", def_troop_num

        self.origin.set_troops(att_troop_num)
        self.target.set_troops(def_troop_num)
        
        if (def_troop_num > 0):
            print "Attack failed!"
        else:
            print "Territory captured!"
            self.target.set_ownership(self.origin.owner)
            
            move_troops = input("How many troops will you move? ")
            while (move_troops < 1 or move_troops >= att_troop_num):
                if (move_troops < 1):
                    print "You must move at least 1 army!"
                elif (move_troops >= att_troop_num):
                    print "The max you can move is ", att_troop_num-1
                move_troops = input("How many troops will you move? ")
                
            self.target.adjust_troops(move_troops)
            self.origin.adjust_troops(-move_troops)
        
if __name__ == "__main__":
    Battle.attack()
    