
N = gets.chomp.to_i

MAP = N.times.map{ gets.chomp.split("").map(&:to_i)}

DIRECTION = [[1,0], [0,1], [-1,0], [0,-1]]


def solution()
  ans = []
  visited = N.times.map{ [0]*N }
  MAP.each_with_index do |row, i|
    row.each_with_index do |col, j|
      if col == 1 and visited[i][j].zero?
        need_visit = [[i,j]]
        counter = 0
        until need_visit.empty?
          x, y = need_visit.shift
          if visited[x][y] == 1
            next
          else
            counter+=1
          end
          visited[x][y] = 1
          DIRECTION.each do |dx, dy|
            nx, ny = x+dx, y+dy
            if nx.between?(0, N-1) and ny.between?(0, N-1) and MAP[nx][ny] == 1 and visited[nx][ny].zero?
              need_visit << [nx, ny]
            end
          end
        end
        ans << counter
      end
    end
  end
  [ans.size, *ans.sort]
end

puts solution()
