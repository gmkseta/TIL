n = gets.chomp.to_i
dp = [0]*12

dp[1] = 1 # 1
dp[2] = 2 #  1 1, 2
dp[3] = 4 #  1 1 1, 1 2, 2 1, 3
(4..11).each do |i|
  dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
end

ans = []
n.times do
  ans << dp[gets.chomp.to_i]
end
puts ans
