N = gets.to_i

COSTS = Array.new(N) { gets.split.map(&:to_i) }

dp = Array.new(N) { [0] * 3 }
dp[0][0] = COSTS[0][0]
dp[0][1] = COSTS[0][1]
dp[0][2] = COSTS[0][2]
(1...N).each do |i|
  3.times do |j|
    dp[i][j] = [dp[i - 1][(j + 1) % 3] + COSTS[i][j], dp[i - 1][(j + 2) % 3] + COSTS[i][j]].min
  end
end

p dp[-1].min