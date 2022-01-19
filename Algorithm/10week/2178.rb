


N, M = gets.chomp.split.map(&:to_i)

board = N.times.map { gets.chomp.split('').map(&:to_i) }


DIRECTION = [[1, 0], [-1, 0], [0, 1], [0, -1]]
need_visited = [[0,0]]

dp = Array.new(N) { Array.new(M, Float::INFINITY) }
dp[0][0] = 1
until need_visited.empty?
  x, y = need_visited.shift
  DIRECTION.each do |dx, dy|
    nx, ny = x + dx, y + dy
    next if nx < 0 || nx >= N || ny < 0 || ny >= M
    next if board[nx][ny] == 0
    next if dp[nx][ny] <= dp[x][y] + 1
    dp[nx][ny] = dp[x][y] + 1
    need_visited << [nx, ny]
  end
end

p dp[N-1][M-1]



