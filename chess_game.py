def main():
    white_figure, white_position = get_white_figure()
    black_figures = get_black_figures(white_position)  # Pass white_figure to the function  
    captures = white_captures_black(white_figure, white_position, black_figures)

    if captures:
        print(f"White {white_figure} can capture black figures in these coordinates: {captures}")
    else:
        print(f"No black pieces can be captured by white {white_figure} :( ")

def get_white_figure():
    """asking for white figure (rook or king) and its coordinates"""

    while True:
        white_input = input("Choose white figure (rook or king): ")
        if white_input not in ["rook", "king"]:
            print("Invalid figure. Please choose rook or king.")
        else:
            white_position = input(f"Enter position for the white {white_input} (e.g. a1, b8): ")
            x, y = convert_position_to_coordinates(white_position) #converting chess notation to coordinates
            if x is not None and y is not None:
                print(f"White {white_input} was successfully added to {white_position}")
                return white_input, (x, y)
            else:
                print("Invalid position. Please enter in valid format (e.g. a1, b8): ")

def get_black_figures(white_position):
    """Creates a list of already taken and unoccupied coordinates"""

    black_figures = [] 
    all_coordinates = {(x, y) for x in range(8) for y in range(8)}  # All possible coordinates in range 8x8
    all_coordinates.discard(white_position)  # eliminating white figure's position

    while True:
        black_position = input("Enter coordinates for 1-16 black figures (or 'done' to finish): ")
        if black_position == "done":
            if len(black_figures) >= 1:
                black_positions_notation = [convert_coordinates_to_position(coords) for coords in black_figures] # Convert black figures' coordinates to chess notation
                print(f"You listed black figures at: {black_positions_notation}")
                return black_figures
            else:
                print("You must add at least one black figure")           
        else:
            x, y = convert_position_to_coordinates(black_position)
            if x is not None and y is not None:
                if (x, y) in black_figures:
                    print("Position already taken by another black figure.")
                elif (x, y) not in all_coordinates:
                    print("Position is occupied by the white figure.")
                else:
                    black_figures.append((x, y))
                    all_coordinates.discard((x, y)) 
                    print(f"Black figure added at position {black_position}")

                    if len(black_figures) == 16: # Check if we have reached 16 black figures
                        print("16 black figures were added.")
                        return black_figures  # Exit after adding 16 figures
            else:
                print("Invalid position. Please enter in valid format (e.g. a1, b8): ")

def get_initial_black_positions(black_figures):
    '''Convert black figures' coordinates to chess notation'''

    return [convert_coordinates_to_position(coords) for coords in black_figures]

def convert_position_to_coordinates(position):
    '''Convert chess notation to coordinates'''

    if len(position) != 2 or position[0] not in "abcdefgh" or not position[1].isdigit(): 
        return None, None
    x = ord(position[0]) - ord('a') #Converts the letter ('a' to 'h') into a number (0 to 7). For example, 'a' becomes 0, 'b' becomes 1, and so on.
    y = 8 - int(position[1])
    if 0 <= x < 8 and 0 <= y < 8:
        return x, y
    return None, None
'''X coordinates: ord(character) function returns the Unicode (ASCII) code of the character, for example: ord('a') returns 97, so for "a", ord('a') - ord('a') = 97 - 97 = 0
   Y coordinates: as starting with white figure, the chess board top is line 8 and bottom - line 1. so in python we have to convert the numbers, for example:
    if the figure is placed at a1 (whis is at the bottom of the board), python coordinates should be (0;7)'''

def white_captures_black(white_figure, white_position, black_figures):
    '''Function determines if the white figure (rook or king) can capture any black figures based on its position.'''

    captures = []
    x, y = white_position

    if white_figure == "rook":
        captures += check_direction(black_figures, x, y, 1, 0)  # Right
        captures += check_direction(black_figures, x, y, -1, 0) # Left
        captures += check_direction(black_figures, x, y, 0, 1)  # Up
        captures += check_direction(black_figures, x, y, 0, -1) # Down
    elif white_figure == "king":
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in black_figures:
                captures.append(convert_coordinates_to_position((nx, ny)))
    return captures

def check_direction(black_figures, x, y, dx, dy):
    '''Function that helps the rook capture black figures by checking each direction until it finds a black figure or goes out of bounds'''
    nx, ny = x + dx, y + dy 
    while 0 <= nx < 8 and 0 <= ny < 8: #checking if the new position is within bounds of the board
        if (nx, ny) in black_figures: 
            return [convert_coordinates_to_position((nx, ny))] 
        nx += dx #The movement continues in the same direction until ir encounters black figure or reaches the edge of board
        ny += dy
    return []

def convert_coordinates_to_position(coords):
    '''Formula converts coordinates to chess notation'''
    x, y = coords
    return f"{chr(x + ord('a'))}{8 - y}"

main()