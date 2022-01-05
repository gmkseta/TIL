R,C = gets.chomp.split.map(&:to_i)

@board = R.times.map{ gets.chomp.split('' )}

N = gets.chomp.to_i

sticks = gets.chomp.split.map(&:to_i)

LEFT = -1
RIGHT = 1
@dir = [[0,1], [0,-1], [-1,0], [1,0]]

def bfs(start_y,start_x)
  need_visit = [[start_y,start_x]]
  visited = [0]*(R*C)
  visited[start_y*C+start_x] = 1
  need_down = []
  min_height = Float::INFINITY
  flag = false
  while need_visit.size > 0
    y,x = need_visit.shift
    need_down.append(y*C+x)
    flag = true if y==R-1
    @dir.each do |dy, dx|
      ny = y + dy
      nx = x + dx
      if ny >= 0 && ny < R && nx >= 0 && nx < C && @board[ny][nx] == 'x' && visited[ny*C+nx] == 0
        visited[ny*C+nx] = 1
        need_visit << [ny,nx]
      end
    end
  end
  return flag, need_down
end



sticks.each_with_index do |stick, i|
  direction = i % 2 == 0 ? LEFT : RIGHT
  if direction == LEFT
    line = @board[R-stick]
  else
    line = @board[R-stick].reverse!
  end
  if removed_idx = line.find_index('x')
    line[removed_idx] = '.'
    if direction == RIGHT
      line.reverse!
      removed_idx = C-removed_idx-1
    end
    @dir.each do |dy, dx|
      ny = R-stick + dy
      nx = removed_idx + dx
      if ny >= 0 && ny < R && nx >= 0 && nx < C && @board[ny][nx] == 'x'
        flag, need_down = bfs(ny,nx)
        while not flag
          loop_need_down = need_down.clone
          need_down = []
          loop_need_down.sort.reverse.each do |idx|
            y,x = idx/C, idx%C
            @board[y][x] = '.'
            @board[y+1][x] = 'x'
            need_down.append((y+1)*C+x)
          end
          need_down.sort.reverse.each do |idx|
            y,x = idx/C, idx%C
            if @board[y+1].nil? or (
                (not need_down.include? (y+1)*C+x) and @board[y+1][x] == 'x'
              )
              flag = true

            end
          end
        end
      end
    end
  end
end
puts @board.map(&:join)




