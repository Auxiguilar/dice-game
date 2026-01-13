import logging
import time
from random import randint as ri


logger = logging.getLogger(__name__)


T_RATE: float = 1 / 10



#####################
# Display functions #
#####################

def wait(sec: float) -> None:
    time.sleep(sec)

def show_player_turn(player: int, player_score: int) -> None:
    print()
    wait(T_RATE * 2)

    print(f'Player {player}\'s turn')
    wait(T_RATE)

    print(f'Player {player}\'s score: {player_score}')
    wait(T_RATE)

def show_dice(dice: list[int]) -> None:
    print('[', end='')

    for i in range(len(dice) - 1):
        print(f'{dice[i]}', end=', ', flush=True)
        wait(T_RATE / 2)

    print(f'{dice[-1]}]')
    wait(T_RATE)

def get_choices() -> str:
    print('Select dice based on list index:')
    wait(T_RATE)

    return input('> ').strip()

def show_turn_loss() -> None:
    print('Turn loss!')
    wait(T_RATE)

def show_remaining(remaining: list[int]) -> None:
    if remaining and len(remaining) > 1:
        print('Remaining: [', end='')

        for i in range(len(remaining) - 1):
            print(f'{remaining[i]}', end=', ', flush=True)
            wait(T_RATE / 2)

        print(f'{remaining[-1]}]')
        wait(T_RATE)

    else:
        print(f'Remaining:', end='')
        wait(T_RATE / 2)

        print(remaining)
        wait(T_RATE)

def show_scored(selection: list[int], throw_score: int) -> None:
    if selection and len(selection) > 1:
        print('Scored: [', end='')
        wait(T_RATE)

        for i in range(len(selection) - 1):
            print(f'{selection[i]}', end=', ', flush=True)
            wait(T_RATE / 2)
        
        print(f'{selection[-1]}]', end='')
        wait(T_RATE / 2)

    else:
        print(f'Scored:', end=' ')
        wait(T_RATE / 2)

        print(selection, end='')
        wait(T_RATE / 2)

    print(f' for {throw_score}')
    wait(T_RATE)

def show_all_used() -> None:
    print('All dice used!', end=' ')
    wait(T_RATE)

    print('You may roll the full hand again...')
    wait(T_RATE)

def will_continue() -> str:
    print('Keep going?')
    wait(T_RATE)

    return input('> ').lower().strip()

def show_player_score(turn_score: int, player_score: int) -> None:
    print(f'Turn score: {turn_score}')
    wait(T_RATE)

    print(f'Total score: {player_score}')
    wait(T_RATE)

    input('> OK ')
    wait(T_RATE)

def show_winner(player: int, player_score) -> None:
    print()
    wait(T_RATE)

    print(f'Player {player} wins with a score of: {player_score}!')
    wait(T_RATE)

def show_results(player_scores: list[int]) -> None:
    print()
    wait(T_RATE)

    for i in range(len(player_scores)):
        player: int = i + 1

        print(f'Player {player} score: {player_scores[i]}')
        wait(T_RATE)



########################
# Evaluation functions #
########################

def is_scorable(dice: list[int]) -> bool:
    scorable: bool = False

    if 1 in dice or 5 in dice:
        logger.debug('contains 1 or 5')
        scorable = True
    
    for i in range(1,7):
        if i == 1 or i == 5:
            continue

        count: int = 0
        for die in dice:
            if die == i:
                count += 1
        
        if count >= 3:
            logger.debug(f'num of {i} >= 3')
            scorable = True
        
    logger.debug(f'scorable: {scorable}')
    return scorable

def is_valid_choices(indexes: list[int], max_choices: int) -> bool:
    # Checks for duplicate indexes, invalid length, potential out-of-range.
    valid: bool = True

    if not indexes:
        logger.debug('empty list')
        valid = False

    # Invalid length
    if len(indexes) > max_choices:
        logger.debug(f'len(indexes) > max_choices: {len(indexes)} > {max_choices}')
        valid = False

    # Out of range
    for i in indexes:
        if i > max_choices - 1:
            logger.debug(f'index is out of range: {i} > {max_choices - 1}')
            valid = False

    # Duplicate index
    for n in range(len(indexes) - 1):
        if len(set(indexes)) != len(indexes):
            logger.debug(f'duplicate indexes: {indexes}')
            valid = False

    logger.debug(f'valid: {valid}')
    return valid

def is_valid_selection(selection: list[int]) -> bool:
    of_concern: dict[int, int] = {}
    for die in selection:
        if die == 1 or die == 5:
            continue
        if not of_concern.get(die):
            of_concern[die] = 0
        of_concern[die] += 1

    valid: bool = True
    for v in of_concern.values():
        if v < 3:
            logger.debug(f'{v} < 3?')
            valid = False
            break

    logger.debug(f'valid: {valid}')
    return valid



####################################
# Generation and scoring functions #
####################################

def throw_dice(num_dice: int) -> list[int]:
    dice: list[int] = sorted([ri(1,6) for i in range(num_dice)])

    logger.debug(f'dice: {dice}')
    return dice

def select_dice(dice: list[int]) -> tuple[list[int], list[int]]:
    selection: list[int] = []
    remaining: list[int] = []

    while True:
        choices: str = get_choices()
        logger.debug(f'choices: "{choices}"')

        indexes: list[int] = [int(c) for c in choices if c.isdigit()]
        logger.debug(f'indexes: {indexes}')

        if not is_valid_choices(indexes, len(dice)):
            continue

        selection: list[int] = [dice[i] for i in indexes]
        if not is_valid_selection(selection):
            selection.clear()
            continue

        remaining = [dice[i] for i in range(len(dice)) if i not in indexes]

        break

    logger.debug(f'selection: {selection}')
    logger.debug(f'remaining: {remaining}')
    return selection, remaining

def score_dice(dice: list[int]) -> int:
    dice_num: dict[int, int] = {}
    for die in dice:
        if not dice_num.get(die):
            dice_num[die] = 0
        dice_num[die] += 1

    score: int = 0

    for die, num in dice_num.items():

        value: int = 0

        if die == 1 and num >= 3:
            value = die * 1000 # 1000 (1 x 3+)
        elif die == 5 and num < 3:
            value = (die * 10) * num # 50 (5 x 1 | 2)
        elif die == 1:
            value = (die * 100) * num # 100 (1 x 1 | 2)
        else:
            value = die * 100 # x00

        # n x 3+
        for i in range(num - 3):
            value *= 2

        score += value
    
    logger.debug(f'score: {score}')
    return score

def select_and_score(dice: list[int]) -> tuple[int, int]:
    if not is_scorable(dice):
        show_turn_loss()
        return 0, 0
    
    selection, remaining = select_dice(dice)
    num_scored: int = len(selection)
    throw_score: int = score_dice(selection)

    show_remaining(remaining)
    show_scored(selection, throw_score)

    return throw_score, num_scored



##########################
# Control flow functions #
##########################

def turn(num_dice: int = 6) -> int:
    turn_score: int = 0
    used_dice: int = 0
    
    while True:
        logger.info(f'number of dice: {num_dice - used_dice}')
        logger.info(f'used dice: {used_dice}')

        dice: list[int] = throw_dice(num_dice - used_dice)
        show_dice(dice)

        throw_score, num_scored = select_and_score(dice)
        
        if num_scored == 0:
            turn_score = 0
            logger.info('turn loss')
            break

        turn_score += throw_score
        used_dice += num_scored
        
        if used_dice == num_dice:
            used_dice = 0
            
            show_all_used()
            logger.info(f'all dice used')

        if 'n' == will_continue():
            logger.debug('player rerolling')
            break
    
    logger.info(f'turn score: {turn_score}')
    return turn_score

def round(player_scores: list[int], target_score: int) -> bool:
    for i in range(len(player_scores)):
        player: int = i + 1

        show_player_turn(player, player_scores[i])
        logger.info(f'player {player} turn')
       
        turn_score: int = turn()
        player_scores[i] += turn_score

        show_player_score(turn_score, player_scores[i])

        if player_scores[i] >= target_score:
            show_winner(player, player_scores[i])
            logger.debug(f'player {player} score >= target_score')
            logger.info(f'player {player} wins')

            return True
        
    return False



#############
# Main loop #
#############

def game_loop(player_count: int = 2, target_score: int = 10_000):
    logger.info('game loop started')

    player_scores: list[int] = [0] * player_count
    round_count: int = 0

    game_won: bool = False

    while not game_won:
        round_count += 1

        logger.info(f'game round: {round_count}')
        game_won = round(player_scores, target_score)

    show_results(player_scores)
