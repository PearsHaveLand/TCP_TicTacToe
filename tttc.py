#Client requirements:
#	set up TCP socket
#	get user input
#	validate user input?
#	receive win condition

# | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
# |---||--|       |--coordinates--|
# pos 0: exit
# pos 1: client makes first most
# exit bits set to 1 upon exit choice

from socket import *

EXIT_STR = "10000000"
EXIT_BYTE = int(EXIT_STR, 2)
CLIENT_FIRST_STR = "01000000"
CLIENT_FIRST = int(CLIENT_FIRST_STR, 2)
EMPTY_MSG_STR = "00000000"
EMPTY_MSG = int(EMPTY_MSG_STR, 2)
COORDS_SECTION = int("00001111", 2)
BOARD_SPOTS = [' ', ' ',' ', ' ',' ', ' ',' ', ' ',' ']

#Returns numerical representation of binary string str_dec
def get_bin(str_dec):
    return int(str, 2)

def get_coords(byte_msg):
    return byte_msg & COORDS_SECTION

#Uses a provided string to generate a message to send to the server
#Populates a byte of information
def generate_message(str):
    if str == "exit":
        return EXIT_BYTE
    #Since this will only be called after validating input, there is
    #no need to further validate input
    else:
        return int(str)
    
#Ensures that the user's input meets the standards of the protocol
def validate_input(str):
    #First, check if exiting
    if str == "exit":
        return True
        
    #Next, check if numerical coordinates are correct
    elif str.isdigit() and len(str) == 1:
    
        #If both numbers are between 0 and 2, inclusive
        if int(str) <= 8 and int(str) >= 0:
            return True
    
    #If none of these conditions are met, return false
    return False

#function to get user input
#returns a string indicating the coordinates selected by the user
def get_input():
    valid_input = False
    user_input = ''
    #Until valid input is entered, continue prompting user
    while not valid_input:
        print("Enter a position (0 to 8), or 'exit' to quit.")
        user_input = str(input("Coordinates: "))
        valid_input = validate_input(user_input)
        
    # Handle exit
    if user_input != "exit":
        BOARD_SPOTS[int(user_input)] = 'X'

    return generate_message(user_input)
    
def send_input(socket, msg):
    msg_arr = bytearray()
    msg_arr.append(msg)
    socket.send(msg_arr)
    
def recv_msg(socket):
    return socket.recv(1024)[0]
    
def make_move_s(position):
    BOARD_SPOTS[position] = 'O'
    return "FULL"

def init_game(socket, client_first):
    msg = 0
    if(client_first):
        msg = CLIENT_FIRST
    else:
        msg = EMPTY_MSG
    send_input(socket, msg)
    
def run_game(socket, me_first=False):
    msg = bytearray()
    
    #Whether or not the player wishes to exit the game
    game_exit = False
    
    init_game(socket, me_first)
    
    #While the player continues to play the game, do not exit
    while not game_exit:

        # Wait for server move
        msg = recv_msg(socket)
        print("server message:", msg)
        make_move_s(get_coords(msg))

        render_board()

        msg = get_input()
        if(msg == EXIT_BYTE):
            game_exit = True
        send_input(socket, msg)	
    return
    
def render_board():
    display = ""
    for index in range(len(BOARD_SPOTS)):
        if index % 3 == 0:
            display += '\n' + BOARD_SPOTS[index]
        else:
            display += '|' + BOARD_SPOTS[index]
    print(display)
    

def main():
    server_name = input("Enter the IP address of the tic-tac-toe server: ")
    server_port = 13037
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    run_game(client_socket)
    client_socket.close()
    #coords = get_input()
    #client_socket.send(coords.encode())
    
if __name__ == "__main__":
    main()