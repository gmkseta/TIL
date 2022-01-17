
N = gets.to_i

BOARD = N.times.map { gets.chomp.split.map(&:to_i)}

@white = 0
@blue = 0

def check(x, y, n)
  if n == 1
    BOARD[y][x]
  else
    part_result =  [check(x, y, n/2), check(x+n/2, y, n/2), check(x+n/2, y+n/2, n/2), check(x, y+n/2, n/2)]
    if part_result.all?(1) or part_result.all?(0)
      return part_result[0]
    else
      @white+= part_result.count(0)
      @blue+= part_result.count(1)
      return false
    end
  end
end

result = check(0,0,N)
if result == 1
  @blue += 1
elsif result == 0
  @white += 1
end

p @white
p @blue