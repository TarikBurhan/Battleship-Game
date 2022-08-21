from network import *


def main():
    print("Game will be on localhost with port 8000.\n")
    host = 'localhost'
    port = 8000
    is_host = None
    win_status = False
    turn = None
    enemy_hit = False
    move = None

    while True:
        host_or_join = input("Do you want to host or join? (H for host, J for join)\n")
        if(host_or_join.upper() == "H"):
            is_host = True
            turn = False
            break
        elif(host_or_join.upper() == "J"):
            is_host = False
            turn = True
            break

    network = Network(host, port, is_host)

    my_board = create_board()
    enemy_board = create_board()
    
    place_ships(my_board, enemy_board)
    print("All ships deployed")

    while(check_ships(my_board) != False):
        if(turn == True):
            x, y = get_shoot_coords(enemy_board)
            move = str(x) + str(y) + str(enemy_hit)[0]
            network.send(bytes(move, 'utf-8'))
        else:
            print("Waiting for response from opponent. \n")
            data = network.receive()
            if not data:
                win_status = True
                break 
            data = data.decode('utf-8')
            enemy_shot_x = int(data[0])
            enemy_shot_y = int(data[1])
            your_shot_hit = data[2]
            is_hit = False
            
            if(your_shot_hit == "T"):
                is_hit = True

            enemy_hit = is_enemy_attack_valid(enemy_shot_x, enemy_shot_y, my_board)

            if(enemy_hit == True):
                update_self_board(enemy_shot_x, enemy_shot_y, my_board)
            
            if move != None:
                update_enemy_board(x, y, is_hit, enemy_board)

            print_boards(my_board, enemy_board)

        turn = not turn
            
    if(win_status == True):
        print("You won.\n")
    else:
        print("You lost.\n")

def x():
    q = "011"
    z= bytes(q, 'ascii')

    print(z)


if __name__ == "__main__":
    x()
    main()