


a, b = gets.chomp.split.map(&:to_i)

def counter(n)
  result = 0
  k = 0
  while 2**k <= n
    p = 2**(k+1)
    p_count = (n+1)/p
    result += p_count*(p/2)
    remain = (n+1)%p
    result += [0, remain - p/2].max
    k+=1
  end
  result
end

puts counter(b) - counter(a-1)
