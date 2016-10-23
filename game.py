import Server
import sys
import socket
import time
import copy

# server
s = []

#positions of dancers
red = []
blue = []

# board with locations of dancers/stars
board = [[]]


def parse_input(filename):
	global red
	global blue

	fh = open(filename)
	file_contents = fh.readlines()
	
	adding_red = True
	
	for line in file_contents:
		fields = []
		line = line.rstrip('\r\n')

		if line == "Red dancer positions (start at 0)":
			continue
		
		if line == "Blue dancer positions (start at 0)":
			adding_red = False
			continue
		if line == "    ":
			continue

		fields = line.split(' ')

		if adding_red:
			red.append([int(fields[0]), int(fields[1])])
		else:
			blue.append([int(fields[0]), int(fields[1])])

def setup_server(port):
	global s

	s = Server.Server('', port)
	s.establishConnection()

def setup_board(size):
	global board
	
	board = [['.' for i in range(size)] for j in range(size)]
	for r in red:
		board[r[0]][r[1]] = 'R'
	for b in blue:
		board[b[0]][b[1]] = 'B'


def is_invalid_star(point):

	if point[0] < 0 or point[0] >= len(board) or point[1] < 0 or point[1] >= len(board):
		return False
		
	if board[point[0]][point[1]] == 'S':
		return True

	return False

# place stars based on spoiler input
# returns boolean if placement is allowed
def update_stars(stars):
	
	star = stars.split()
	star_count = 0
	star_locations = []
	if len(star) > 2*int(sys.argv[4]) or len(star)%2 == 1:
		return False
	i = 0
	while i < len(star):
		if int(star[i]) < 0 or int(star[i]) >= len(board) or int(star[i+1]) < 0 or int(star[i+1]) >= len(board):
			print "Ignoring star at {} {}".format(star[0], star[1])
		elif board[int(star[i])][int(star[i+1])] != '.':
			print "Ignoring star at {} {} -> {}".format(star[i], star[i+1], board[int(star[i])][int(star[i+1])])
		else:
			board[int(star[i])][int(star[i+1])] = 'S'
			star_count += 1
			star_locations.append([int(star[i]), int(star[i+1])])
		i += 2
	
	if star_count > int(sys.argv[4]):
		print "Added too many stars"
		return False

	# check for nearby stars ( <=3 is not ok, >= 4 is ok)
	for location in star_locations:
		for i in range(location[0], location[0]+1):
			if is_invalid_star([i, location[1]-3]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]-1, location[0]+2):
			if is_invalid_star([i, location[1]-2]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]-2, location[0]+3):
			if is_invalid_star([i, location[1]-1]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]-3, location[0]):
			if is_invalid_star([i, location[1]]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]+1, location[0]+4):
			if is_invalid_star([i, location[1]]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]-2, location[0]+3):
			if is_invalid_star([i, location[1]+1]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0]-1, location[0]+2):
			if is_invalid_star([i, location[1]+2]):
				print "Star", location[0], location[1], " too close to another star"
				return False
		for i in range(location[0], location[0]+1):
			if is_invalid_star([i, location[1]+3]):
				print "Star", location[0], location[1], " too close to another star"
				return False
	
	return True

# helper for updating dancer positions
def is_valid_dancer_move(start, end):
	if end[0] < 0 or end[0] >= len(board):
		return False
	if end[1] < 0 or end[1] >= len(board):
		return False
	if (start[0] == end[0] and (abs(end[1] - start[1]) == 1)) or (start[1] == end[1] and (abs(end[0] - start[0]) == 1)):
		return True
	if start[0] == end[0] and start[1] == end[1]:
		return True
	return False
			
# update position of dancers based on choreographer
def update_dancers(moves):
	global board
	global red
	global blue

	m = moves.split()
	new_board = copy.deepcopy(board)
	i = 0
	num_dancers = len(red)
	while i < len(m):
		start = [int(m[i]), int(m[i+1])]
		end = [int(m[i+2]), int(m[i+3])]
		if not is_valid_dancer_move(start, end):
			return False
		if board[start[0]][start[1]] == 'R':
			if board[end[0]][end[1]] != 'S':
				new_board[start[0]][start[1]] = '.'
				new_board[end[0]][end[1]] = 'R'
				index = red.index([start[0], start[1]])
				red[index] = [end[0], end[1]]
			else:
				return False
		elif board[start[0]][start[1]] == 'B':
			if board[end[0]][end[1]] != 'S':
				new_board[start[0]][start[1]] = '.'
				new_board[end[0]][end[1]] = 'B'
				index = blue.index([start[0], start[1]])
				blue[index] = [end[0], end[1]]
			else:
				return False
		else:
			return False
		i += 4

	# check if new_board has same number of dancers
	# such that multiple ones dont go to same spot, while allowing for swapping of dancers
	red_count = 0
	blue_count = 0
	for i in range(len(new_board)):
		red_count += new_board[i].count('R')
		blue_count += new_board[i].count('B')
	if red_count != num_dancers or blue_count != num_dancers:
		return False

	board = copy.deepcopy(new_board)
	
	return True

def get_nearby(point, dancer):

	nearby = []

	# check top
	if (point[1] < len(board)-1) and board[point[0]][point[1]-1] == dancer:
		nearby.append([point[0], point[1]-1])

	# check left
	if point[0] > 0 and board[point[0]-1][point[1]] == dancer:
		nearby.append([point[0]-1, point[1]])

	# check right
	if (point[0] < len(board)-1) and board[point[0]+1][point[1]] == dancer:
		nearby.append([point[0]+1, point[1]])

	# check bottom
	if point[1] > 0 and board[point[0]][point[1]-1] == dancer:
		nearby.append([point[0], point[1]+1])
	
	return nearby


def game_finished(board, red, blue):

	if len(red) == 0 and len(blue) == 0:
		return True

	for r in red:
		nearby_blues = get_nearby(r, 'B')
		for nearby_blue in nearby_blues:
			new_red = copy.deepcopy(red)
			new_red.remove(r)
			new_blue = copy.deepcopy(blue)
			new_blue.remove(nearby_blue)
			new_board = copy.deepcopy(board)
			new_board[r[0]][r[1]] = '.'
			new_board[nearby_blue[0]][nearby_blue[1]] = '.'

			if game_finished(new_board, new_red, new_blue):
				return True
		return False
	return True



def print_board():
	for r in board:
		for c in r:
			print c,
		print ""
	
	
def run_game():
	
	s.send("^", 0)
	start_time = time.time()
	stars = s.receive(0)
	s.send("$", 0)
	if time.time() - start_time > 120:
		s.send("$", 1)
		print "Spoiler took longer than 2 minutes, Choreographer wins"
		return
	if not update_stars(stars):
		s.send("$", 1)
		print "Invalid placement of stars, Choreographer wins"
		return

	first_move = True
	time_remaining = 120
	num_moves = 0
	while 1:
		if first_move:
			stars += "#"
			s.send(stars, 1)
			print "sent star locations"
			first_move = False
		else:
			s.send("#", 1)
		start = time.time()
		
		# make sure all data is gathered, check for '$'
		c_moves = s.receive(1)
		
		time_taken = time.time() - start
		time_remaining -= time_taken
		if time_remaining < 0.0:
			s.send("$", 1)
			print "Choreographer took longer than 2 minutes, Choreographer loses"
			return
		if not update_dancers(c_moves):
			s.send("$", 1)
			print "Invalid placement of dancers, Choreographer loses"
			return
		if len(sys.argv) > 5:
			if sys.argv[5]:
				print_board()
				time.sleep(1)
		num_moves += 1
		if game_finished(board, red, blue):
			s.send("$", 1)
			print "Choreographer finished with {} steps".format(num_moves) 
			break
		else:
			print "Remaining time:", time_remaining


if len(sys.argv) < 5:
	print "python game.py <string:dancer_locations> <int:port_number> <int:board_size> <int:number_of_stars> [bool:print_board]"
	exit()	

parse_input(sys.argv[1])
setup_server(int(sys.argv[2]))
setup_board(int(sys.argv[3]))
run_game()