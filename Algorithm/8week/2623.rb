
N, M = gets.chomp.split.map(&:to_i)

indegree = [0]*(N+1)
graph = (N+1).times.map{[]}
M.times do |i|
  list = gets.chomp.split.map(&:to_i)
  (1...list[0]).each do |j|
    graph[list[j]].push(list[j+1])
    indegree[list[j+1]] += 1
  end
end

queue = []
ans = []
(1..N).each do |i|
  queue.push(i) if indegree[i] == 0
end

while not queue.empty?
  node = queue.shift
  ans.push(node)
  graph[node].each do |i|
    indegree[i] -= 1
    queue.push(i) if indegree[i] == 0
  end
end

if ans.size == N
  puts ans
else
  puts '0'
end