import logging
from game_logic import game_loop

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='game.log',
    level=10,
    format="%(asctime)s - %(levelname)s - %(name)s:%(funcName)s - %(message)s"
)


def main():
    logger.info('game started')
    print('Hello from dice-game!')
    game_loop()
    logger.info('game completed, exited')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt, game exited.')
        print('\nExiting game...')
