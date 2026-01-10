import logging
from random import randint as ri


logger = logging.getLogger(__name__)


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

    # For numbers 2, 3, 4, 6.
    for die, num in dice_num.items():
        if num == 0:
            continue
        if die == 1 or die == 5:
            continue

        value: int = die
        for i in range(num-1):
            value *= 10

        score += value

    # For number 1.
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

    # For number 5.
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
    logger.debug(f'score: {score}')
    return score

def dice_selection_valid(dice: list[int]) -> bool:
    dice_of_concern: dict[int,int] = {
        2: 0,
        3: 0,
        4: 0,
        6: 0
    }

    # If there are any dice with a number other than 1, 5 in the group:
    for die in dice:
        if die in dice_of_concern:
            dice_of_concern[die] += 1
        
    for num in dice_of_concern.values():
        if num > 0 and num < 3:
            logger.debug(f'valid: False')
            return False
    
    logger.debug(f'valid: True')
    return True

def select_dice(dice: list[int]) -> list[int]:
    indexes: list[int] = []
    selection: list[int] = []
    
    while True:
        choices: str = input('Select dice based on list index:\n> ').strip()
        logger.debug(f'choices: "{choices}"')

        for c in choices:
            if c.isdigit():
                indexes.append(int(c))

        if len(indexes) > len(dice):
            logger.debug('choices > number of dice')
            indexes.clear()
            continue

        logger.debug(f'indexes: {indexes}')
        for i in indexes:
            try:
                selection.append(dice[i])
            except IndexError as ie:
                logger.error(ie)
                break

        if (len(selection) != len(indexes)) or ((not selection) or (not indexes)):
            indexes.clear()
            selection.clear()
            continue

        break
    
    logger.debug(f'selection: {selection}')
    return selection

def is_scorable(dice: list[int]) -> bool:
    if 1 in dice or 5 in dice:
        logger.debug('scorable: True')
        return True
    
    for i in range(1,7):
        if i == 1 or i == 5:
            continue

        count: int = 0
        for die in dice:
            if die == i:
                count += 1
        
        if count >= 3:
            logger.debug('scorable: True')
            return True
        
    logger.debug('scorable: False')
    return False

def turn(num_dice: int = 6) -> int:
    score: int = 0
    used_dice: int = 0
    
    while True:
        dice: list[int] = throw_dice(num_dice - used_dice)
        print(dice)

        scorable: bool = is_scorable(dice)
        if not scorable:
            print('Loss!')

            logger.debug(f'score: {0}')
            return 0

        while True:
            selection: list[int] = select_dice(dice)
            if dice_selection_valid(selection):
                used_dice += len(selection)
                score += score_dice(selection)
                print(f'Remaining: {[die for die in dice if die not in selection]}\nScored: {selection}')
                break
        
        if used_dice == num_dice:
            used_dice = 0
            print('All dice used! Rolling all dice again.')

        if 'n' == input('Keep going? (Y/n)\n> ').lower().strip():
            break
    
    logger.debug(f'score: {score}')
    return score

def throw_dice(num_dice: int) -> list[int]:
    dice: list[int] = [ri(1,6) for i in range(num_dice)]
    dice.sort()

    logger.debug(f'dice: {dice}')
    return dice

def round(player_scores: list[int]) -> None:
    for i in range(len(player_scores)):
        logger.info(f'player {i + 1} turn')

        print(f'\nPlayer {i + 1}\'s turn!\nPlayer {i + 1}\'s score: {player_scores[i]}')
       
        turn_score: int = turn()
        logger.info(f'player {i + 1} turn score: {turn_score}')
        player_scores[i] += turn_score

def game_loop(player_count: int = 2, target_score: int = 5000):
    logger.info('game loop started')

    player_scores: list[int] = [0] * player_count
    round_count: int = 0

    while True:
        round_count += 1
        logger.info(f'Game round: {round_count}')
        round(player_scores)

        for i in range(len(player_scores)):
            if player_scores[i] > target_score:
                print(f'\nPlayer {i + 1} wins!')

                for i in range(len(player_scores)):
                    print(f'Player {i + 1} score: {player_scores[i]}')

                logger.info(f'total player scores: {player_scores}')
                return
