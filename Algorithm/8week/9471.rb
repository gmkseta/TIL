T = gets.chomp.to_i
def fisano(m)
  fibo = [0, 1]
  (m**2-1).times do |i|
    fibo[0], fibo[1] = fibo[1], (fibo[0] + fibo[1])%m
    if fibo[0] == 0 && fibo[1] == 1
      return i+1
    end
  end
  fibo[1]
end
T.times do
  n, m = gets.chomp.split.map(&:to_i)
  puts "#{n} #{fisano(m)}"
end
