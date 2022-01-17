N = gets.to_i


graph = (N+1).times.map{[]}
costs = Array.new(N+1,0)
full_costs = Array.new(N+1,0)
indegree = Array.new(N+1,0)

N.times do |i|
  cost, *need_built = gets.split.map(&:to_i)[...-1]
  costs[i+1] = cost
  need_built.each do |need|
    graph[need] << i+1
    indegree[i+1] += 1
  end
end


queue = []
indegree.each_with_index do |indegree, i|
  if indegree == 0
    queue << i
    full_costs[i] = costs[i]
  end
end

while not queue.empty?
  node = queue.shift
  graph[node].each do |next_node|
    indegree[next_node] -= 1
    full_costs[next_node] = [full_costs[node] + costs[next_node],full_costs[next_node]].max
    if indegree[next_node] == 0
      queue << next_node
    end
  end
end

puts full_costs[1..]
