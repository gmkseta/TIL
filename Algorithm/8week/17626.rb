n = gets.chomp.to_i
dp = [0, 1]

(2..n+1).each do |i|
  min_value = Float::INFINITY

  j = 1
  while j**2 <= i

    min_value = [min_value, dp[i - j**2]].min
    j += 1
  end
  dp << min_value + 1

end
p dp
