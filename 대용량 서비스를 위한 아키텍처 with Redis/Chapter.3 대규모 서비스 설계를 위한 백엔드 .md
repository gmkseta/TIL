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











