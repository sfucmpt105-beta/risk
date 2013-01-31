import random

def dice_roll_sequence(att_troop_num, def_troop_num):
    #ask number of dice to roll
    att_dice_num=input("Enter # of attacking dice:")
    while (att_dice_num<1 or att_dice_num>3 or att_dice_num >= att_troop_num):
        att_dice_num=input("Invalid input. \nEnter # of attacking dice:")

    def_dice_num=input("Enter # of defending dice:")
    while (def_dice_num<1 or def_dice_num>2 or def_dice_num >= def_troop_num):
        def_dice_num=input("Invalid input. \nEnter # of defending dice:")
        
    attacker_rolls= [random.randint(1,6) for x in range(att_dice_num)]
    defender_rolls= [random.randint(1,6) for x in range(def_dice_num)]
    attacker_rolls.sort(reverse=True)
    defender_rolls.sort(reverse=True)
        
    print("Attacker Rolls: ", attacker_rolls)
    print("Defenders Tolls: ", defender_rolls)

    #calculate losses
    for j in range(0,def_dice_num):
        if attacker_rolls[j] <= defender_rolls[j]:
            att_troop_num -= 1
        else:
            def_troop_num -= 1
    
    #print att_troop_num
    #print def_troop_num
    return att_troop_num, def_troop_num
    
    
def main():
    #test values
    att_troop_num=10
    def_troop_num=5
    
    #can't attack with only 1 army
    if (att_troop_num==1):
        print "You don't have enough troops to attack!\n"
    else:
        att_troop_num,def_troop_num=dice_roll_sequence(att_troop_num, def_troop_num)
    print "Attacker Troops:", att_troop_num
    print "Defender Troops:", def_troop_num
    
if __name__ == "__main__":
    main()

       
    