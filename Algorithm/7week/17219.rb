N, M = gets().chomp().split.map(&:to_i)
passwords = {}
N.times do
  site, password = gets().chomp.split 
  passwords[site] = password
end

M.times do
  site = gets().chomp
  puts passwords[site]
end