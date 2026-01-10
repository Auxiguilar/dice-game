import sys
import logging
from game_logic import game_loop

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='game.log',
    level=10 if '--debug' in sys.argv[1::] else 20,
    format="%(asctime)s - %(levelname)s - %(name)s:%(funcName)s - %(message)s"
)


def main():
    logger.info('game started')
    print('Hello from dice-game!')
    game_loop()
    logger.info('game completed, exited')
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt, game exited.')
        print('\nExiting game...')
        sys.exit(1)
