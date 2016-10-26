# dancing_without_stars


For any questions or bugs, please email yw2336@nyu.edu.

## Running the game:

```
python game.py <string:dancer_locations> <int:port_number> <int:board_size> <int:number_of_stars> [bool:print_board]
```

The last argument is optional, allowing you to see the movements of the dancers through an ASCII representation of the board.


## Running the client:
Connect to the game server using the same port.  A sample client (for both spoiler and choreographer) has been provided.


## Spoiler
As the spoiler, wait for a message from the server containing the string "^", then send the coordinates of the stars in a string of x,y coordinates separated by spaces.

For 10 stars, this means that there will be 20 integers sent to the server.

After sending the coordinates, please close the socket on the client.  The server will also send a message of "$" signalling that the spoiler is no longer needed.

The sample spoiler creates a star at a random location, so it is possible that it creates an invalid star.


## Choreographer
As the choreographer, you will receive the locations of the stars in the same format, a list of x,y coordinates separated by spaces.  At the end of this string will be a "#", to ensure that all characters have been sent.

If the star placement is invalid, the server will instead send the choreographer a message containing "$" to signal that the game has ended.

The choreographer's moves will be sent to the server as a pair of x,y coordinates for starting position and ending position of each dancer that the choreographer wants to
move, separated by spaces.  The sample choreographer also shows the format.

This means that some can remain still by omitting the coordinates for that dancer (if towards the end of the dance).  In addition, you can also send moves so that the start and end position of a dancer is the same.  The behavior is identical.

After each move has been validated, the server will send a message of "#" to the choreographer, requesting the next set of moves.

When the game is complete (all dancers have been paired up with the other color), the server will send the choreographer a message of "$" so that the choreographer can close the socket.  The server will also show the number of steps required to finish the dance.
