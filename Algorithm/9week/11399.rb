n = gets.chomp.to_i

arr = gets.chomp.split.map(&:to_i)

arr.sort!

ans = 0
time = 0
arr.each do |a|
  time+=a
  ans += time
end

p ans