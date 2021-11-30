# Redis 



## Redis 기본 자료 구조

### Key Value Store

* NoSql



### Redis vs Memcached

* Redis
  * 많은 자료구조
  * Replication 
  * Cluster모드 
  * 메모리 파편화가 잘 일어남? - jmalloc을 써서.. 함 
* Memcached
  * Redis에 비해 메모리 관리 더 안정적
  * slab 테이블을 이용해서 메모리관리 자체적으로

### Redis 사용처

* 주로 Cache 저장

### 제공 자료구조

* String
* List
* Set
* Hash
* Sorted Set

기본적으로 Hash Table 

키 겹치면 선행 리스트 구조로. 특정 키에 너무 많ㅇ ㅣ들어가면 실제론 리밸런싱해서 키우니까 문제는 없지만... 특정 테이블만 늘어난다면 .. ? 문제가될수도



## String

`set <key> <value>`

`get <key>`

`mset, mget`

싱글스레드라서 처리량을 좀 줄이는게 좋음! 값도 너무 큰거 ㄴ

### List, Hash, Set, Zset

value가 !

## List

* 중간에 추가 삭제가 느리고, Head와 Tail에로만 데이터 추가, 삭제할 때 유용함 
  * O(N)이라 선형 탐색의 비용이 비싼 자료구조
* Queue 형태의 자료구조가 필요할 때 많이 사용한다.
  * SideKiq이나 Jesqueue라는 Redis 기반의 Queue들이존재

```
Lpush <key> <value>
Rpush <key> <value>
Lpop <key> <value>
Rpop <key> <value>
Lrange <key> <시작인덱스> <끝인덱스>
```



List 는 Job Queue로 많이 씀

 blpop -> 원래는 없으면 바로리턴인데, b 붙으면 새로 들어올때까지 대기

## Set

* 유일한 값들만 있는 집합을 유지하는 자료구조
  * 중복된 값 X
* 친구리스트 팔로워리스트 등을 저장하는데 사용 가능
  * 특정 그룹을 저장할 때
* Spring Security Oauth
  * access token을 이거로?

```
Sadd <key> <item>
#추가
smembers <key>
#확인
Sismember <key> <item> 
#있으면 1 없으면 0
Srem <key> <item>
#있으면 삭제
순서없음
```



## Sorted Set

* 스코어를 가지는 Set 자료구조.
* 아이템들의 랭킹을 가지는데 사용 가능함
* 스코어는 Double형태, 특정 정수값을 사용할 수 없음
* Skiplist자료구조를 사용
  * Log(N)의 검색속도를 가지는 자료구조

```
ZADD <key> <score> <item>
Value가 이미 존재하면 해당 score로 변경함
ZRANGE <key> <startIdx> <endIdx>
스코어 idx로!
zREVrange - 리버스!
ZRANGEBYSCORE key start_score end_score
괄호 들어가면 포함 X
zrangebyscore key (70 100

```



## Hash

* key 하위에 subkey를 이용해 추가적인 Hash table
* 일반적인 k/v 데이터를 특정 군에 데이터로 묶고 싶을 떄 유용함

```
Hset key subkey value
Hget key subkey
Hmset key subkey value subkey subvalue
Hmget key subkey subkey
hgetall key
# 모든 subkey value
hvals - 값만
# 모든 value
```

collection에 너무 많은 값을 넣으면 안된다.





# Redis Transaction - Multi/Exec

redis는 싱글 스레드라 명령들이 아토믹을 보장한다. 

그 아토믹을 보장ㅎ해 줄때도 여러명이 동시에 실행되길 원할때???

### Redis Transaction - 한번에 실행되는 것을 보장해주느 명령

### Multi

* Exec가 나올 떄 까지 명령을 모아 대기한다.

### Exec

* Exec 를 실행하면 Multi로 모인 명령이 순서대로 실행됨
* 다른 명령으 ㅣ수행 없이!
  * Redis는 싱글 스레드이므로 다른 명령이 이 동안에 수행되지 않는다.
  * 너무 많은 작업이 있으면 전체 Redis성능이떨어짐
* Lua스크립트를 써도 같은 보장이 가능함.

```redis
multi
set a 1
set b 2
exec
```



## redis pipeline

* redis 명령의 수행
* 응답을 기다리는 동안 Time Gap이 존재
* set a 123 -> ok 하고 오는데에 시간?

* 동기적으로 명령을 보내는 경우 응답을 기다리지 않고 명령을 미리 보내는 방식!
* Library들이 보통 명령을 보내고 응답을 기다림
* 100만개를 set하는 테스트를 하면 10배 이상 차이가남
* pipeline은 라이브러리에서 제공하는 기능이라 !
* 응답을 대기하지 않는다!
* Redis에서 제공하는 기능이 아닌 라이브러리에서 응답을 기다리는 것 때문에 느려지는것
* 라이브러리가 제공해주는 !
* Async Redis Client라면 제공할 필요가 없음