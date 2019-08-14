from socket import *
import _thread

#def generate_printable_board(board):
EXIT_STR = "10000000"
EXIT_BYTE = int(EXIT_STR, 2)
CLIENT_FIRST_STR = "01000000"
CLIENT_FIRST = int(CLIENT_FIRST_STR, 2)
EMPTY_MSG_STR = "00000000"
EMPTY_MSG = int(EMPTY_MSG_STR, 2)
COORDS_SECTION = int("00001111", 2)
BOARD_SIZE = 9
EMPTY_SPACE = ' '
CLIENT_MARK = 'X'
SERVER_MARK = 'O'

def send_msg(socket, msg):
	msg_arr = bytearray()
	msg_arr.append(msg)
	socket.send(msg_arr)

def get_coords(byte_msg):
	return byte_msg & COORDS_SECTION

def make_move_s(board):
	for space in board:
		if space == EMPTY_SPACE:
			space = SERVER_MARK
			return board
	return "FULL"

def make_move_c(board, coord):
	if board[coord] == EMPTY_SPACE:
		board[coord] = CLIENT_MARK
	return board

def check_client_first(socket, board):
	init_msg = socket.recv(1024)[0]
	coord = 0
	
	#If init_msg contains CLIENT_FIRST indicator
	if init_msg & CLIENT_FIRST == CLIENT_FIRST:
		
		#Get client coordinate, then apply their move choice
		coord = get_coords(init_msg)
		make_move_c(board, coord)
	
	return board
	
#Creates and runs new game
#	Game has different port number than original server
#	Communicates with client to play
def run_game(socket, port, addr):
	client_msg = 0
	game_positions = ""
	client_first = False
	
	#Populate board with empty spaces
	for i in range(0, BOARD_SIZE):
		game_positions += EMPTY_SPACE
		
	check_client_first(socket, board)
	
	#Keep running until the user exits
	while not (client_msg == EXIT_BYTE):
		
		#Receive the message
		client_msg = socket.recv(1024)[0]
		
		#If the message is NOT the exit code
		if not client_msg == EXIT_BYTE:
			send_msg(socket, client_msg)
		
	socket.close()
	print("connection closed")
	
#Listens for clients, creates new game instances for each client
def main():
	server_port = 13037
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.bind(('',server_port))
	server_socket.listen(1)
	print('The server is ready to receive')
	while True:
		#addr is a tuple, containing address and port number
		connection_socket, (addr, client_port) = server_socket.accept()
		_thread.start_new_thread(run_game, (connection_socket, client_port, addr))
		
if __name__ == "__main__":
	main()