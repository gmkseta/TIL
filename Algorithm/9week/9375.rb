
T = gets.chomp.to_i

T.times do
  n = gets.chomp.to_i
  closet = {}
  ans = 1
  n.times do
    wear, type = gets.chomp.split
    if closet[type].nil?
      closet[type] = 1
    else
      closet[type] += 1
    end
  end
  closet.each do |key, value|
    ans *= (value+1)
  end
  puts ans-1
end