
N = gets.to_i

packages = gets.split.map(&:to_i).sort!
packages.sort!
packages.prepend(0)
truck, heli = gets.split.map(&:to_i)
dp = [0]*(N+1)
(1..N).each do |i|
  dp[i] = dp[i-1] + truck*packages[i]
  acc = heli
  (i).downto(1) do |j|
    acc += (packages[(i+j+1)/2] - packages[j])*truck
    dp[i] = [dp[i], dp[j-1] + acc].min
  end
end

p dp[N]

