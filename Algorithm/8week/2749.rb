n = gets.chomp.to_i

# n > 2라면, k(10n) = 15×10(n-1)
fibo = [0, 1]
while n >= 1500000
  n%=1500000
end

(n-1).times do
  fibo[0], fibo[1] = fibo[1], (fibo[0] + fibo[1])%1_000_000
end
if n.zero?
  puts 0
else
  puts fibo[1]
end