"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""

# returns true if board is empty
def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False
    
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    start = "" # "open" if a stone can be placed at the start of the sequence
    end = "" # "open" if a stone can be placed at the end of the sequence
    if board[y_end + d_y][x_end + d_x] == " ":
        end = "open"
    else:
        end = "closed"
    
    if board[y_end + d_y * -length][x_end + d_x * -length] == " ": 
        start = "open"
    else:
        start = "closed"

    if start == "open" and end == "open":
        return "OPEN"
    elif start == "closed" and end == "closed":
        return "CLOSED"
    else:
        return "SEMIOPEN"

def in_bounds(y, x):
    if 0 <= y < 8 and 0 <= x < 8: # Check to see if the coordinates are within the range of the board
        return True
    
    return False

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    y = y_start
    x = x_start

    while in_bounds(y, x) and in_bounds(y + (length - 1) * d_y, x + (length - 1) * d_x):
        current_length = 0
        for i in range(length):
            if board[y + i * d_y][x + i * d_x] == col:
                current_length += 1
            else:
                break

        if current_length == length:
            # Check for openness on both ends
            before_y = y - d_y
            before_x = x - d_x
            after_y = y + length * d_y
            after_x = x + length * d_x

            is_open_before = in_bounds(before_y, before_x) and board[before_y][before_x] == " "
            is_open_after = in_bounds(after_y, after_x) and board[after_y][after_x] == " "

            if is_open_before and is_open_after:
                open_seq_count += 1
            elif is_open_before or is_open_after:
                semi_open_seq_count += 1

        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    board_height = len(board)
    board_width = len(board[0])

    # Check vertical sequences from the top edge
    for x in range(board_width):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1, 0)  # From top edge vertically down
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq

    # Check horizontal sequences from the left edge
    for y in range(board_height):
        open_seq, semi_open_seq = detect_row(board, col, y, 0, length, 0, 1)  # From left edge horizontally right
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq

    # Check diagonals:
    # Down-right diagonals starting from the top edge and left edge
    for x in range(board_width):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1, 1)  # Down-right diagonal from top edge
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    for y in range(1, board_height):  # Skip (0,0) to avoid double-counting
        open_seq, semi_open_seq = detect_row(board, col, y, 0, length, 1, 1)  # Down-right diagonal from left edge
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq

    # Down-left diagonals starting from the top edge and right edge
    for x in range(board_width):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1, -1)  # Down-left diagonal from top edge
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq
    for y in range(1, board_height):  # Skip (0, board_width - 1) to avoid double-counting
        open_seq, semi_open_seq = detect_row(board, col, y, board_width - 1, length, 1, -1)  # Down-left diagonal from right edge
        open_seq_count += open_seq
        semi_open_seq_count += semi_open_seq

    return open_seq_count, semi_open_seq_count

def search_max(board):
    results = {}
    result_max = 0

    # search all squares in board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                # change empty square to black piece to create a test case
                board[i][j] = 'b'

                # score the test case
                results[i,j] = [score(board)]
                # print(results)

                # revert test case back to actual board
                board[i][j] = ' '
    
    # find the max score
    for key in results.keys():
        if results[key][0] > result_max:
            result_max = results[key][0]
    # print(result_max)

    # return the first max score coordinates
    for key in results.keys():
        if results[key][0] == result_max:
            return key
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    # check if 5 in a row exist (note: doesn't check closed case wins)
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    open_b[5], semi_open_b[5] = detect_rows(board, "b", 5)
    open_w[5], semi_open_w[5] = detect_rows(board, "w", 5)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return "Black won"
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return "White won"

# checks if any empty spaces remain on the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                return "Continue playing"
    else:
        return "Draw"

    



def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
       
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    #play_gomoku(8)
    easy_testset_for_main_functions()
    
