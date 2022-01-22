N = gets.to_i

x_points = []
y_points = []

N.times do
  x, y = gets.chomp.split.map(&:to_i)
  x_points << x
  y_points << y
end

def distance(points, from)
  result = 0
  points.each do |point|
    result += (from - point).abs
  end
  result
end

def ternary_serach(points)
  low = -1_000_000
  high = 1_000_000
  while low + 3 < high
    left = (2 * low + high) / 3
    right = (low + 2 * high) / 3
    if distance(points, left) > distance(points, right)
      low = left
    else
      high = right
    end
  end
  result = Float::INFINITY
  (low..high).each do |i|
    result = [result, distance(points, i)].min
  end
  result
end

p ternary_serach(x_points) + ternary_serach(y_points)
