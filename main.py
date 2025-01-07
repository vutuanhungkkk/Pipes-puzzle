from puzzle import PipesPuzzle
from ui import PuzzleInterface

if __name__ == "__main__":

  solve_choice = input("Solve by DFS or BestFirstSearch? (1: DFS, 2: A*): ")

  puzzle_pipes = PipesPuzzle()
  puzzle_pipes.solve(solve_choice)
  puzzle_interface = PuzzleInterface(puzzle_pipes)
  puzzle_interface.running()
  #Hiển thị biểu đồ
  if len(puzzle_pipes.dataForPlot) != 0:
    t = input("Shall we show statistics about heuristic searching ?? (Y: Yes, other: No): ")
    if t == 'Y' or t =='y':
      puzzle_pipes.simulatePlot()
