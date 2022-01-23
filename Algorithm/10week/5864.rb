# frozen_string_literal: true

# N, A, B = gets.chomp.split.map(&:to_i)
#
# cows = Array.new(N) { gets.chomp.to_i }
#
# cows.sort!
# dp = [0] * (N)
# dp[0] = A
# (1...N).each do |i|
#   dp[i] = A + dp[i - 1]
#   acc = A
#   (i).downto(1) do |j|
#     acc += (cows[j] - cows[j - 1]).to_f / 2 * B
#     dp[i] = [dp[i], acc].min
#   end
# end
#
# p dp[N - 1].round(1)
#
#
#

# frozen_string_literal: true

N, A, B = gets.chomp.split.map(&:to_i)

COWS = Array.new(N) { gets.chomp.to_i }.sort

@dp = [0] * N
@dp[0] = A
@visited = [false] * N

def solution(i)
  return 0 if i >= N
  return @dp[i] if @visited[i]

  @visited[i] = true
  ans = 1000.0 * 1000 * 1000 * 1000
  (i...N).each do |j|
    ans = [ans, A + B * (COWS[j] - COWS[i]) / 2.0 + solution(j + 1)].min
  end
  @dp[i] = ans
end

ans = solution(0)
if (ans - ans.round).abs < 0.001
  puts ans.round
else
  puts ans
end