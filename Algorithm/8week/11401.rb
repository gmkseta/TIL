n,k = gets.split.map(&:to_i)

MOD=1_000_000_007

def pow(x,y)
  ans = 1
  while y > 0
    ans = ans*x%MOD if y&1 == 1
    y = y/2
    x = x * x % MOD
  end
  ans
end


#n!
fac_n = 1;
(1..n).each{|i| fac_n = (fac_n * i) % MOD }
#k!
fac_k = 1
(1..k).each{|i| fac_k = (fac_k * i) % MOD }
# k-(n-k)!
(1..n-k).each{|i| fac_k = (fac_k * i) % MOD }
#페르마의 소정리에 의해서 (n!/((n-k)!k!)) % MOD = (n!/(n-k)!) % MOD * ((k!)^(MOD - 2)) % MOD를 만족함.
p (fac_n*pow(fac_k, MOD-2))%MOD


