# How To Run

    Install pygame

    ```bash
        pip install pygame
    ```

    and then run the main.py

    ```bash
        python main.py
    ```

# Tetris Plus

    The idea is that when even a row is cleared a creazy random even should happen
    I made 4 events
    Gravity Shift: pieces move to the top and start spawn from down
    Double Troble: spawn two pieces insted of one
    Phantom Blocks: the blocks are still there but there hidden
    Flip Screen: rotate the screen 90 deg
    To go back to normal you should clear another row

# Key Points

    I'm using pygame just for the background music


    You could start with Easy Medium or Hard mode where just set the initial_spawn time value

    Everytime a piece move down the score increses by 10 point and when a row is cleared it increses by 1000.
    The Levels start from 1 and the time_spawn for the pieces start from 1000 for easy, 500 for medium and 300 for hard and with each 1000 the level add 1 and
        The time_spawn decreses by 50ms
        untill it reach the min playable time_spawn which is 50(Not that anyone can reach that level).
