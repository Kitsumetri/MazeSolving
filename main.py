import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class WavePoint(Point):
    dist_value: int


class GenerateMaze:

    @staticmethod
    def get_puzzle_in_matrix_from_input() -> tuple:

        maze = []
        start_point = Point(x=-1, y=-1)
        finish_point = Point(x=-1, y=-1)

        with open("maze_input.txt", 'r') as file:
            lines = [line.replace('\n', '') for line in file.readlines()]
            file.close()

        for i in range(len(lines)):
            row_array = []
            for j in range(len(lines[i])):
                match lines[i][j]:
                    case '#':
                        row_array.append(0)
                    case 'S':
                        start_point.x = i
                        start_point.y = j
                        row_array.append(3)
                    case 'F':
                        finish_point.x = i
                        finish_point.y = j
                        row_array.append(2)
                    case ' ':
                        row_array.append(1)
            maze.append(row_array)

        return maze, start_point, finish_point

    @staticmethod
    def draw_maze(maze: list) -> None:
        plt.imshow(X=maze, cmap='inferno')
        plt.axis('off')
        plt.title('Maze visualization')
        plt.show()


class SolveMaze:
    move_direction = {
        'x': [-1, 0, 0, 1],
        'y': [0, -1, 1, 0]
    }

    @staticmethod
    def draw_path(path, maze):
        for point in path:
            maze[point[0]][point[1]] = 4
        GenerateMaze.draw_maze(maze)

    class Wave:

        @staticmethod
        def recreate_path(maze_map: list, start: Point, finish: Point) -> list:

            def point_is_in_maze(x: int, y: int) -> bool:
                return len(maze_map) > x >= 0 and len(maze_map[0]) > y >= 0

            def point_is_visited(visited: list, x: int, y: int) -> bool:
                return visited[x][y] > 0

            path = []
            point = WavePoint(finish.x, finish.y, maze_map[finish.x][finish.y])
            path.append((point.x, point.y))

            while True:

                for k in range(4):

                    new_x = point.x + SolveMaze.move_direction['x'][k]
                    new_y = point.y + SolveMaze.move_direction['y'][k]

                    if new_x == start.x and new_y == start.y:
                        path.append((start.x, start.y))
                        path.reverse()
                        return path

                    if point.dist_value - maze_map[new_x][new_y] == 1 \
                            and point_is_in_maze(new_x, new_y) \
                            and point_is_visited(maze_map, x=new_x, y=new_y):

                        path.append((new_x, new_y))
                        point = WavePoint(new_x, new_y, point.dist_value - 1)

        @staticmethod
        def get_path(maze: list, start: Point, finish: Point) -> list:

            from queue import Queue

            def point_is_valid_and_not_visited(mat_maze: list, visited: list, x: int, y: int) -> bool:
                return (height > x >= 0 and width > y >= 0) and mat_maze[x][y] == 1 and visited[x][y] == 0

            height, width = len(maze), len(maze[0])

            if not maze or len(maze) == 0 \
                    or maze[start.x][start.y] == 0 \
                    or maze[finish.x][finish.y] == 0:
                exit(-1)

            iterations = 0

            point_queue = Queue()
            point_queue.put(WavePoint(start.x, start.y, 1))

            visited_map = [[0 for _ in range(width)] for _ in range(height)]
            visited_map[start.x][start.y] = 1

            while not point_queue.empty():

                point = point_queue.get()

                if point.x == finish.x and point.y == finish.y:
                    print('Iterations:', iterations)
                    print('Number of movement:', point.dist_value)
                    point_queue.task_done()
                    path = SolveMaze.Wave.recreate_path(visited_map, start, finish)
                    print('Path using Lee Algorithm:\n', *path)
                    return path

                iterations += 1

                for k in range(4):

                    new_x = point.x + SolveMaze.move_direction['x'][k]
                    new_y = point.y + SolveMaze.move_direction['y'][k]

                    if point_is_valid_and_not_visited(mat_maze=maze, visited=visited_map, x=new_x, y=new_y):
                        visited_map[new_x][new_y] = point.dist_value
                        point_queue.put(WavePoint(x=new_x, y=new_y, dist_value=point.dist_value + 1))


def main() -> None:
    maze_matrix, start, finish = GenerateMaze.get_puzzle_in_matrix_from_input()

    GenerateMaze.draw_maze(maze_matrix)
    maze_matrix[start.x][start.y] = 1
    maze_matrix[finish.x][finish.y] = 1

    print(f"\nStart point: ({start.x},{start.y})\n"
          f"Finish Point ({finish.x},{finish.y})\n")

    SolveMaze.draw_path(SolveMaze.Wave.get_path(maze_matrix, start, finish), maze_matrix.copy())
    print()


if __name__ == '__main__':
    main()
