from random import randint as ri


def score_dice(dice: list[int]) -> int:
    dice_num: dict[int, int] = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    for die in dice:
        dice_num[die] += 1

    score: int = 0

    # For 2, 3, 4, 6.
    for die, num in dice_num.items():
        if num == 0:
            continue
        if die == 1 or die == 5:
            continue

        value: int = die
        for i in range(num-1):
            value *= 10

        score += value

    # For 1.
    for die, num in dice_num.items():
        if num == 0:
            continue
        if die != 1:
            continue

        value: int = 100
        if num >= 3:
            for i in range(num-2):
                value *= 10
        else:
            value *= num

        score += value

    # For 5.
    for die, num in dice_num.items():
        if num == 0:
            continue
        if die != 5:
            continue

        value: int = 50
        if num >= 3:
            for i in range(num-2):
                value *= 10
        else:
            value *= num

        score += value
    
    # Oh my god...
    return score

def dice_selection_valid(dice: list[int]) -> bool:
    dice_of_concern: dict[int,int] = {
        2: 0,
        3: 0,
        4: 0,
        6: 0
    }

    # If there are any dice other than 1, 5 in the group:
    for die in dice:
        if die in dice_of_concern:
            dice_of_concern[die] += 1
        
    for num in dice_of_concern.values():
        if num > 0 and num < 3:
            return False
    
    return True

def select_dice(dice: list[int]) -> list[int]:
    indexes: list[int] = []
    selection: list[int] = []
    
    while True:
        choices: str = input('Select dice based on list index:\n> ').strip()

        for c in choices:
            if c.isdigit():
                indexes.append(int(c))
        
        if len(indexes) > len(dice):
            continue

        for i in indexes:
            selection.append(dice[i])

        break

    return selection

def round(num_dice: int = 6) -> int:
    score: int = 0
    used_dice: int = 0
    
    while used_dice < 6:
        dice: list[int] = throw_dice(num_dice - used_dice)
        print(dice)

        while True:
            selection: list[int] = select_dice(dice)
            if dice_selection_valid(selection):
                used_dice += len(dice) - len(selection)
                score += score_dice(selection)
                break
        
        if 'n' == input('Keep going?\n> '):
            break

    return score
        

def throw_dice(num_dice: int) -> list[int]:
    dice: list[int] = [ri(1,6) for i in range(num_dice)]
    dice.sort()
    return dice

def game_loop():
    total_score: int = 0

    while True:
        total_score += round()
        if 'y' == input('Quit?\n> '):
            break

    print(f'Total score: {total_score}')
    
    

def main():
    print("Hello from dice-game!")
    game_loop()


if __name__ == "__main__":
    main()
