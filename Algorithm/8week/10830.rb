N, B = gets.split.map(&:to_i)

matrix = N.times.map{ gets.split.map(&:to_i) }

def calc_row(row, col, m1, m2)
  [m1[row], m2[col]].transpose.map{|a| a.inject(:*)%1000}.sum%1000
end

def multi(m1, m2)
  result = m1.map(&:clone)
  N.times do |i|
    tmp = m1[i].clone
    N.times do |j|
      tmp[j] = calc_row(i, j, m1, m2.transpose)
    end
    result[i] = tmp
  end
  result
end

def solution(matrix, b)
  return matrix if b == 1
  result = matrix.map(&:clone)
  while b > 0
    if b & 1 == 1
      result = multi(result, matrix)
    end
    b >>= 1
    matrix = multi(matrix, matrix)
  end
  result
end


result_matrix = solution(matrix, B-1)
puts result_matrix.map{|a| a.map().join(' ')}.join("\n")