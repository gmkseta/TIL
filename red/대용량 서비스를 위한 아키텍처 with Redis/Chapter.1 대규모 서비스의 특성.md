# 1. 대규모 서비스란

* 많은 사용자 트래픽
* 많은 사용자 데이터
* 트래픽 / 데이터 빠른 증가

스타트업에서 서비스의 인기가 좋아, 트래픽이 감당할 수 없을 정도로 늘어난다면? 며칠동안 서비스가 안된다면??

## 대규모 서비스가 가져야 할 특성

### 확장성 - Elastic

* 서비스의 가용 용량을 늘이고 줄이는 것이 쉬워야한다
* 트래픽이 늘어서 서버를 추가해야 한다면?
  * 추가가 되어야 하는 서버의 종류는?
  * 쉽게 가능한가?
* 줄어서 줄여야 한다면?
  * 제거가 되어야 하는 서버의 종류는?
  * 쉽게 제거 가능한가?

### 장애회복성 - Resiliency

* 서비스에 장애가 일어났을 때 가능한 메뉴얼한 처리 없이 자동적으로 회복되어야한다.
* 서비스 중인 API서버, 한,두대가 장애가 나면 서비스는 계속 지속될 수 있나?
* 서비스 데이터를 저장하는 DB가 장애가 나면 서비스는 계속 지속될 수 있나?
* SPOF가 없어야 한다
  * Single Point of Failure
  * 해당 지점에 장애가 발생하면 전체 서비스에 장애를 낼 수 있는 부분
  * 한대의 물리서버는 무조건 SPOF가 존재한다. - API서버 하나 / DB 서버 하나.
    * DB서버 늘렸을 때 Primary가 장애가 나도 Secondary로 서비스 - Replication
    * 모든 부분에서 최소 이중화가 되어야한다.
  * 이 외에도 SPOF가 발생할 수 있는 부분들
    * Switch, Route등 서버 외의 하드웨어 부분
    * Network의 Bandwidth의 한계
      * 10G 스위치에 10Gbps이상의 데이터를 전달 하면?
        * Capa를 넘어가는 순간 패킷 드랍이 발생한다.
    * Switch도 이중화가 필요하다.

* failover
* replication

### 자동화 - Automation

* 배포부터 장애처리 등 대부분 자동화 되어서 버튼 클릭 한두번 정더로 진행되어야한다.
* 서비스 운영의 많은 부분이 자동화가 되어야한다.
* IaC가 중요함
* On-Premis 서비스의 준비
  * 장비의 준비는 인프라팀의 도움이 꼭 필요하다.
  * 일부 기업에서는 이런 부분도 최대한 API를 통해 준비하기위해 private-cloud등을 도입
  * OS와 기본적인 네트웤 설정 이외에 모든 설정을 설치 스크립트 하나로 처리가 되어야한다. IaC
  * Chef / Puppet / Ansible

* Cloud - 서비스의 준비

  * IaC로 생성한다. - cdk 도 취급 해주세요 ㅜㅜ
  * 특정 이미지를 모두 만들어 둘 수도 있고, Terraform으로 인프라를 구성한 후에 ansible로 필요한 설정을 할 수도 있다.

* 모니터링 - Monitoring
  * 서비스 상태는 항상 모니터링 되어야 한다.

# 2. 실습

여러명이서 작업할때 state를 s3에 저장을 한다? 호우

```
terraform init
terraform plan -out "output"
terraform apply "output"
```

spot은 비용은 싸지만? - 한두시간 쓰면 사라질 수 있다.

* terraform 에서 나온 public ip / private ip로 create_hosts.py 변경해서 실행

* geoip 부분 아웃풋을 aws/hosts에 넣어둔다

geoip는 자동으로 `https://github.com/charsyam/geoip.git`  얘를 갖고와서 띄운다??

gunicorn으로 파이썬 어플리케이션을 띄워준다.

* ```
  ansible-playbook -i aws the_red_1_base.yml       
  ```

  * role에 따라서 뭐가 많이 만들어둔 듯

  * ```yaml
    ---
    - name: Configure users on all servers
      hosts: all
      become: yes
    
      roles:
         - { role: base, tags: [ 'base' ] }
         - { role: docker, tags: [ 'docker' ] }
         - { role: locust, tags: [ 'locust' ] }
         - { role: prometheus_node_exporter, tags: [ 'prometheus_node_exporter' ] }
         - { role: pyenv, tags: [ 'pyenv' ] }
    
    ```

* packer를 이용해 ami를 만들면 더 빠른 세팅

* packer sample도 보면 인프라 구축 ㅇㅇ

* ```
  ansible-playbook -i aws the_red_2_geoip.yml                 
  ```

* on Premis 에서 사용하는 방식임


TODO study

* ansible이 뭐 해주는건가?
* create_host.py.
* base.yml? 머임
* packer

















