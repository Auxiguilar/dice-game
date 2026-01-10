from game_logic import game_loop          


def main():
    print("Hello from dice-game!")
    game_loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting game...')
