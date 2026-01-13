import sys
import logging
from game_logic import game_loop

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='game.log',
    level=logging.DEBUG if '--debug' in sys.argv[1::] else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s:%(funcName)s - %(message)s"
)


def main():
    print('Hello from dice-game!')
    logger.info('game started')
    
    game_loop()

    print('\nGame complete, exiting...')
    logger.info('game completed, exited')
    
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt, game exited.')
        print('\nExiting game...')
        sys.exit(1)
