require 'set'
N, M = gets.chomp.split.map(&:to_i)

BOARD = N.times.map { gets.chomp.split('') }

@visited = [0]*N*M

DIRECTION = {
  "D": [0, 1],
  "U": [0, -1],
  "L": [-1, 0],
  "R": [1, 0]
}
@ans = 0
x, y = 0, 0
layer = 1
def bfs(x,y,layer)
  queue = [[x,y]]
  while not queue.empty?
    x,y = queue.shift
    if @visited[y*M+x].zero?
      @visited[y*M+x] = layer
      direction = BOARD[y][x]
      dx, dy = DIRECTION[direction.to_sym]
      x += dx
      y += dy
      queue << [x,y]
    else
      @ans += 1 if @visited[y*M+x] == layer
    end
  end
end

(N*M).times do |i|
  if @visited[i].zero?
    x = i % M
    y = i / M
    bfs(x, y, layer)
    layer+=1
  end
end

@ans += 1 if @visited[y*M+x] == layer

p @ans