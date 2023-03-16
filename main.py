from detection import *
from brain import *

if __name__ == '__main__':
    board = Tic()
    board.show()
        
    list_cell_order = []

    while not board.complete():
        player = 'O'

        cell_played = main_function(list_cell_order)
        list_cell_order.append(cell_played)
        # print(list_cell_order)
        time.sleep(5)
        
        cell_played = replace_cell(cell_played)

        player_move = cell_played - 1
        # player_move = int(input('Next Move: ')) - 1
        if player_move not in board.available_moves():
            continue
        board.make_move(player_move, player)
        board.show()

        if board.complete():
            break
        player = get_enemy(player)
        computer_move = determine(board, player)
        board.make_move(computer_move, player)
        board.show()
        
    print('Winner is', board.winner())