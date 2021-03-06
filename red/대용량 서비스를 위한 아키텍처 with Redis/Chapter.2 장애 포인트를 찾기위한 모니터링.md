# 장애 포인트를 찾기위한 모니터링



## 간단한 Scrap 서비스

* 요구사항
  * 제공하는 OG 파싱 후 보여주기
  * OG 없다면 아무것도 보여주지 않는다.
* OpenGraph
  * ogp.me 보면됨
  * 페이스북에서 웹 페이지의 정보를 요약해서 보여주기위해 만든 프로토콜
  * 등등 아는 대로임

### Scrap server http endpoint

* `/api/v1/scrap?url={{url}}`
  * url 은 urlencoding으로 인코딩 된다.
  * /api/v1/scrap?url=https%3A%2F%2Fwww.fastcampust.co.kr

Design doc

## 실습

```shell
pyenv local the-red-dev
pyenv rehash
```

로 그냥 같은 환경 사용 가능 

## 지표 수집과 모니터링 

### 서비스에서의 지표

* API call 수 
  * 현재 요청중인 초당 콜 수
  * 실패한 초당 콜 수
* API Latency
  * 현재 api 들의 속도가 median값 99%값 , 최대값 등의 지표

### 서비스 노드 지표

* 서버의 상태
* CPU사용량 ( DB, API, Cache 서버 CPU 사용량 )
* 메모리 사용량
* 디스크 사용량
* 네트워크 사용량 - 파일이나 ㅌㅔ이터 전송량
* 현재 동작중인 정상적인 서버의 수 

### 에러의 수집

* Sentrye등의 외부 서비스도 많이씀

### AWS에서 

* CloudWatch 쓸수있고
* 서비스 지표들은 자체적으로 수집해야함
* Datadog, New Relic, Watap 등 

### Alarm

* 등급을 나눈다
  * 서비스에 영향을 주나? 장애의 정도로
  * 즉각적인 조치가 필요한가? 





### Prometheu

### Grafana

* Visualization 을 한다.
* AGPL 이라서 사용자에게 노출되면 서비스의 소스코드 노출
* 꼭 데이터 소스가 Prometheus 일 필요는 없고 cloudwatch이런거 ㅇㅋ

### Sentry

실제 모니터링은 Prometheus 

따라서 데이터 소스를 제공해줘야함

- 같은 서버에 있으므로 internal ip로

scrap/metrics  라는 endpoint로 접근하면 값을 반환하게 된다.



## 성능 테스트

* 성능 테스트
  * 서비스가 어느 정도의 성능을 내는지를 알아보는 테스트
* 부하 테스트
  * 어느 부분에서 어느 정도 부하가 걸리는지
* 스트레스 테스트
  * 성능 / 부하 테스트가 특정 시간 이상 지속적으로 안정적으로 되는지 확인하는 테스트 

### 주의점

* 주요 시나리오를 테스트하나?
  * 하나만 호출 X 실제 서비스에서 사용되는 패턴으로
  * api마다 부하 종류가 다르다
  * 여러 api 조합이 필요할지도
* 클라이언트의 성능 한게를 확인한다.
  * 부하를 주는 클라이언트의 한계로 인해서 성능 측정이 어려울 수 있으므로 , 클라이언트를 점점 늘리면서 테스트

### 확인할 부분

* OS에서 설정하는 값들에 대한 확인이 필요하다
  * ulimit -a
    * open files
    * max user processes 라는 값의 튜닝
  * /etc/limits.conf 수정
  * 재시작 필요
* ec2는 재시작 보다 ami에 기본 설정을 해두고 이용이 더 좋음

### 툴

* ngrinder
* locust
* jmeter
* gatling
* ab

### Ngrinder

* 평균 tps / 최대 tps / 성공 수, 실패 수 
* 실패 수가 전체의 30%면 테스트 실패



실습 - 

테스트대상이 느려서 처리가 안되는 경우

Agent의 한계가 걸려서 부하럴 더 못 주는 경우





todo 

ansible 