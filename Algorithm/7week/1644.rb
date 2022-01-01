
def prime_list(n)
  sieve = Array.new(n+1, true)
  sieve[0] = sieve[1] = false
  
  (2..Math.sqrt(n).ceil).each do |i|
    (i**2..n).step(i) { |j| sieve[j] = false } if sieve[i]
  end
  sieve.each_with_index.select { |x, i| x }.map { |x, i| i }
end


n = gets().to_i

arr = prime_list(n)

left = 0
right = 1

counter = 0
while left<=right do
  sum = arr[left..right].sum
  if n == sum
    counter += 1
    right+=1
  elsif n < sum
    left+=1
  else
    right+=1
  end
  break if right > arr.size-1
  
end
  
print(counter)