
N = gets.to_i

p1, p2 = gets.chomp.split.map(&:to_i)

m = gets.to_i

graph = Hash.new{|h, k| h[k] = [] }


m.times.map do
  x, y = gets.chomp.split.map(&:to_i)
  graph[x].append(y)
  graph[y].append(x)
end

def solution(p1,p2, graph)
  need_visited = [p1]
  visited = Array.new(N+1, 0)
  until need_visited.empty?
    node = need_visited.shift
    if node == p2
      return visited[node]
    end
    graph[node].each do |next_node|
      if visited[next_node] == 0
        need_visited.append(next_node)
        visited[next_node] = visited[node] + 1
      end
    end
  end
  -1
end

p solution(p1, p2, graph)



