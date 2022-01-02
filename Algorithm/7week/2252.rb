@N, @M = gets().chomp().split.map(&:to_i)

@cnt_of_link = [0]*(@N+1)

@graph = (@N+1).times.map{[]}
queue = [] 

@M.times do
  a, b = gets().split.map(&:to_i)
  @cnt_of_link[b] += 1
  @graph[a].append(b)
end

(1..@N).each do |i|
  queue.append(i) if @cnt_of_link[i].zero?
end

while !queue.empty?
  v = queue.pop()
  print "#{v} "
  @graph[v].each do |next_v|
    @cnt_of_link[next_v] -= 1
    queue.append(next_v) if @cnt_of_link[next_v].zero?
  end
end
