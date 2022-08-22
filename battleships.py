"""
    Main functions for Battleship Game
"""


SHIP_LENGTHS = [CARRIER, BATTLESHIP, CRUISER, SUBMARINE, DESTROYER] = 5, 4, 3, 3, 2

SHIP_NAMES = {
                CARRIER: "Carrier",
                BATTLESHIP: "Battleship",
                CRUISER: "Cruiser",
                DESTROYER: "Destroyer",
                SUBMARINE: "Submarine"
             }

BOARD_FIELD = [EMPTY, MY_SHIP_ALIVE, MY_SHIP_SUNK, MY_SHIP_MISS, ENEMY_SHIP_SUNK, ENEMY_SHIP_MISS] = 0, 1, -1, 3, 2, -2

def create_board():
    """
    Returns 10x10 2 dimensional array to create board
    """
    return [[0] * 10 for i in range(10)]

def coord_valid(coordination):
    """
    Returns boolean value whether given coordination is in range 0 to 10
    """
    if(0 <= coordination <= 9):
        return True
    else:
        return False

def is_placement_valid(x1, y1, x2, y2, my_board):
    if(x1 == x2):
        for i in range(y1, y2 + 1):
            if(my_board[x1][i] != EMPTY):
                return False
    else:
        for i in range(x1, x2 + 1):
            if(my_board[i][y1] != EMPTY):
                return False
    return True

def print_boards(my_board, enemy_board):
    """
    Prints both players and enemy board with its ships.

    :param my_board: Your board
    :param enemy_board: Enemy board
    """
    print("""
        ■: Your ship that alive, X: Your ship that sunk,
        □: Enemy ship that sunk, M: Your missed attack\n""")
    boards = "      Your Board  \t\t       Enemy Board\n\r"
    boards += "  0|1|2|3|4|5|6|7|8|9 \t\t  0|1|2|3|4|5|6|7|8|9\n"
    for i, rows in enumerate(zip(my_board, enemy_board)):
        for j, entries in enumerate(rows):
            boards += f"{i}|"
            for entry in entries:
                if(entry == EMPTY):
                    boards += " "
                elif(entry == MY_SHIP_ALIVE):
                    boards += "■"
                elif(entry == MY_SHIP_SUNK):
                    boards += "X"
                elif(entry == MY_SHIP_MISS):
                    boards += "X"
                elif(entry == ENEMY_SHIP_SUNK):
                    boards += "□"
                elif(entry == ENEMY_SHIP_MISS):
                    boards += "M"
                
                boards += "|"
            if not j:
                boards += " \t\t"
        boards += "\n\r"
    print(boards)

def get_placement_coords(ship_type):
    """
    Get coordinates from the player with the given coordinates.

    :param ship_type: Ship type from the SHIP_LENGTHS list.
    """
    length = ship_type
    while True:
        input_string = input(f"""Place your {SHIP_NAMES.get(ship_type)} type ship with length of {length}. (Format example: X1Y1 X2Y2 like 01 21) \n""")
        if(len(input_string) != 5):
            print("You typed in wrong format.\n")
        else:
            try:
                x1 = int(input_string[0])
                y1 = int(input_string[1])
                x2 = int(input_string[3])
                y2 = int(input_string[4])
            except:
                print("Coordinates must be integers.\n")
            else:
                if(coord_valid(x1) & coord_valid(y1) & coord_valid(x2) & coord_valid(y2) == False):
                    print("Coordinates must be between 0 and 9.\n")
                else:
                    if(x1 == x2):
                        if(y1 == y2):
                            print("Both coordinates can not be same.\n")
                        elif(y1 > y2):
                            print("Y1 coordinate should be lower than Y2. Change the order of the coordinates.\n")
                        else:
                            if(abs(y2 - y1) + 1 != length):
                                print(f"Your ship length does not match with {SHIP_NAMES.get(ship_type)}.\n")
                            else:
                                return x1, y1, x2, y2
                    else:
                        if(y1 != y2):
                            print("Your ship can not be diagonal.")
                        elif(x1 > x2):
                            print("X1 coordinate should be lower than Y2. Change the order of the coordinates.\n")
                        else:
                            if(abs(x2 - x1) + 1 != length):
                                print(f"Your ship length does not match with {SHIP_NAMES.get(ship_type)}.\n")
                            else:
                                return x1, y1, x2, y2

def place_ship(x1, y1, x2, y2, board):
    """
    Place ship between given coordinates.

    :param x1: First X-axis coordinate
    :param y1: First Y-axis coordinate
    :param x2: Second X-axis coordinate
    :param y2: Second Y-axis coordinate
    :param board: Board to place ship
    """
    if(is_placement_valid(x1, y1, x2, y2, board) == True):
        if(x1 == x2):
            for i in range(y1, y2 + 1):
                board[x1][i] = MY_SHIP_ALIVE
        else:
            for i in range(x1, x2 + 1):
                board[i][y1] = MY_SHIP_ALIVE
        print("Ship has been deployed.\n")
        return True
    else:
        print("You have already have ship in these coordinates.\n")
        return False

def place_ships(my_board, enemy_board):
    """
    Place all ships in the game.
    :param my_board: Board that ships will be deployed
    :param enemy_board: Enemy board that needs to be checked
    """
    total_ship_count = len(SHIP_LENGTHS)
    while True:
        coords = get_placement_coords(SHIP_LENGTHS[total_ship_count - 1])
        if(place_ship(*coords, my_board) == True):
            total_ship_count -= 1
            print_boards(my_board, enemy_board)
        if(total_ship_count == 0):
            return True

def is_enemy_attack_valid(x, y, my_board):
    """
    Checks whether enemy shot is sunk the ship or missed it
    :param x: x-axis value
    :param y: y-axis value
    :param my_board: Which board that needs to be checked
    """
    if(my_board[x][y] == MY_SHIP_ALIVE):
        return True
    else:
        return False

def is_attack_valid(x, y, enemy_board):
    """
    Checks whether players shot never done before
    :param x: x-axis value
    :param y: y-axis value
    :param enemy_board: Which board that needs to be checked
    """
    if(enemy_board[x][y] == EMPTY):
        return True
    else:
        return False

def update_self_board(x, y, my_board):
    """
    Changes players board according to enemy's shot
    :param x: x-axis value
    :param y: y-axis value
    :param my_board: 
    """
    if(my_board[x][y] == EMPTY):
        my_board[x][y] = MY_SHIP_MISS
    elif(my_board[x][y] == MY_SHIP_ALIVE):
        my_board[x][y] = MY_SHIP_SUNK

def update_enemy_board(x, y, response, enemy_board):
    """
    Changes enemy's board according to players shot
    :param x: x-axis value
    :param y: y-axis value
    :param response: Response from the enemy player that whether there is a ship or not
    :param enemy_board: Which board that needs to be checked
    """
    if(response == True):
        enemy_board[x][y] = ENEMY_SHIP_SUNK
    else:
        enemy_board[x][y] = ENEMY_SHIP_MISS

def check_ships(player_board):
    """
    Check whether there are ships remaining in player board.
    :param player_board: Which board that needs to be checked
    """
    for i, rows in enumerate(player_board):
        for ship_status in rows:
            if(ship_status == MY_SHIP_ALIVE):
                return True
    
    print("All of your ships have been sunk.\n")
    return False

def get_shoot_coords(enemy_board):
    """
    Get attack coordinates from the player and return them
    :param enemy_board: Enemy player board that need to be checked
    """
    while True:
        input_string = input("Give attack coordinates. (Format example: X1Y1 like 67)\n")
        if(len(input_string) != 2):
            print("You need to enter 2 coordinate.\n")
        else:
            try:
                x = int(input_string[0])
                y = int(input_string[1])
            except:
                print("Coordinates must be integers.\n")
            else:
                if(is_attack_valid(x, y, enemy_board) == False):
                    print("You cannot attack the same coordinate.\n")
                else:
                    return x, y

