require 'set'
N, M = gets().chomp().split.map(&:to_i)

unheard = Set.new
unseen = Set.new

N.times{ unheard.add(gets().chomp) }
M.times{ unseen.add(gets().chomp) }
ans = unheard & unseen
puts ans.size
puts ans.to_a.sort