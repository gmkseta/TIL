# n = gets.to_i
# dp = (n+1).times.map{[0,0]}
# stairs = [0, *(1..n).map{ gets.to_i }]
# dp[1][0] = stairs[1]
# dp[2][0] = stairs[2] if n>1
# (2..n).each do |i|
#   dp[i][0] = stairs[i] + dp[i-2].max
#   dp[i][1] = stairs[i] + dp[i-1][0]
# end
#
# p dp[-1].max
a=b=c=0; gets.to_i.times{s=gets.to_i;a,b,c=c,a+s,[a,b].max+s};p c

