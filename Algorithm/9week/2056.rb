
N = gets.chomp.to_i

graph = Array.new(N+1) { [] }
indegree = [0]*(N+1)
costs = [0]*(N+1)
ans = [0]*(N+1)
(1..N).each do |i|
  cost, pre_cnt, *pre_works = gets.chomp.split.map(&:to_i)
  costs[i] = cost
  pre_cnt.times do |j|
    graph[pre_works[j]].push(i)
    indegree[i] += 1
  end
end

queue = []
indegree[1..].each_with_index do |indeg, i|
  if indeg == 0
    queue.push(i+1)
    ans[i+1] = costs[i+1]
  end
end

while not queue.empty?
  cur = queue.shift
  graph[cur].each do |next_|
    indegree[next_] -= 1
    ans[next_] = [ans[next_], ans[cur] + costs[next_]].max
    queue.push(next_) if indegree[next_] == 0
  end

end

p ans[1..].max


