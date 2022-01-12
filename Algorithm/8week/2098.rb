def tsp()
  def find_path(last, visited)

    if visited == VISITED_ALL
      return (DIST[last][0] or INF)
    end

    return @cache[last][visited] if @cache[last][visited]
    tmp = INF
    N.times do |city|
      if (visited & (1 << city) == 0) and (DIST[last][city] != 0)
        tmp_cost = find_path(city, visited | (1 << city))
        next if tmp_cost.zero?
        tmp = [tmp, tmp_cost + DIST[last][city]].min
      end
    end
    @cache[last][visited] = tmp
  end
  return find_path(0, 1<<0)
end

N = gets.chomp.to_i
@cache = (1..N).map{ [nil] * (1<<N) }

VISITED_ALL = ( 1<<N ) - 1
INF = Float::INFINITY
DIST = (0..N-1).map{ gets.chomp.split.map(&:to_i) }
puts tsp()


