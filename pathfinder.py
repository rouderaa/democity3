import random


def generate_path_grid(grid, start, end, grid_size=(20, 20), min_straight_before_turn=2):
    """
    Generates a 2D grid with a random path from start to end coordinates.

    Each cell in the grid is an integer representing a path component:
    - 0: Empty space
    - 1: Straight path
    - 2: Left turn
    - 3: Right turn

    Args:
        start (tuple): A tuple (row, col) for the starting position.
        end (tuple): A tuple (row, col) for the ending position.
        grid_size (tuple): A tuple (rows, cols) for the dimensions of the grid.
        min_straight_before_turn (int): The minimum number of straight steps
                                        required before a turn is allowed.
    Returns:
        list: A 2D list of integers representing the grid and the path.
    """
    rows, cols = grid_size
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and
            0 <= end[0] < rows and 0 <= end[1] < cols):
        raise ValueError("Start or end coordinates are outside the specified grid size.")

    # --- 1. Generate the path as a list of coordinates ---
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    path = [start]
    current_pos = start

    dr, dc = end[0] - start[0], end[1] - start[1]
    if abs(dr) > abs(dc):
        current_dir = (1 if dr > 0 else -1, 0)
    else:
        current_dir = (0, 1 if dc > 0 else -1) if dc != 0 else (1, 0)

    straight_steps_count = 1

    while current_pos != end:
        prev_dir = current_dir

        # Determine possible next directions based on rules
        if straight_steps_count < min_straight_before_turn:
            possible_dirs = [current_dir]
            weights = [1.0]
        else:
            current_dir_index = directions.index(current_dir)
            left_dir = directions[(current_dir_index - 1 + 4) % 4]
            right_dir = directions[(current_dir_index + 1) % 4]
            possible_dirs = [left_dir, current_dir, right_dir]
            weights = [0.2, 0.6, 0.2]

            dist_to_end = abs(end[0] - current_pos[0]) + abs(end[1] - current_pos[1])
            for i, (dr, dc) in enumerate(possible_dirs):
                next_pos_check = (current_pos[0] + dr, current_pos[1] + dc)
                if not (0 <= next_pos_check[0] < rows and 0 <= next_pos_check[1] < cols):
                    weights[i] = 0
                    continue
                new_dist = abs(end[0] - next_pos_check[0]) + abs(end[1] - next_pos_check[1])
                if new_dist < dist_to_end:
                    weights[i] += 0.5

        # --- CORRECTED LOGIC: Try available moves until a valid one is found ---
        valid_move_found = False
        while sum(weights) > 0:
            chosen_dir = random.choices(possible_dirs, weights=weights, k=1)[0]
            next_pos = (current_pos[0] + chosen_dir[0], current_pos[1] + chosen_dir[1])

            # A move is valid if it doesn't go to an already visited cell
            if next_pos not in path:
                valid_move_found = True
                current_dir = chosen_dir
                current_pos = next_pos
                path.append(current_pos)

                if current_dir == prev_dir:
                    straight_steps_count += 1
                else:
                    straight_steps_count = 1
                break  # Exit the inner 'while' and continue to the next path step
            else:
                # Invalidate this choice and try again in the next inner loop
                idx_to_remove = possible_dirs.index(chosen_dir)
                weights[idx_to_remove] = 0

        if not valid_move_found:
            print("Warning: Path generation got stuck and could not find a valid next step.")
            break  # Exit the main 'while' loop

    # --- 2. Populate the grid based on the generated path ---
    if not path: return grid

    def get_direction(p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1])

    grid[start[0]][start[1]] = 1
    if end in path: grid[end[0]][end[1]] = 1
    for i in range(1, len(path) - 1):
        dir_in, dir_out = get_direction(path[i - 1], path[i]), get_direction(path[i], path[i + 1])
        r, c = path[i]
        if dir_in == dir_out:
            grid[r][c] = 1
        else:
            cross_product = dir_in[1] * dir_out[0] - dir_in[0] * dir_out[1]
            grid[r][c] = 3 if cross_product > 0 else 2

    return grid


def print_grid_uppercase(grid):
    """Helper function to print the grid with an uppercase 'X' for the path."""
    print("-" * (len(grid[0]) * 2 + 3))
    for row in grid:
        line = "| "
        for cell in row:
            if cell == 0:
                line += ". "
            else:
                line += "X "
        line += "|"
        print(line)
    print("-" * (len(grid[0]) * 2 + 3))


# --- Example Usage ---
if __name__ == '__main__':
    GRID_DIMENSIONS = (15, 30)
    START_POS = (7, 1)
    END_POS = (7, 28)

    rows, cols = GRID_DIMENSIONS
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    YRANGE = [1, 4, 10]
    for y in YRANGE:
        START_POS=(y, 1)
        END_POS=(y, 28)
        path_grid = generate_path_grid(
            grid,
            start=START_POS,
            end=END_POS,
            grid_size=GRID_DIMENSIONS,
            min_straight_before_turn=4
        )
    print_grid_uppercase(path_grid)