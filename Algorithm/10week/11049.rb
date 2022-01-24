N = gets.to_i

dp = Array.new(N) { [Float::INFINITY] * (N) }

matrix = Array.new(N) { gets.chomp.split.map(&:to_i) }
dp[1] = matrix[0][0] * matrix[1][0] * matrix[1][1]

(2...N).each do |i|

  dp[i] = [
    dp[i - 1] + matrix[0][0] * matrix[i][0] * matrix[i][1],
    dp[i - 2] + matrix[i - 1][0] * matrix[i][0] * matrix[i][1]
  ].min
end

p dp