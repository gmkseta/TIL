# 3. 대규모 서비스 설계를 위한 백엔드 에센셜

## LoadBalancer

* 요청을 여러 서버로 분배해주는 하드웨어 or 소프트웨어 장비
* 요청자는 lb 뒤의 목록은 알지 못한다.

### Software Load Balancer

* nginx / haproxy 등 
* ![image](https://user-images.githubusercontent.com/72075148/134348270-c1312663-48b4-4d92-91ad-202e38c7a648.png)

### Server Side

Caller는 LB의 주소만 알고 그 뒤의 상태는 모름 서버가 한 두 대 사라지든 말든 

* 로드밸런서를 통해 리퀘스트를 분산한다.
* 클라이언트가 서버 개별의 주소를 알 필요가 없다. - 다만 로드밸런서 주소는 알아야지
* 실제적으로 한 단계를 더 거치므로 Latency가 늘어날 수 있다. - hop
* 로드밸런서가 장애 발생하면 서비스가 더 ㄴㄴ

### Client side

* 클라이언트가 서버의 대수 및 주소를 모두 알아야한다.
* Latency 줄어들 수 있음
* 장애포인트가 줄어든다.
* 클라에서 서버 목록하고 주소를 관리해야하는 단점 - 만약 바뀌거나 추가/삭제 되면 ?

## LoadBalancer - 실습

- /the_red.git 에서
- redis / zookeeper를 설치
- java 8 or 11 
- production에서는 zookeeper를 3~5대 사용함
- chapter 2 -> loadbalancer ->
- docker build . -t gmkseta/lb_scrap
- `docker run -e ENDPOINTS=0.0.0.0:7001 -p 7001:7001 gmkseta/lb_scrap`
- `docker run -e ENDPOINTS=0.0.0.0:7002 -p 7002:7002 gmkseta/lb_scrap`

7001 / 7002로 두개 띄우고 software lb 쓰는거 예제 - 로컬에 nginx 쓰는듯..?

nginx 로컬에 말고 그냥 하고싶은데 docker-compose로 ? or docker network쓰거나?

aws - elb 에 target group에 health check를 해서, 횟수 해놔서? 뭘한다

//geoip-lb-1390122424.ap-northeast-2.elb.amazonaws.com

elb를 통해서만 접근

## 서비스 디스커버리

* DNS로 찾는다?
* 클라이언트에서는 외부 dns로 우리 서버의 주소를 알게?
* 내부 dns?에서도 ..
* 서버가 죽었을 때 DNS TTL 동안은 ( ex 1분~ ) 어쨋든 서빙안되고 

### Service Discovery

* 서비스의 주소, 포트, 프로토콜 등을 알려주는 방법

* LB는 부하를 직접적으로 나눠주는거고, Service Discovery는 어떤 서비스가 있고, 해당 서비스에 어떤 서버나 endPoints가 있는가를..
* Client side에서 예약서버가 결제서버의 주소는 어케알지?

* 설정파일?
  * 서버 주소 목록을 설정파일에 넣어두자!
  * payment_servers=10.1.0.10:10000,10.1.0.1000~
  * 서버 목록이 변경되면? 설정파일 수정 후 재배포 
* DNS?
  * DNS이용해서 동적으로 바꾸자 
  * DNS질의로 서버 목록을 갖고오자
  * DNS는 누가 업데이트? DNS TTL문제는?
* LB 못쓴다면?
  * 홉을 원하지 않거나
  * 비싸서? - 돈이없다면

그래서 Service Discovery가 필요하다..?

* 어떤 서비스가 있는지
* 접속 방법
* 추가 / 제거가 있을 떄 알려주는거
* ![image](https://user-images.githubusercontent.com/72075148/134760494-f6eb05a3-3443-47eb-92d3-2788f5e9390f.png)
* health check를 한다 - 
* 서버 추가 하는 부분도 health check생기면 인듯 결제서버쪽에서 service discovery쪽으로 보내는거인듯 lb랑 반대
* 

### Coordinator

* 서비스 가용성이 높다
  * 일반적으로 3대 이상으로 동작
  * 데이터 동기화가 이루어 진다. 절반이상 장애 안나면 서비스 유지 가능
* 보통 특정 값을 저장할 수 있는 대시보드 역할
  * cluster membership
  * 변경되는 값에 대한 Noti
* 노드의 순서를 보장
  * Leader election

### Cluster Membership

* API 추가/변경
* Database Master장비 추/변
* Cache장비 추/변

* 목록을 추가/배포해야 했는데 - 목록만 추가하면 알아서 동작 / 장비만 추가하면 .. 

![image](https://user-images.githubusercontent.com/72075148/134760685-fbe5aaba-66f0-488d-81bb-1966ed02f21d.png)

### Leader Election

* HealthChecker를 만든다 치면 - 어케 보장하냐 맞는걸
* HealthChecker를 체크하는 HealthChecker??
* HealthChecker를 여러개 .. 만들자
* 장애나면 알람이 몇개나 갈까.. 헉
* 여러대지만 한대만 동작하면 좋겠다
* ![image](https://user-images.githubusercontent.com/72075148/134761002-ad763bf2-1622-43c4-b82c-e0b8ddd58fc3.png)

* 여러대 서버중에 한대만 그 일을 하게 하고싶을 떄 - or 분산 Lock
* 이런 종류의 모니터링은 ?? aws lambda로 쉽게 구현한다?
* leader선정 - 
  * dns를 이용해서 동적으로 바꾸자
  * zookepper? - 정렬해서 맨 위
  * etcd - 특정 키를 쓰는데 성공한 서버가 리더 되도록하자

### Watcher

* 설정을 바꿔서 재 배포하는건 힘들다 - 동적으로, 각 서버들에게 해당값을 바꾸라고? 통지한다.

* redis, pub/sub 등..

### Feature Flag

* 값이 바뀌었을 때 각 서버에 ..  
* 새로운 기능을 출시/배포 했을 때 마치 이 플래그로 기능 동작 여부놓는거처럼
* 재배포가 힘들면- 오래걸리면 이게 더 낫지.- 롤백 /재배포 하는거 시간 걸려서?
* 이게 서버의 응답을 바꾸는거면 클라쪽에서 에러날수도있고
* 클라이언트도..

## Service Discovery 실습

- redis / db에 lb못붙이는건 당연히 같은 데이터 갖고있는게 아닐 가능성잉 있자나
- zookeeper
  - 자체 service 는 그냥 노드 health check해서 목록 .. 구현 혹은 라이브러리로 코드에 추가하면 되는데
  - redis / dbms는 외부에서 모니터링 하고 zookeeper에 등록하는 형태의 agent가 필요
    - agent가 죽거나 하면 장애로 인지 ..할수도
  - Heartbeat 체크 30초 단위라 .. DNS TTL하고 동일한거 아닌가? 결국..

### chapter2 - service_discovery

./zkserver.sh start

callee start.sh 하면 - 여기 코드에 zookeeper등록하는ㄱ ㅔ있음

```
ZK_SCRAP_PATH = "/the_red/services/scrap/nodes"
```

round robind으로 caller에서 나눠서 보내나봄

근데 그래서 뭐쓰라는거지 쩝

Health Check를 DB로 하고있다.

## Circuit Breaker

![image](https://user-images.githubusercontent.com/72075148/134761730-b2645784-80b6-494d-aa35-a9368e9df134.png)

* 만약 timeout이 300ms
* 평소에 20ms 처리
* 1스레드는 1초에 50개 처리
* 장애가 나면 1초에 3개밖에 처리못함

### 장애의 연쇄 반응

* A서비스가 장애가 나면 여기에 의존하는 B서비스도 점점 느려진다.
* 결국 B에 의존하는 CDE도 결국 느려진다..

### 필수적인 API, 필수적이지 않은 API

* 서비스 기준에 따라 다 달라진다..
* 커머스에서 상품 리스트는 중요하지?
* 일부 카테고리만 안보이는거면 그냥 넘어가도 되지않나..?
* 추천시스템이나 리뷰같은거는...



### Fast Fail Back

* 정상적이지 않으면 timeout등으로 처리량이 줄고 부하가 늘어날 수 있다.
* 추천 서비스 장애시 기본 순서로 그냥 정보 보여준다.

![image](https://user-images.githubusercontent.com/72075148/134761900-aec2abde-a697-4d00-bb10-8bb8c3e9614b.png)

![image](https://user-images.githubusercontent.com/72075148/134761912-6312fd76-042d-44ee-819b-a94c9cc40064.png)



threshold가 있어서 - 3번? 뭐 이런식으로 연속으로 그 이상 실패하면 open으로 바뀐다.

open 상태의 reset timeout이 되면 한번더 시도한다.

api server가 콜 하면 circuit breacker가

![image](https://user-images.githubusercontent.com/72075148/134762006-dde32405-b45d-433c-a695-70a63edaf2b5.png)

바로 리턴하므로 300ms 안걸림!

기준 정해야함

* 몇번 실패하면? fail back이 동작하나??

* 서비스가 살아있는지 확인은 어떤 방법?? health check.. Interval?? - 민감도가 달라질 수 있으니까...
* aiobreaker 
* pybreaker

* hystrix
* Resilience4j



### 실습

* circuit_breaker - callee 키고

* caller 에 app.ini 에 주소변경 - 아니면 주키퍼의 서비스 디스커버리 사용도 가능

  * [scrap]

    endpoint=127.0.0.1:7001 ( callee 주소로 )

* 바인드 된 주소로만 잘 

* calleed에 5초 timeout으로 한다면



## 

## Failover

Active한 시스템에 장애가 발생했을 때 StandBy 서버가 Active로 전환해서 서비스가 계속 운영되게 하는 것을 말한다

서비스 가용성을 제공하기 위해서 사용



* 간단한 시나리오
  * api서버가 장애가 일어나면? - secondary- 직접 바꿔서 배포한다...
  * 모니터링하다가 장애가 발생한 시점에? 설정하고.. 담당자가 휴가거나 잠들어있거나 하면...
  * lb로 하것지 뭐 
  * 자동화 된 방식의 Failober 방식이 필요함

### Coordinator를 이용한 방식

* (Service Discovery 형태)
* 장애 나면 Failover 요청을 주고, 바뀐다?

기존 lb랑 다른 그게 뭐지??

* 만약 외부에 서비스를 제공하는 방식이면?? 못씀 그걸 열어두면 너무 위험함
* 그 코디네이터 엔드포인트 공개해야해서 그런듯

### VIP ( Virtual IP) 를 이용하는 방법

* elb바꿔주는 방식인듯
* 장비의 이전 등에서도 씀
* 만약 connection을 계속 맺고있으면..? 
  * 끊어주는 작업도 들어감!
  * 클라에서 접속이 끊겼을 때 재접속하는 코드가 필요함

### DNS를 이용하는 방법

* DNS TTL이 문제
* 외부의 DNS냐 내부냐에 따라 달라짐
  * 외부는 캐싱타임이 길다? - 자주 접속이 있으니까
  * 내부는 짧아도된다? - 10 - 30 - 60초 등

그냥 클라에서 요청을 Ip / domain으로 하냐으 ㅣ차이인가.?

Proxy종류에 따라서 dns cashing을 영구히 하는 애들이 있다.? 외부의 서비스를 머시기하는경우는 .. .

AWS에서는 기본으로 DNS기반의 failover를 쓴다 \

ELB, ElasticCache에서도 .. Rds에서도..

기본적으로 multi-az사용

결국 서비스의 복구비용 - 운영비용 -> 복구비용에는 유저가 떨어져 나가는 것도 포함

거의 DNS를 표준처럼 쓴다? route53에서 ..

### 실습

redis를 서로 다른 conf/ port로 켜서 failover 실습

그냥 주키퍼 써서 하는듯!

## Replication

* Primary데이터를 Secondary에서 복사해서 데이터의 Sync를 맞추는 작업
* 전통적인 RDBMS에서 이런 형태로 지원
* NoSQL도
* 안되면 장애시 데이터 유실이 많이 발생한다
* Replication 해도 보장되는건 아님
  * P -> S 에 전달 하는데 S에서 반영 X인데 P에서 끝내보통
  * raw데이터로 ..

### Active StandBy 패턴

* Active

  Primary는 읽기 쓰기,

* StandBy

  Replcation으로 받다가 장애시 승격됨 

  * autoincrement 머시기인가? 맞춰주고 되는거로..
  * 승격 될때 MHA 방식. MMM 등 , AWS는 뭐 알아서 해주고

* 복구 후 새로운 StandBy에서 초기화가 필요하지

  * 초기에 데이터 복제 하느라 Primary에 부하가 가중된다
  * Mysql -
    * Rebooting으로 해결되는 케이스, 
    * 대체 해야하는 경우
  * Secondary 몇개나 두지? 
    * 2대를 추천함!
    * 복구시 Primary가 아닌 Secondary에서 해버려서!
    * redis는 안되더라 .. primary..무조건

* Standby는 평소 백업용이고 서비스에서는 사용 X - 같은 규모, 성능의 장비

### 읽기분배

* 읽기가 Secondary로, Primary만 write

단점 

* Replication Lag
* 시간차 발생함, Eventual Consistency
* 뭐 근데 대부분 큰 문제는 안댐!
  * 서비스에 따라!
* Replication Lag상태에서 데이터를 Cache하는 경우 문제가 오래 지속될지도.

### 실습은 별거 없는듯

그냥 replication Aurora에서 자동으로 되는거 확인정도

Internal external dns



## 6. 샤딩 Sharding

### State

* 사라지지 않고 유지해야 하는 정보 - DB
* 유지하지 않아도 되는 데이터
  * Scrap 서버- , 데이터가 없으면 다시 접속해서 생성
  * GeoIp서버도 호출 해서 결과를 가져올 수 있다.
  * 쉽게 재생성 할 수 있는 데이터들을 Stateless한 데이터라고 한다.
  * 실제 필요한 데이터를 DB에 저장하고, 비지니스 로직만 들고 있는 API 서버들은 대부분 stateless
  * Stateless한 서버는 그냥 lb에 추가만 하면 됨 - 로직만 들고있어서!

### State 서버의 확장은?

* State를 저장하는 DB서버의 확장은 쉽지 않다. - scale up을 한다.
* Query Off - 읽기 분산으로 부하를 분산하는 방법을 알아봤었지?
* ![image](https://user-images.githubusercontent.com/72075148/135279454-98493e9e-049e-4895-bd1b-08e7981a97a7.png)
* ![image](https://user-images.githubusercontent.com/72075148/135279491-c75dbff9-bb5a-44af-9272-8e8f3b35a733.png)
* 계속 replica 장비를 추가하면? 
* 쓰기 연산이 어쨋든 계속..어쩌구 .웅애
* 더 좋은 장비를 쓰게된다ㅣ..,.

## Partitioning

### Vertical Partitioning

* 테이블을 컬럼 기준으로 나눈다.
* 자주 사용하는 컬럼과 자주사용하지 않는 컬럼을 나눠서 성능을 향상시킨다.
  * 자주 안쓰는거 없어져서 테이블이 더 작은 사이즈를 차지하게된다.

### Horizontal Partitioning

* 같은 테이블을 데이터 기준으로 나눈다

* 데이터의 개수가 적어지므로 하나의 디비에서 처리해야하는 부하가 줄어든다

* Sharding이라고함

* 여러대의 DB와 연결되어야하는 단점

* 어떤 데이터를 어디에 저장하냐?

* 

  ##### Key를 처리하는 방법?

  * Range 1~1000, 1001~2000
    * 새로운 Shard를 추가하는게 쉬움
    * 균등하지 못할수있음
  * Modular
    * 한대 추가되면 데이터의 이동이 심해진다
    * 한번에 두배로 늘리면? 절반이 이동해서 ㄱㅊ함 
      * 1%2 = 1 
      * 2%2 = 0 
      * 3%2 = 1 
      * 4%2 = 0 
      * 1%4 부터는 0,1,2,3으로 디면서 반반이동임
    * 그럼 1대 2대 4대 8대 ;; 16대;;;;
    * PreShard한다음 Scale-Up으로 가져감
  * Indexed
    * 특정 데이터 위치를 가리키는 서버가 존재
    * 상태도 있음
    * 분배를 원하는 형태로 하기 쉬움
    * 걔가 하나의 서비스라서 SPOF가 될 수 있음
    * 관리 포인트 증대
    * 매번 질의해야함,
    * 클라이언트가 위치를 요청했을 때 저장하는 방식으로 장애 완화함
  * Complexed 
    * 다 섞어 구현이 복잡해
    * ![image-20210930023715653](/Users/seongjunkim/Library/Application Support/typora-user-images/image-20210930023715653.png)



## 실습

* zookeeper / redis 쓰나범

* ```python
  data = {
      "0": {"host": "redis0:127.0.0.1:16379", "start": 0, "end": 1000},
      "1": {"host": "redis1:127.0.0.1:16380", "start": 1000, "end": 2000},
      "2": {"host": "redis2:127.0.0.1:16381", "start": 2000, "end": 3500},
      "3": {"host": "redis3:127.0.0.1:16382", "start": 3500, "end": -1},
  }
  ```

* -1  이면 키 더 큰거 그냥 다 

* ![image](https://user-images.githubusercontent.com/72075148/135449160-37db4b90-ebc9-40a3-80fb-120eeb0f802d.png)

* ![image](https://user-images.githubusercontent.com/72075148/135449206-71ecaf4f-a78f-4af3-9ef0-170ee2e0a081.png)

* /api/v1/write_post/{usr_id}

* /api/v1/posts/{usr_id}/{post_id}

* /api/v1/posts/{usr_id}

* user_id 기준으로 range shard

* ```python
  class RangeShardPolicy(ShardPolicy):
      def __init__(self, infos):
          length = len(infos) 
  
          current = infos[0]
          if current.validate() == False:
              raise Exception("RangeInfo is invalid")
          
          for i in range(1, length):
              prev = infos[i-1]
              current = infos[i]
  
              if current.validate() == False:
                  raise Exception("RangeInfo is invalid")
  
              if prev.end != current.start:
                  raise Exception("RangeInfo Order is invalid")
  
          self.infos = infos
  
  ```

* 





## Consistent Hashing

* 서버 추가/삭제 시 리밸런싱이 계속 일어남 - sharding modular방식
* 같은 해시를 사용하면 항상 같은 결과
* 서버별로 해시를 적용한다?
  * Rule을 정한다? - Hash의 값보다 크면서 가장 가까운 Hash값을 가진 서버에 자신의 데이터를 저장한다.
  * ![image](https://user-images.githubusercontent.com/72075148/135321548-6d6b75fe-c182-4091-b1b5-cd3d494e55f9.png)
  * 서버 장애가 발생하면 해시 링의 다음 서버에 모든 부하가 넘어간다. 따라서 부하에 안정적이지 않음
* Virtual Node
  * Hash에 + 해서?  가상 주소를 만들어서 에 매칭을 한다.
  * ![image](https://user-images.githubusercontent.com/72075148/135321760-9462c1a3-bcc2-451e-a5c6-baeccacf1c2a.png)
  * 균등해짐.
* 서버 이름을 어떤 값을 서버의 Key로 사용해야할까?
  * IP? DNS?? 
  * 계속 사용할 수 있는 이름을 사용하면 링이 유지되지만 변경되는걸 쓰면 안됨 데이터 위치가 바뀜
  * 유니크한 닉네임을 사용해라
* ketema hash를 사용했음
  * md5를 써서 느림
* 그래서 murmurhash3
* jump hash
  * 고정된 값으러 매번 시드가 바뀌면 머시ㅣㄱ한거 말거
  * 속도 빠른거>???



## 실습

* docker로 redis 4대 키고
* redis를 닉네임으로 쓴다
* ![image](https://user-images.githubusercontent.com/72075148/135451723-24d5dbd4-0f4a-4970-bb39-a72392983572.png)
* ketama 해시를 만들어서 쓰고있고
* 리플리카 

# GUID

* 메일서비스 설계해보자

  * 가입
  * 수신
  * 리스트
  * 상세

* 가정

  * 메일 정보는 각각 분리되어있다
    * 사용자의 메일 수신 리스트
    * 각 메일의 실제 파일 내용
  * 한 계정의 메일 목록 정보는 모두 같은 DB안에 존재한다.
    * 한 계정의 정보는 여러 DB로 샤딩되지 않는다.
  * EML을 저장하는 부분은 AWS S3 같은 오브젝트 서비스를 사용함
  * 메일 ID만 보고도 어떤 DB에 관련 정보가 있는지 알 수 있어야한다.

  

* 사용자 정보와 사용자 메일의 메타정보는 다르다

  * 메일 정보 
    * 발신자
    * 타이틀
    * 본문 등 
  * 계정 정보
    * 이메일
    * 로그인 관련..

* 2억명 사용자가 있다고 가정

  * 각 유저는 1024Byte 데이터 사용
  * 1024*2억 = 191GB
  * 8:2법칙에 따라서 20프로 정도가 빈번하게 접근해도 38.2G
  * 크게 샤딩이 되지 않더라도 샤딩 될 일이 없다.,
  * 샤딩이 필요해도 Range 샤딩 정도로 충분함

1. 메일 수신하는경우

   * 디비에 대용량 파일을 넣으면 속도 몇메가 이런게 디비에 넣어야한다는게 착각 , 더 빠르다고 생각하는데 아님
     * 경로랑 거기서 갖고오는게 성능이나 비용측면훨나음
   * 수신받는 도메인은 하나만 ..
   * EML ( 메일 내용 ) 은 DB가 아닌 다른 곳에 저장된다. S3
   * 메일을 가져가는 방법은 일단 수신 받은 시간 순으로만 된다고 저장한다.
     * Nosql - second index 써야하고 등 .. 제공해야하냐 고민
     * 송신자 순 메일 제목순 은 고려 안한다.

2. 메일이 1024바이트라면 

   * 2억명의 유저가 메일 1000개씩 들고있다고 가정하면
     * 191*1000 이므로 DB당 1테라 정도 스토리지면 190개의 샤드
   * 2백만명이 1000개면
     * 1.9 테라정도 스토리지 - 1TB씩 쓰면 2개의 샤드
   * 즉 사용자의 데이터는 스토리지를 많이 사용함
   * ![image](https://user-images.githubusercontent.com/72075148/135323567-5e7b2039-5d74-48f8-85a3-74e0b9414570.png)
   * ![image](https://user-images.githubusercontent.com/72075148/135323749-2d808190-a063-48f4-9c8d-39becaaee815.png)
   * EML저장을 위한 서비스 추가로 필요
   * EML파일에 대한 key를 무엇으로 하나? 
   * Uniq한 값을 만들어낼 수 있어야한다.
   * {receiver_id}_{mail_id}
     * mail_id 자체로는 나눠진 shard마다 중복 존재 가능함
       * mail_id를 auto increment 로 쓰면 shard 전체에서 유일한 key가 아닌 db에서만 유일
       * 그래서 저건 유니크하다? 그런가 진짜>?? 아 마자 어차피 샤딩해서 그 유저의 디비는 정해져있는거구나,.
   * uuid로 유일성을 보장하는거로,
     * 128bit , 36char 라서 좀 크다,...;
     * 시간정보가 들어가지만 시간 순으로 정렬되지 않는다.
   * 새로운 아이디가 필요하다
     * 유일성을 보장해야한
     * 용략을 적게 차지해야한다
     * id만으로 시간의 순서나 생성 시간을 알 수 있어야한다
     * 필요한 특정 정보를 담을 수 있어야한다.

   ## Simple Key version

   * 64bit - 8bytes
   * Timestamp - 52bits + sequence - 12bits
   * 기존 user_id를 생성되는 Key와 붙여서 사용하는 방법
   * 62029324585984 >> 12 = 1515948385 
   * 62029324585984 & 0xFFF=1024
   * charsyam_62029324585984
   * 생성 프로세스가 하나일 때만 유일성이 보장된다. - 타임 스템프 .. 프로세스 하나면 ..
   * ![image](https://user-images.githubusercontent.com/72075148/135324850-0a064f65-9f4e-4419-864f-d0d3d59f62e4.png)
   * worker ID 붙여서 . - 4bits으로 ? - 16대까진 ..
   * key 생성 서버를 구축해야함
   * key만 보고 shard를 알 순없나?
   * ![image](https://user-images.githubusercontent.com/72075148/135325064-3f440ea3-95c2-45fe-84bb-190b2d51ac79.png)

   * 그럼 개별 유저의 데이터 이동이 가능한가..?
   * 샤드 정해진 크기만 쓰고, 유저간 샤드 재배치는 없다고 가정하는거임
   * scaleup하는거로 하고, 빨리 찾는게 중요하는 그렇게 하는거로 ...
   * 그냥 유저 id랑 메일 아이디로 하면 안대나 ..쩝  - eml에 저장할떄.흠
     * 아 재배치가 어려워서 그런가?
     * 같은 아이디면 옮길 때 어려워서 ? 새로 만들어야하니까 , .. 
     * 글로벌하게 유니크한거로,

### 실습

* 데이터 sharding을 위해서 Key가 유일 할 필요가 있다, - db여러대쓰면 유일안하고, uuid는 유일하지만 키 사이즈가 큼
* 유일성을 보장한다,.
* 시간으로 정렬이 가능하다,
* twitter의 snowflake방식을 제안
* ![image](https://user-images.githubusercontent.com/72075148/135453653-70e2000b-c720-43c4-90ab-eb1a2ac9bfb6.png)
* 현재시간부터임  지금부터 시간임?
* datacenterid와 workerid가 중복되면 중볻괸 값이 발생할 수 있음
* 저러면 오우
* guid , guid_str두개 만들어서 쓴다?

# 비동기큐

* 바로 쓰면 부하가 늘어날 때 Latency가 늘어나고 처리량이 조절 안됨 - 
* 오래걸리는거 - 디비 아니더라도 , 비동기로 후 처리
* 큐에 넣고 워커들이 .. 인코딩 처리를 하고 .. 뭐 어쩌구
* 유저는 응답 받고 안써졌으니까 흠좀무 하자나 - 이거 먼저 캐싱 처리하고 후처리한다?
  * Write Back형태를 취한다.
  * hotkey이슈가있다?
* 작업 큐에 들어오는건 워커로 조절이 되는데 유저 수는 조절이 안되니까.
* Redis를 이용한 Sidekiqm Jesquem Kafka같은거 쓸수있다.
* 대규모 트래픽 발생하면 처리량을 조절하는 BackPressure로 동작
* 작업 큐를 .. redis replicationㅇ쩌구 해서 ,, 안정적으로 ,

### 실습

* 사이드킥 - 레디스 기반의 큐
* 

## 배포

* 일종의 무정지 배포
* 서버를 내리고 올리고, 배포 끝나면 다시 LB에 추가
* rolling update
* 기존 서비스의 중지 - 이전 소스나 바이너리 복사, 서비스 재시작
* 롤링 업데이트에서의 롤백은 배포랑 동일한 시간
* 배포에 굉장히 많은 시간이 걸리면?
* Blue set / Green set이 존재
* 같은 양의 Green set을 준비 - 새로운 버전을 배포
* Blue Green은 쉬운가?
  * 같은 장비를 쉽게 준비할수있나
    * cloud는 쉽지
    * 온프로미스에서는 같은 양이 있어야하니까 .
      * 사용하는 리소스의 제한 ,
      * 한서버에 두개의 프로세스와 proxy를 실행
      * 새로운 장비 수급 없이 배포 가능
      * 리소스를 풀로 사용 못하니까 부하 많으면 배포시 장애가 발생,,,

* Canary Deployment - 그 새인가바
  * 새로 배포한 버전에 버그있으면 롤백해도 영향..
  * 일부만 배포하고 확인하고 상태 점검 후 나중에
  * 안드로이드 보면 퍼센트로 배포 가능한데 그런식>
  * 한대만 배포하면? 로드밸런서에서... 다음 요청도 저기서 같은곳에서 받는게 맞니>?
  * Canary에 접근하는 유저는 그 다음에도 거기로 가도록 Tag생성해서 다른 서버에서는 해당 유저는 특정 서버로 redirection되도록
  * 모든 서버에 구현 후 특정 유저만 해당 기느 동작하도록
  * 

## 실습

* 80포트로 바꾼다음에 돌리고, 
* geoip 를 돌려
* 그럼 80포트에서 접속 안되다가
* lb로 접속하면 연결 됨
* 7002로 배포 후
* 7001 포트로 새로 배포 하고
* nginx-  geoip_port를 변경해서 배포  - elb는 nginx 80번만 보고있음



### AWS에서 bluegreen targetGroup변경, weigh 변경



