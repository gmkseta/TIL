@n,@m = gets().split().map(&:to_i)

@edges = @m.times.map{gets().split().map(&:to_i)}



@parent = {}
@rank = {}


def find node
  if @parent[node] != node
    @parent[node] = find(@parent[node])
  end
  @parent[node]
end

def union node1, node2
  root1 = find(node1)
  root2 = find(node2)
  if root1 != root2
    if @rank[root1] > @rank[root2]
      @parent[root2] = root1
    else
      @parent[root1] = root2
      if @rank[root1] == @rank[root2]
        @rank[root2] += 1
      end
    end
  end
end

def make_set(node)
  @parent[node] = node
  @rank[node] = 0
end

def kruskal
  @n.times{|i| make_set(i)}
  @edges.each_with_index do |edge, idx|
    if find(edge[0]) != find(edge[1])
      union(edge[0],edge[1])
    else
      puts idx+1
      return
    end
  end
  puts 0
end

kruskal()