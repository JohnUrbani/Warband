# Text adventure style game where the player leads an army through an invasion
# in which they have to take over territory and recruit as they go. Plays similar
# to Oregon Trail but you can get new members and there aren't random events, every
# run will have the same options at the same areas
import random
SAVE_FILE = 'save.txt'


def main():
    repeat = True
    while repeat:
        choose_game = input('[N]ew Game?\n[C]ontinue?\n[E]xit\n').lower()
        while choose_game != 'n' and choose_game != 'c' and choose_game != 'e':
            choose_game = input('Choose a valid option\n').lower()

        if choose_game == 'n':
            repeat = False
            new_save()
            start()
        elif choose_game == 'c':
            try:
                save = open(SAVE_FILE, 'r')
            except IOError:
                print('No save file found, please choose [N] to create a new game')
            else:
                if save.readline() == '':
                    print('No save data found, please choose [N] to create a new game')
                    save.close()
                else:
                    repeat = False
                    print('Save found')
                    save.close()
                    start()


# Creates or updates the save file into its blank, default, state
def new_save():
    save = open(SAVE_FILE, 'w')
    # File saved with these stats, split by commas
    # save_data[0] Men (0-50)
    # save_data[1] Money (0-infinity)
    # save_data[2] Food (0-infinity)
    # save_data[3:] Claimed Territory (0 or 1) in this order
    # Homeland 0 (Purchase food & men)
    # Forest 0 (Hunt for food, encounter bandits, lose random numbers of men (0-4))
    # Village 0 (Recruit men (Get 0-3 men), buy food, threaten for food and men (Get 0-6 men, 0-20 food, lose 0-2 men))
    # Mountain Pass 0 (Set up camp or continue, if continued, skip to the next forest but lose men from the conditions)
    # Mountain 0 (Continue to forest)
    # Forest 0 (Hunt for food)
    # Village 0 (Recruit men (Get 0-3 men), buy food, threaten for food and men (Get 0-6 men, 0-20 food, lose 0-2 men))
    # Plains 0 (Hunt for food)
    # PreCastle 0 (Set up camp/prep for battle or go to battle immediately)
    # Castle 0 (Lose 8-20 men, if survived you win)
    # Castle after camp 0 (Lose 5-12 men, if survived you win)
    save_data = ['10', '20', '20', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    for val in save_data:
        save.write(val + ',')


def start():
    save = open(SAVE_FILE, 'r')
    save_data = save.readline().split(',')
    for i in range(50):
        print()
    game_loop(save_data)


def game_loop(save_data):
    while int(save_data[0]) > 0 and int(save_data[2]) > 0:
        show_stats(save_data)
        choices(save_data)
        save_game(save_data)


def save_game(save_data):
    save = open(SAVE_FILE, 'w')
    for val in save_data:
        save.write(str(val) + ',')


def show_stats(save_data):
    men = save_data[0]
    gold = save_data[1]
    food_loss = str(int(men) // 2)
    food = save_data[2]
    print('Men: ' + men + '/50     Gold: ' + gold + '     Food: ' + food + '(-' + food_loss + '/travel)\n')


def choices(save_data):
    if save_data[3] == '0':
        level1(save_data)
    elif save_data[4] == '0':
        level2(save_data)
    elif save_data[5] == '0':
        level3(save_data)
    food_loss = str(int(save_data[0]) // 2)
    save_data[2] = str(int(save_data[2]) - int(food_loss))


# Homeland
def level1(save_data):
    print('You and your men begin preparing for their invasion on Castle Bhutan.')
    print("Stepping into the marketplace you wonder what supplies you'll need for")
    print('the journey ahead or if you should hire any more loyal men.')
    print()
    choice = ''
    while choice != 'c':
        choice = (input('[B]uy 5 Food (5 gold)     [H]ire Men (10 gold)     [C]ontinue Onward\n')).lower()
        while choice != 'b' and choice != 'h' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'b' and int(save_data[1]) >= 5:
            save_data[2] = str(int(save_data[2]) + 5)
            save_data[1] = str(int(save_data[1]) - 5)
            print(save_data[1] + ' gold left')
        elif choice == 'b' and int(save_data[1]) < 5:
            print("You don't have enough gold for that!")

        if choice == 'h' and int(save_data[1]) >= 10:
            save_data[0] = str(int(save_data[0]) + 1)
            save_data[1] = str(int(save_data[1]) - 10)
            print(save_data[1] + ' gold left')
        elif choice == 'h' and int(save_data[1]) < 10:
            print("You don't have enough gold for that!")
    print()
    print('You and your men set off on their invasion.')
    save_data[3] = 1


# Forest 1
def level2(save_data):
    print('You enter the nearby forest that leads to the main roads.')
    print('This forest is known for its bandits, some say that they steal')
    print('from the rich and give to the poor. Must not be big fans of yours.')
    print()
    investigated = False
    choice = ''
    while choice != 'c':
        choice = (input('[H]unt for Food     [I]nvestigate Bandits     [C]ontinue Onward\n')).lower()
        while choice != 'h' and choice != 'i' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'h':
            men_lost = random.randint(2, 4)
            food_gained = random.randint(5, 15)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('While hunting for food, your men encountered a party of bandits.')
            print('During the strife,', men_lost, 'men were killed.')
            print('The hunting party returned with', food_gained, 'food.')

        if choice == 'i' and not investigated:
            men_lost = random.randint(0, 1)
            gold_gained = random.randint(3, 12)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[1] = str(int(save_data[1]) + gold_gained)
            print('Your men set out to investigate the forest.')
            print('They stumbled upon the bandit camp unseen and decided to take something back.')
            print('The party returned with', gold_gained, 'stolen gold.')
            if men_lost > 0:
                print('However during the raid,', men_lost, 'man was lost')
            investigated = True
        elif investigated:
            print("Your men don't want to go back to the bandit camp.")

    print()
    print('Exiting the forest you and your men set off to a village along the road.')
    save_data[4] = 1


# Village 1
def level3(save_data):
    # Recruit men (Get 0-3 men), buy food, threaten for food and men (Get 0-6 men, 0-20 food, lose 0-2 men)
    print('The village was lively, having had a good harvest the year before.')
    print('You overhear some of your men question if the villagers needed it all for themselves.')
    print('You walk up to the village elder.')
    print()
    recruited = False
    choice = ''
    while choice != 'c':
        choice = (input('[B]uy 5 Food (4 gold)     [R]ecruit Men     [T]hreaten for Men and Food     [C]ontinue Onward\n')).lower()
        while choice != 'b' and choice != 'r' and choice != 't' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'b' and int(save_data[1]) >= 4:
            save_data[2] = str(int(save_data[2]) + 5)
            save_data[1] = str(int(save_data[1]) - 4)
            print(save_data[1] + ' gold left')
        elif choice == 'b' and int(save_data[1]) < 4:
            print("You don't have enough gold for that!")

        if choice == 'r' and not recruited:
            men_gained = random.randint(0, 3)
            save_data[0] = str(int(save_data[0]) + men_gained)
            print(str(men_gained), 'men want to join your cause.')
            recruited = True
        elif recruited:
            print('No more villagers wish to join you.')

        if choice == 't':
            men_gained = random.randint(0, 6)
            men_lost = random.randint(0, 3)
            food_gained = random.randint(3, 10)
            save_data[0] = str(int(save_data[0]) + men_gained)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('You demand food and men from the village elder.')
            print('The villagers around jumped into action.')
            if men_lost > 0:
                print('The villagers bested', str(men_lost), 'of your men.')
            if men_gained > 0:
                print('However you prevailed, taking', str(men_gained), 'villagers into your party.')
            print('After the assault your men took', str(food_gained), 'food from the villagers.')
            choice = 'c'

    print()
    print('You and your men adventure off towards the mountain pass.')
    save_data[5] = 1


# Mountain Pass
def level4(save_data):
    print(save_data)


# Mountain
def level5(save_data):
    print(save_data)


# Forest 2
def level6(save_data):
    print(save_data)


# Village 2
def level7(save_data):
    print(save_data)


# Plains
def level8(save_data):
    print(save_data)


# PreCastle
def level9(save_data):
    print(save_data)


# Castle Camp
def level10(save_data):
    print(save_data)


# Castle no Camp
def level11(save_data):
    print(save_data)


main()
