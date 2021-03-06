- [ ] 데이터베이스를 사용하는 이유
- [ ] 데이터베이스의 특징]
- [ ] 관계형 데이터베이스의 구성 요소

  - [ ] 키
  - [ ] 스키마, 테이블
  - [ ] 인덱스

- [ ] ACID
- [ ] 트랜잭션

  - [ ] 격리수준
  - [ ] 커밋, 롤백

- [ ] 동시성 제어
- [ ] 트리거
- [ ] SQL injection
- [ ] ORM
- [ ] 정규화
- [ ] NoSQL

  - [ ] Cap

- [ ] Redis

  - [ ] 램? 그렇다면

- [ ] Memcached
- [ ] 자료구조
- [ ] 파티셔닝

  - [ ] 샤딩

- [ ] 레플리카
- [ ] Mysql vs Postgres

# RDB 기본

## 데이터베이스를 사용하는 이유

```
데이터베이스가 존재하기 이전에는 파일 시스템을 이용하여 데이터를 관리하였다.
(현재도 부분적으로 사용되고 있다.) 데이터를 각각의 파일 단위로 저장하며 이러한 일들을 처리하기 위한 독립적인 애플리케이션과 상호 연동이 되어야 한다.
이 때의 문제점은 데이터 종속성 문제와 중복성, 데이터 무결성이다.
```

```
* 파일 시스템의 문제점을 해결하기 위해 사용
* 파일 시스템이 OS마다 다를 수 있기 때문에 OS에 종속적인 파일 시스템을 이용하는 것은 프로그램의 확장성을 해침
* 데이터 중복, 비일관성, 검색 등의 문제 존재 -> 중복 최소화, 보안성, 계속적 변화에 대한 적응
* DB는 원자적 갱신, 동시성 제어, 데이터 보호, 백업 및 회복 등의 여러 데이터 관리 기능을 통해 데이터를 편하게 관리할 수 있음
```

## 데이터베이스의 특징

1. 데이터의 독립성
   - 물리적 독립성 : 데이터베이스 사이즈를 늘리거나 성능 향상을 위해 데이터 파일을 늘리거나 새롭게 추가하더라도 관련된 응용 프로그램을 수정할 필요가 없다.
   - 논리적 독립성 : 데이터베이스는 논리적인 구조로 다양한 응용 프로그램의 논리적 요구를 만족시켜줄 수 있다.
2. 데이터의 무결성
   여러 경로를 통해 잘못된 데이터가 발생하는 경우의 수를 방지하는 기능으로 데이터의 유효성 검사를 통해 데이터의 무결성을 구현하게 된다.
3. 데이터의 보안성
   인가된 사용자들만 데이터베이스나 데이터베이스 내의 자원에 접근할 수 있도록 계정 관리 또는 접근 권한을 설정함으로써 모든 데이터에 보안을 구현할 수 있다.
4. 데이터의 일관성
   연관된 정보를 논리적인 구조로 관리함으로써 어떤 하나의 데이터만 변경했을 경우 발생할 수 있는 데이터의 불일치성을 배제할 수 있다. 또한 작업 중 일부 데이터만 변경되어 나머지 데이터와 일치하지 않는 경우의 수를 배제할 수 있다.
5. 데이터 중복 최소화
   데이터베이스는 데이터를 통합해서 관리함으로써 파일 시스템의 단점 중 하나인 자료의 중복과 데이터의 중복성 문제를 해결할 수 있다.

## 데이터베이스의 성능?

데이터베이스의 성능 이슈는 디스크 I/O 를 어떻게 줄이느냐에서 시작된다. 디스크 I/O 란 디스크 드라이브의 플래터(원판)을 돌려서 읽어야 할 데이터가 저장된 위치로 디스크 헤더를 이동시킨 다음 데이터를 읽는 것을 의미한다. 이 때 데이터를 읽는데 걸리는 시간은 디스크 헤더를 움직여서 읽고 쓸 위치로 옮기는 단계에서 결정된다. 즉 디스크의 성능은 디스크 헤더의 위치 이동 없이 얼마나 많은 데이터를 한 번에 기록하느냐에 따라 결정된다고 볼 수 있다.

그렇기 때문에 순차 I/O 가 랜덤 I/O 보다 빠를 수 밖에 없다. 하지만 현실에서는 대부분의 I/O 작업이 랜덤 I/O 이다. 랜덤 I/O 를 순차 I/O 로 바꿔서 실행할 수는 없을까? 이러한 생각에서부터 시작되는 데이터베이스 쿼리 튜닝은 랜덤 I/O 자체를 줄여주는 것이 목적이라고 할 수 있다.

## 관계형 데이터베이스의 구성요소

- 데이터가 테이블에 저장.
- 구성요소: 행(튜플), 열(속성)
  - 행은 순서가 없지만, 열은 순서가 있다.
- 스키마: 이름과 데이터 유형을 정의
- 키: 테이블에서 특정 행을 유일하게 식별할 수 있게 하는 특징, 열 혹은 복수의 열 모음
  - 테이블의 각 행에는 프라이머리 키 값이 반드시 있어야 한다.
- 외부키
  - 이용하여 다른 테이블과 링크할 수 있다.
  - 그 값이 다른 테이블의 키 열의 값과 같은 열
  - 참조무결성: 모든 외부 키 값이 참조하는 테이블의 값으로 존재하는 경우

### 테이블

- 행과 열로 이루어진 데이터의 집합

### 행

- 테이블을 구성하는 데이터 셋으로 `튜플`이나 `레코드`라고 불림
- 한 객체에 대한 정보를 가짐

### 열

- 테이블을 구성하는 데이터 셋으로 `속성`이라고 불림

### 도메인

- 데이터베이스 필드에 채워질 수 있는 `값들의 집합`

### 뷰

- 하나 이상의 테이블에서 유도된, 메모리에 물리적으로 존재하지 않는 `가상 테이블`
- 특정 사용자로부터 특정 속성을 `숨기는` 기능으로 뷰를 정의하여 그 뷰를 테이블처럼 사용
- 인덱스를 가질 수 없고, 뷰의 정의를 변경할 수 없음
- 테이블의 기본키를 포함하여 정의 시, 삽입/삭제/갱신 가능

- 검색, 정렬 시 튜플을 구분하는 기준이 되는 속성 (Attribute)
- 용어
  - 유일성: 키로 튜플을 유일하게 식별할 수 있음
  - 최소성: 튜플을 구분하는데 꼭 필요한 속성들로만 구성

### 키

- 검색, 정렬 시 튜플을 구분하는 기준이 되는 속성 (Attribute)
- 용어
  - 유일성: 키로 튜플을 유일하게 식별할 수 있음
  - 최소성: 튜플을 구분하는데 꼭 필요한 속성들로만 구성

### 👉 후보 키 - candidate key

- 릴레이션을 구성하는 속성들 중에서 튜플을 `유일하게 식별` 할 수 있는 속성들의 `부분 집합`
  - 기본 키로 사용할 수 있는 속성들
- 모든 테이블은 하나 이상의 후보 키를 가짐
- 유일성과 최소성 만족

### 👉 기본 키 - primary key

- 후보 키 중에서 선택한 Main Key (주 키)
- 특정 튜플을 유일하게 식별할 수 있음
- 중복 값과 NULL 값 불가 (`개체 무결성`)
- 유일성과 최소성 만족

### 👉 대체 키 (보조 키) Alternate key

- 후보 키가 두개 이상일 때, 기본 키를 제외한 나머지 후보 키

### 👉 슈퍼 키

- 유일성을 만족, 최소성은 만족하지 않는 속성들의 집합

### 👉 외래 키

- 한 테이블의 키 중에서 다른 테이블의 튜플을 식별할 수 있는 키
- 참조되는 릴레이션의 `기본 키`와 대응되어 릴레이션 간에 `참조 관계`를 표현하는 키
- 사용 이유: 테이블을 연결, 중복 방지, 무결성 유지
  - 예시: 물건 구매시 같은 사람이 여러 물건을 구매하면 사람에 대한 데이터가 중복 -> 사람과 물건 구매로 테이블을 분리해 중복 제거

## 스키마와 테이블의 차이

### 👉 스키마

- 데이터베이스의 조직, 데이터 구조에 대한 공식적인 설명 -> 테이블, 열, 데이터 유형, 인덱스 등의 정의를 포함
- `테이블(릴레이션)의 이름과 속성들의 나열`로 테이블에서의 첫 행 헤더, 데이터의 구조와 구성을 설명

### 👉 테이블

- `행과 열로 구성된 데이터 집합`

## 인덱스

### 정의 및 사용 이유

- `추가적인 쓰기와 저장 공간` 사용을 통해 데이터베이스의 `검색 속도 향상`을 위해 사용하는 자료구조
- 칼럼의 값(Key)과 해당 레코드가 저장된 주소를 `키와 값의 쌍`으로 인덱스 정의

### 👉 장단점

- 검색 속도 향상
- 데이터의 추가, 삭제, 수정의 경우 인덱스도 변경해야 하여 성능이 오히려 저하될 수 있음
- 추가적인 저장 공간 필요 및 저장 성능 저하

하지만 검색성능을 실질적으로 향상시키기 위해서는 해당 쿼리가 index를 사용하는지, 카디널리티, Selectivity 같은 요소들이 고려된 인덱스가 생성되어야 합니다.

일반적인 경우의 장점으로는 빠른 검색 성능을 들 수 있습니다.

일반적인 경우의 단점으로는 인덱스를 구성하는 비용 즉, 추가, 수정, 삭제 연산시에 인덱스를 형성하기 위한 추가적인 연산이 수행됩니다.

따라서, 인덱스를 생성할 때에는 트레이드 오프 관계에 놓여있는 요소들을 종합적으로 고려하여 생성해야합니다.



## 트랜잭션

- 데이터베이스의 상태를 변화시키는 하나의 `원자적인/논리적인 작업 단위`
- Lock과 유사한 기능을 하지만 Lock은 동일한 자원을 요청할 경우 한 시점에는 하나의 커넥션만 변경하는데에 반해 트랜잭션은 논리적인 작업의 쿼리의 개수와 관계없이 논리적인 작업 셋 자체가 `100% 적용되거나 아무것도 적용되지 않아야 함을 보장`
- 주의사항
  - 최소한의 코드에 적용하는 것이 좋음
  - DB 커넥션의 수는 제한적 -> 커넥션이 부족해 대기할 수 있음
- 동시에 여러 트랜잭션이 처리될 때, 특정 트랜잭션이 다른 트랜잭션에서 변경/조회하는 데이터에 대한 접근 권한 수준을 결정하는 것
- 트랜잭션에서 일관성 없는 데이터를 허용하도록 하는 수준

### 트랜잭션의 격리 수준(Transaction Isolation Levels)

- 트랜잭션 격리수준은 고립도와 성능의 트레이드 오프를 조절합니다.\
- 동시에 여러 트랜잭션이 처리될 때, 특정 트랜잭션이 다른 트랜잭션에서 변경/조회하는 데이터에 대한 접근 권한 수준을 결정하는 것
- 트랜잭션에서 일관성 없는 데이터를 허용하도록 하는 수준

#### Read Uncommited lv 0

- Select를 수행할 때 해당 데이터에 Shared Lock이 걸리지 않는 레벨
- 다른 트랜잭션에서 커밋되지 않은 내용도 접근할 수 있음
- 일관성 유지가 거의 불가능

#### Read Committed lv 1

- 다른 트랜잭션에서 커밋된 내용만 참조할 수 있다.
- SELECT를 수행하는 동안 해당 데이터에 Shared Lock이 걸리는 레벨
- 커밋된 내용만 접근 가능

#### Repeatable Read lv 2

- 트랜잭션이 완료될 때까지 SELECT 문장이 사용하는 모든 데이터에 Shared Lock이 걸리는 레벨
- 트랜잭션에 진입하기 이전에 커밋된 내용만 접근 가능
- 데이터 추가는 허용, 변경/삭제는 허용하지 않음

#### Serializable lv 3

- 트랜잭션에 진입하면 락을 걸어 다른 트랜잭션이 접근하지 못하게 한다.(성능 매우 떨어짐)
- 트랜잭션이 완료될 때까지 SELECT 문장이 사용하는 모든 데이터에 Shared Lock이 걸리는 레벨
- 완벽한 읽기 일관성을 제공함
- 데이터의 추가/변경/삭제 불가능

트랜잭션에도 상태가 있다는 것을 아시나요? 🚉

- Active: 트랜잭션이 동작중인 상태

- Failed: 트랜잭션이 실패한 상태

- Partially Commited: 트랜잭션에 `Commit` 명령이 도착한 상태, `sql` 문이 실행되고 남은 `commit` 만 남은 상태를 의미한다

  > 이 단계에서 Commit에 문제가 발생하면, `Failed` 상태로 돌아가게 된다. 성공하면 `Commited` 상태

- Commited: 트랜잭션이 성공적으로 완료한 상태

- Aborted: 트랜잭션이 취소되고, 트랜잭션 실행 이전의 데이터로 돌아간 상태

##

## Commit과 Rollback

### Commit

- 트랜잭션이 성공하여 트랜잭션 결과를 `영구적으로 반영`하는 연산

### Rollback

- 트랜잭션의 실행을 취소하였음을 알리는 연산
- 트랜잭션이 수행한 결과를 `원래의 상태로 원상 복귀시키는 연산`

## 동시성 제어 (병행 제어)

### 👉 정의

- 동시에 여러개의 트랜잭션을 병행 수행할 때, 트랜잭션들이 DB의 `일관성`을 파괴하지 않도록 `트랜잭션 간의 상호작용을 제어`하는 것

### 👉 목적

- DB의 공유도 최대화
- 시스템 활용도 최대화
- 응답 시간 최소화
- 단위 시간당 트랜잭션 처리 건수 최대화
- DB의 일관성 유지

### 👉 필요성

#### 갱신 분실

- 같은 데이터를 동시에 갱신할 때 갱신 결과의 일부가 사라짐

#### 모순성

- 동시에 같은 데이터를 갱신할 때, 데이터의 상호 불일치가 발생 (비일관성)

#### 연쇄 복귀

- 트랜잭션 중 하나에 문제가 생겨 롤백되는 경우, 다른 트랜잭션들도 함께 롤백

### 방법1: 로킹(Locking)

- 트랜잭션이 데이터에 접근하기 전에 Lock을 요청해서 Lock이 허락되면 그 로킹 단위에 접근할 수 있도록 하는 기법
- 하나의 트랜잭션이 사용하는 데이터에 다른 트랜잭션이 접근하지 못하게 락을 설정 -> `잠근후 실행, 실행 완료 후 언락`
- 테이블, 속성, 튜플 단위로 락 설정 가능
- 종류
  - 공유락(Shared Lock): 사용중인 데이터를 다른 트랜잭션이 읽기 허용, 쓰기 불허용
  - 베타락(Exclusive Lock): 사용중인 데이터를 다른 트랜잭션이 읽기, 쓰기 모두 불허용

### 교착상태 (데드락)

- 둘 이상의 트랜잭션이 자원의 잠금(Lock)을 획득한 채 다른 트랜잭션이 소유하고 있는 잠금을 요구하며 `무한정 대기`하는 것
- 잠금을 사용하면 발생할 수 있음

### 방법2: 타임스탬프

- `각 트랜잭션이 데이터에 접근할 시간을 미리 지정`해 시간의 순서에 따라 순서대로 데이터에 접근하여 수행
- 제한적인 시간이 존재하므로 데드락 발생하지 않음

## 무결성 제약조건

- 개체 무결성: 주키는 null, 중복 값을 가질 수 없음
- 참조 무결성: 외래키는 null이거나 참조 릴레이션의 기본키 값과 동일해야 함

## 조인

- 두 개 이상의 테이블이나 데이터베이스를 `연결하여 데이터를 검색`하는 방법
- 적어도 하나의 칼럼을 서로 공유하고 있어야 함

## 시퀀스(오라클)

- `순차적으로 증가하는 숫자를 생성`하는 객체
- `기본 키`와 같은 유일한 숫자를 자동으로 생성하는 것
- 캐쉬에 있어 속도 빠름, 중복 방지에 사용

## 트리거

- DML이 수행되었을 때, 자동으로 실행되게 정의한 프로시저
- DML(INSERT, UPDATE, DELETE)에 의한 데이터 상태관리 자동화
- 데이터 무결성 강화, 업무 처리 자동화

## SQL

- DML: 데이터를 조작

  | 명령어 | 설명                     |
  | ------ | ------------------------ |
  | SELECT | DB의 데이터 조회 및 검색 |
  | INSERT | 데이터 삽입              |
  | UPDATE | 데이터 수정              |
  | DELETE | 데이터 삭제              |

- DDL: 데이터(구조, 객체)를 정의

  | 명령어   | 설명                                |
  | -------- | ----------------------------------- |
  | CREATE   | DB의 테이블 생성                    |
  | DROP     | 테이블 삭제                         |
  | TRUNCATE | 테이블의 데이터 삭제, 테이블 초기화 |
  | ALTER    | 테이블 수정                         |

  - DROP과 TRUNCATE의 차이

- DCL: 권한 제어

  | 명령어 | 설명                  |
  | ------ | --------------------- |
  | GRANT  | 객체에 대한 권한 부여 |
  | REVOKE | 객체에 대한 권한 회수 |

- TCL: 트랜잭션 설정

  | 명령어   | 설명                       |
  | -------- | -------------------------- |
  | COMMIT   | 트랜잭션의 결과 반영       |
  | ROLLBACK | 트랜잭션 취소 및 원상 복구 |

## SQL Injection

- 해커에 의해 조작된 SQL 쿼리문이 데이터베이스에 그대로 전달되어 비정상적인 명령을 실행시키는 공격 기법
- view를 활용하여 접근하는 에러를 볼 수 없게 하고 검증 로직을 추가하여 방어해야함
- 입력값 검증, Prepared Statement 사용(쿼리에 대한 컴파일을 먼저 수행하고, 입력값을 나중에 넣는 방식)

## 힌트(Hint)

- SQL을 `튜닝`하기 위한 지시 구문, 개발자가 직접 최적의 실행 계획을 제공하는 것

## ORM

ORM(Object Relation Mapping): 데이터베이스와 객체 지향 프로그래밍 언어간의 호환되지 않은 데이터를 변환, 맵핑하는 기술 가장 핵심적인 요소는

```
데이터베이스에 의존적인 설계가 아닌, 프로그래밍 지향적인 데이터베이스 설계가 가능하다
SQL을 고려해서 비즈니스 로직에 신경쓰지 않고, 객체지향적인 코드만으로 데이터베이스에 대한 의존성을 덜어낼 수 있다
```

하지만 모든 것을 `ORM` 에 의존할 수는 없다.

테이블이 복잡하거나, SQL 쿼리 성능 향상을 위해서는 직접 쿼리를 만들 수 밖에 없고, 결국 SQL 을 써야되는 상황이 올 수 있다.

이때 해결해주는 것이 바로 Java 진영의 **QueryDSL** 이라는 훌륭한 라이브러리가 존재한다.

ORM 프레임워크에는 여러가지들이 존재하는데, 소개하기 전에 먼저 `Persistent` 에 대한 개념을 알아야 한다.

### Persistent

영속성(Persistent)이란 데이터를 생성한 프로그램이 종료되도 사라지지 않는 데이터의 특성을 의미한다.

영속성을 갖지 않는 객체는 메모리에서만 존재하기 때문에, 프로그램을 종료하면 모두 잃어버리게 됩니다.

Service의 Repository에서 데이터베이스를 통해 데이터를 꺼내오는 과정에 대한 전체적인 Flow인데요,

영속성 Layer에서 Database에 있는 실제 데이터를 꺼내오고, 객체(Object)와 Mapping하는 과정이 이루어지게 됩니다.

다만 영속성에 대해서는 상태들이 존재하는데요,

1. `비영속(new/transient)` : 엔티티 객체가 만들어져서 아직 저장되지 않은 상태
2. `영속(managed)` : 엔티티가 영속성 컨텍스트에 저장되어, 영속성 컨텍스트가 관리할 수 있는 상태
3. `준영속(detached)` : 엔티티가 영속성 컨텍스트에 저장되어 있다가 분리된 상태로, 영속성 컨텍스트가 더 이상 관리하지 않은 상태
4. `삭제(removed)` : 엔티티를 영속성 컨텍스트와 데이터베이스에서 삭제

**그렇기 때문에 객체가 영속성 상태인지, 아닌지 알고 있는 것이 굉장히 중요합니다**

#### 영속성 객체가 저장되는 과정

엔티티가 영속성을 바탕으로 데이터베이스에 저장되는 과정은

1. Application의 엔티티가 만들어져
2. 서 JPA 에게 save 명령을 전송하게 되면
3. 만들어진 엔티티는 **1차적으로 영속성 컨텍스트** 에 저장되고, 저장한 엔티티를 데이터베이스에 저장되기 위한 쿼리문을 생성하여 `지연 쓰기 SQL 저장소` 에 저장됩니다
4. Application에서 commit 명령이 내려지게 되면, 영속 컨텍스트는 자동으로 **flush** 되고
5. 영속성 컨텍스트가 변경 내용을 데이터베이스와 동기(flush) 하게 됩니다 = **SQL 저장소에 쿼리를 전송하게 된다**
6. 마지막으로 데이터베이스에 commit 쿼리문을 명령한다

##

### 데이터베이스 관련 질문

- 일반 SQL
  - 뷰와 테이블의 차이점이 무엇인가?
  - HAVING 문이 하는 일이 무엇인가?
  - 인덱싱할 열을 어떻게 선택하는가?
- PostgreSQL 관련 질문
  - [리소스 소비](http://www.postgresql.org/docs/current/static/runtime-config-resource.html)를 어떻게 개선시키는가?
- SQL 서버
  - 어떻게 SQL 서버를 PostgreSQL이나 MySQL로 이전하겠는가?
- NoSQL 데이터베이스에 대해서 얼마나 아는가?

## 정규화

정규화는 데이터의 중복방지, 무결성을 충족시키기 위해 데이터베이스를 설계하는 것을 의미합니다.

이 이상을 물어보는 경우가 있었는데, 학습이 좀 더 필요한 것 같습니다.

## vs NOSQL

## NoSql

Not Only SQL.

관계형 데이터베이스 모델을 **지양** 하며, 느슨한 스키마를 제공하는 데이터베이스 저장소.

동적인 스케일 아웃을 지원하며, 가용성을 위해 데이터 복제 등의 방법으로 관계형 데이터베이스가 제공하지 못하는 성능과 특징을 제공.

비관계형 데이터베이스에, 비구조적인 데이터를 저장하기 위한 분산 저장 시스템.

그렇기 때문에 **더 융통성있는 데이터 모델** 을 사용하고, **데이터 저장 및 검색을 위한 특화된 매커니즘** 을 제공

### CAP 이론

1. Consistency(일관성): 다중 클라이언트에서 같은 시간에 조회하는 데이터는 항상 동일한 데이터임을 보증하는 것

2. Availability(가용성): 모든 클라이언트에서 읽기와 쓰기 요청에 대하여 항상 응답이 가능하다는 것을 보증.

3. Partition tolerance(네트워크 분할 허용성): 지역적으로 분할된 네트워크 환경에서는 네트워크 데이터의 유실이 일어나도 각 지역내의 시스템은 정상적으로 동작해야 된다를 의미함

   > 네트워크 장애가 일어나냐를 의미한다. 제대로 Replication이 되는지 보는 것.
   >
   > A, B, C 노드가 있는데 B 노드의 네트워크 장애로 이어져도 제대로 서비스를 할 수 있느냐를 물어본다

보통 데이터베이스는 CAP 이론중에서 2가지만 만족할 수 있는데,

`Nosql` 은 여기서 **AP** 를 만족하는 특성을 가지고 있고,

> NoSql ex) DynamoDB 를 사용하다 보면 종종 데이터 정합이 가끔씩 깨질때가 있다.

`RDB` 은 여기서 **CA** 를 만족하는 특성을 가지고 있고,

> 그래서 RDB의 경우에는 Partitioning과, Sharding이라는 개념이 존재한다.

`Redis/MongoDB` 의 경우 여기서 **CP** 를 만족하는 특성을 가지고 있다.

> 보통 Cache로 사용하는 저장소들의 특징이다. ( 일시 장애로 읽기 쓰기가 불가능해도 서비스 장애로 이어지지 않는다 )

## NoSQL

- 관계형 데이터베이스가 아닌 다른 형태 로 데이터를 저장하는 기술
- 특징
  - 반정형(명확한 스키마 없음, 일정 수준의 자유도 허용, NoSQL/JSON 형태의 데이터)/비정형(스키마 없음, 비디오/오디오 등의 멀티미디어 데이터) 데이터에 적합
  - ACID 대신 Eventual Consistency: Consistency를 조금 타협하고 꼭 실제 최신은 아닐 수 있지만 `업데이트가 되기 전까지는` 가지고 있는 최신의 데이터를 반환함을 의미 -> 분산형의 특성상 일관성 유지가 어려움
  - 대용량/분산형 데이터 저장에 유리
  - 특정 도메인의 문제 해결에 좋음: Key-value, Graph 등 자료 형태가 다양해 특정 분야에서 고성능(소셜 네트워크: 인간 관계는 그래프)
  - 데이터를 질의하는 API가 다양
  - 분산형 컴퓨터에 최적화, 확장성 좋음: 머신의 수를 늘리는 `수평적 확장`
  - NoSQL은 SQL보다 제품 지원이 어려움
  - 인력 운영 비용이 더 비쌈: 표준화 부족, 질의 언어 다양
- 종류
  - Column-based: 열 별로 연속적으로 저장, 기존 SQL은 테이블에 행 단위로 순차적으로 저장 -> 레코드의 특정 부분만 수정할 때, 필요한 열의 데이터만 로드하면 되서 IO 작업 감소, 한 열에 들어가는 데이터 형식에 일관성이 있어 DB 내의 한 블록은 동일한 유형의 데이터를 보유 -> 데이터의 유형에 맞는 압축 인코딩 가능, 디스크 공간 절약 및 성능 향상 가능
  - Document-oriented: JSON 객체로 문서(레코드)를 구성, 다양항 구조로 테이블 구성 가능, `MongoDB`
  - Key-Value: 연관 배열을 데이터 모델로 이용, Key는 한 Collection에 한 번만 등장 가능
  - Graph

## Redis

Redis는 key-value store NOSQL DB입니다. 싱글스레드로 동작하며 자료구조를 지원합니다. 그리고 다양한 용도로 사용될 수 있도록 다양한 기능을 지원합니다. 데이터의 스냅샷 혹은 AOF 로그를 통해 복구가 가능해서 어느정도 영속성도 보장됩니다.

## vs Memcached

Redis는 싱글 스레드 기반으로 동작하고, Memcached는 멀티스레드를 지원해서 멀티 프로세싱이 가능합니다.

Redis는 다양한 자료구조를 지원하고, Memcached는 문자열 형태로만 저장합니다.

Redis는 여러 용도로 사용할 수 있도록 다양한 기능을 지원합니다.

Redis는 스냅샷, AOF 로그를 통해서 데이터 복구가 가능합니다.

## Cap 이론, Eventual Consistency

CAP 이론은 분산 환경에서 모두를 만족하는 시스템은 없다는 이론입니다.

- Consitenty(일관성): ACID의 일관성과는 약간 다릅니다. 모든 노드가 같은 시간에 같은 데이터를 보여줘야 한다는 것입니다.
- Availability(가용성): 모든 동작에 대한 응답이 리턴되어야 합니다.
- Partition Tolerance(분할 내성): 시스템 일부가 네트워크에서 연결이 끊기더라도 동작해야 합니다.

CAP는 해당 시스템이 이거다 하고 말하기 곤란한게 어떻게 클러스터링 하느냐에 따라 달라질 수 있습니다. 그렇기 때문에 어떤 전략을 취할 때 어떤 것을 선택했는가를 잘 알아야 합니다. (단순히 MySQL이 CA입니다. 보다는 어떤 이유로 CA인지 근거를 생각해보기) 그리고 어느정도 한계가 있는 이론이고 PACELC 이론이라고 또 있습니다.

Eventual Consistency는 이 Consistency를 보장해주지 못하기 때문에 나온 개념으로, Consistency를 완전히 보장하지는 않지만, 결과적으로 언젠가는 Conssistency가 보장됨을 의미합니다.

## 자료구조

#### B 트리

[![tree](https://user-images.githubusercontent.com/38900338/105454677-9bf88400-5cc5-11eb-993e-fb6f7b9675a1.png)](https://user-images.githubusercontent.com/38900338/105454677-9bf88400-5cc5-11eb-993e-fb6f7b9675a1.png)

- 이진 트리를 확장해서, 더 많은 수의 자식을 가질 수 있게 일반화 시킨 자료구조
- 균형 트리: 루트 ~ 리프의 거리가 일정한 트리
- Branch 노드: Key와 Data 저장

#### B+ 트리

[![Bplustree](https://user-images.githubusercontent.com/38900338/105454222-d9104680-5cc4-11eb-96e9-31e46c0bf2aa.png)](https://user-images.githubusercontent.com/38900338/105454222-d9104680-5cc4-11eb-96e9-31e46c0bf2aa.png)

- B 트리를 확장해서, 데이터의 빠른 접근을 위한 인덱스 역할만 하는 비단말 노드(not Leaf)를 추가한 자료구조
- Branch 노드: Key만 저장, Leaf 노드: Key와 Data 저장 + Linked List로 연결(부등호를 사용한 순차 검색에 유용)
- B 트리보다 풀 스캔 빠름
- Leaf 노드를 제외하면 데이터를 저장하지 않아 더 많은 Key를 저장할 수 있음 -> 트리의 높이가 낮아져 Cache Hit 향상 가능

#### 해시 테이블

- 칼럼의 값으로 생성된 해시를 기반으로 인덱스 구현
- O(1)로 매우 빠름
- `인덱싱에선 부등호 연산 때문에 해시 테이블을 사용하면 성능이 떨어짐`
- `>=, Between, like, order by` 등은 불가능하지만 `==, in, is null` 등에서의 성능은 좋음

### 👉 Clustered Index vs Non Clustered Index

#### Clustered Index

- 인덱스로 지정한 컬럼을 기준으로 데이터를 `물리적으로 정렬`하여 사용하는 인덱스
- 테이블 구조에 영향을 미치는 인덱스
- 한 테이블에 `1개` 생성 가능
- `검색 속도는 빠르지만`, 데이터의 입력/수정/삭제는 느림

#### Non-Clustered Index

- 데이터의 위치를 알려주는 인덱스 페이지를 인덱스 컬럼 값을 기준으로 정렬하여 이용하는 인덱스
  - 리프 페이지에서 `컬럼 값 + 데이터의 포인터(데이터 페이지 번호, 오프셋)`로 주소를 찾아 검색
- 물리적으로 재배열 하지 않음
- 인덱스의 구조는 데이터 행과 독립적
- 한 테이블에 `여러 개` 생성 가능
- `검색 속도는 느리지만`, 데이터의 입력/수정/삭제는 빠름

## DB 클러스터링과 리플리케이션의 차이

|      | DB 클러스터링                                                                                                                                                                                                                 | 리플리케이션                                                                                                                                                                                                                   |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 대상 | DB 서버를 다중화                                                                                                                                                                                                              | DB 서버와 데이터를 같이 다중화                                                                                                                                                                                                 |
| 구조 | 수평적 구조 (Fail Over)                                                                                                                                                                                                       | 수직적 구조 (Master-Slave)                                                                                                                                                                                                     |
| 방식 | 동기 방식으로 동기화                                                                                                                                                                                                          | 비동기 방식으로 동기화                                                                                                                                                                                                         |
| 종류 | Active - Active, Active - Standby                                                                                                                                                                                             | 단순 백업, 부하 분산                                                                                                                                                                                                           |
| 장점 | 일관성, 1개의 서버가 고장나도 시스템은 계속 사용 가능                                                                                                                                                                         | 시간 지연 거의 없음                                                                                                                                                                                                            |
| 단점 | 동기화 시간 소요                                                                                                                                                                                                              | 일관성 없음, Master 오류시 복구 어려움                                                                                                                                                                                         |
| 구조 | [![clustering](https://user-images.githubusercontent.com/38900338/105463364-4b882300-5cd3-11eb-9837-195b872852e2.JPG)](https://user-images.githubusercontent.com/38900338/105463364-4b882300-5cd3-11eb-9837-195b872852e2.JPG) | [![replication](https://user-images.githubusercontent.com/38900338/105463420-5f338980-5cd3-11eb-8ea4-fe1bdc962385.JPG)](https://user-images.githubusercontent.com/38900338/105463420-5f338980-5cd3-11eb-8ea4-fe1bdc962385.JPG) |

## 관계형 데이터베이스(SQL)와 비관계형 데이터베이스(NoSQL)의 차이

| 관계형 데이터베이스                                                                                                  | 비관계형 데이터베이스                                                                                      |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| SQL 사용                                                                                                             | 다양한 질의어 사용                                                                                         |
| ACID                                                                                                                 | Eventual Consistency                                                                                       |
| 엄격한 스키마 아래 행과 열로 구성된 `테이블`들의 관계로 데이터 저장                                                  | 스키마가 없거나 느슨한 스키마로 데이터 저장                                                                |
| `속성(열)에 맞는 자료형에 따라` 데이터를 삽입                                                                        | `key-value`, `Document` 구조의 유연한 데이터 삽입 구조를 갖음                                              |
| 관계를 맺고 있는 데이터가 자주 변경되거나 테이블 안에서 읽어올 데이터가 불분명한 경우 또는 명확한 스키마가 있는 경우 | 데이터 구조를 알 수 없거나 테이블 안에서 읽어올 데이터가 분명한 경우 또는 변경 확장이 쉽게 되어야하는 경우 |
| 데이터의 정렬, 탐색, 분류가 빠름 데이터 무결성 보장                                                                  | 대용량 데이터 처리에 효율적 관계형 DB보다 쓰기와 읽기 성능이 좋음 유연하고 확장성 좋음                     |
| 기존의 스키마 수정 어려움, 빅데이터 처리에 비효율적                                                                  | 크기가 큰 Document에서는 성능 저하                                                                         |
| `Oracle`, `MySQL`                                                                                                    | 키-값: `Redis` 문서형(JSON, XML): `MongoDB`                                                                |

## Redis와 MongoDB

- Redis는 No SQL 방식을 사용하는 인메모리 데이터베이스로 `Key-Value` 형식으로 데이터를 저장하며 주로 캐쉬로 사용
- MongoDB는 NO SQL 방식을 사용하는 데이터베이스로 JSON같은 구조의 `Document` 형식으로 데이터를 저장하고 문서에 대한 ID를 키로 표현

## Redis의 데이터 휘발을 막기 위한 방법

- `snapshot` 기능을 통해 디스크에 백업하거나 `AOF(Append Only File)` 기능을 통해 `명령 쿼리를 저장`해두고 서버가 셧다운 되면 재실행
- snapshot: 특정 시점의 백업 및 복구에 유리, 빠르게 복구 가능, 서버가 다운되면 스냅샷 사이에 변경된 데이터 유실
- AOF: 모든 write/update 연산 자체를 모두 log 파일로 기록, 서버가 실행되면 순차적으로 연산을 재실행하여 데이터를 복구, write 속도 빠름, 데이터 유실X, 데이터 사용량이 큼, 서버 restart 시 속도 느림

## PostgresSQL과 ElasticSearch의 차이점

- PostgresSQL은 관계형 데이터베이스이고 ElasticSearch는 검색 및 분석엔진
- ES는 데이터 모델을 JSON으로 하고 있어 NoSQL처럼 사용할 수 있음

## 파티셔닝

### 정의

- `하나의 DB`에서 데이터를 물리적으로 분할하는 것
- 튜닝 기법: 데이터 용량 증가 시의 성능 향상, 관리 용이를 위해 진행

### 장점

- 관리 용이: 큰 테이블을 제거하여 관리가 쉬움
- 읽기/쓰기 성능 향상
- Insert 시에 분리된 파티션으로 분산시켜 경합을 줄임

### 단점

- 조인 비용 증가
- 테이블과 인덱스를 별도로 분리할 수 없고, 함께 분리해야 됨

### 분할 방법

#### 수평 분할 (Horizontal Partitioning)

- 하나의 DB안에 스키마가 같은 데이터를 두 개 이상의 테이블에 분할하여 저장
- 예시
  - 주민 테이블 -> a동 테이블, b동 테이블로 분리

#### 수직 분할 (Vertical) Partitioning)

- 테이블을 열을 기준으로 분리
- 정규화된 테이블을 분리하는 것

## 샤딩

### 정의

- `여러 DB`에 데이터를 물리적으로 `수평 분할 방식(Horizontal Partitioning)`으로 분산 저장/조회하는 것
- `트래픽 분산` 목적으로 사용: 데이터베이스에 데이터 증가 -> 용량 이슈, CRUD 성능 저하
- 애플리케이션 서버 레벨에서 구현하는 경우가 많았으나 최근에는 플랫폼 차원에서도 제공
  - Hibernate Shards, Spock Proxy(MySQL Proxy 기반), Gizzard(Twitter), Spider(MariaDB 기본 내장)
- 예시
  - 주민 테이블 -> a동 테이블은 A DB, b동 테이블은 B DB에 저장

### 장점

- 쓰기 성능 향상 (읽기 성능 동일)

### 단점

- 두 개 이상의 샤드에서 `JOIN 불가`
- 일관성과 복제에서 불리
- auto increment 등은 샤드 별로 달라질 수 있고, last_insert_id() 값은 유효하지 않음

## 레플리카

### 정의

- `동일한 데이터를 Master/Slave DB로 나누어 저장`하는 것 (이중화)
- 목적
  - `읽기(Select) 성능을 향상`하기 위한 방법
  - 읽기와 쓰기 DB를 분리하여 성능을 향상시킴
  - Fail Over 방지: 메인 DB에 문제가 생겨도 서브 DB로 해결

## Mysql vs PostgreSQL

- 테이블의 집합이라는 의미로 MySQL은 database, PostgreSQL은 schema가 사용된다.
  - postgres는 db기준으로 접속을 하고, schema를 지정하지 않으면 public 기본 사용
  -

### 데이터베이스 풀

- Connection Pool
  - 클라이언트의 요청에 따라 각 어플리케이션의 스레드에서 데이터베이스에 접근하기 위해서는 Connection이 필요하다.
  - Connection pool은 이런 Connection을 여러 개 생성해 두어 저장해 놓은 **공간(캐시)**, 또는 이 공간의 Connection을 필요할 때 꺼내 쓰고 반환하는 **기법**을 말한다.
    [![img](https://github.com/WeareSoft/tech-interview/raw/master/contents/images/db-img/db-connection-02.png)](https://github.com/WeareSoft/tech-interview/blob/master/contents/images/db-img/db-connection-02.png)
- DB에 접근하는 단계
  1. 웹 컨테이너가 실행되면서 DB와 연결된 Connection 객체들을 미리 생성하여 pool에 저장한다.
  2. DB에 요청 시, pool에서 Connection 객체를 가져와 DB에 접근한다.
  3. 처리가 끝나면 다시 pool에 반환한다. [![img](https://github.com/WeareSoft/tech-interview/raw/master/contents/images/db-img/db-connection-01.jpeg)](https://github.com/WeareSoft/tech-interview/blob/master/contents/images/db-img/db-connection-01.jpeg)
- Connction이 부족하면?
  - 모든 요청이 DB에 접근하고 있고 남은 Conncetion이 없다면, 해당 클라이언트는 대기 상태로 전환시키고 Pool에 Connection이 반환되면 대기 상태에 있는 클라이언트에게 순차적으로 제공된다.
- 왜 사용할까?
  - 매 연결마다 Connection 객체를 생성하고 소멸시키는 비용을 줄일 수 있다.
  - 미리 생성된 Connection 객체를 사용하기 때문에, DB 접근 시간이 단축된다.
  - DB에 접근하는 Connection의 수를 제한하여, 메모리와 DB에 걸리는 부하를 조정할 수 있다.
- Thread Pool
  - 비슷한 맥락으로 Thread pool이라는 개념도 있다.
  - 이 역시 매 요청마다 요청을 처리할 Thread를 만드는것이 아닌, 미리 생성한 pool 내의 Thread를 소멸시키지 않고 재사용하여 효율적으로 자원을 활용하는 기법.
- Thread Pool과 Connection pool
  - WAS에서 Thread pool과 Connection pool내의 Thread와 Connection의 수는 직접적으로 메모리와 관련이 있기 때문에, 많이 사용하면 할 수록 메모리를 많이 점유하게 된다. 그렇다고 반대로 메모리를 위해 적게 지정한다면, 서버에서는 많은 요청을 처리하지 못하고 대기 할 수 밖에 없다.
  - 보통 WAS의 Thread의 수가 Conncetion의 수보다 많은 것이 좋은데, 그 이유는 모든 요청이 DB에 접근하는 작업이 아니기 때문이다.

#### B+tree 알고리즘

[![img](https://github.com/WeareSoft/tech-interview/raw/master/contents/images/db-btree.png)](https://github.com/WeareSoft/tech-interview/blob/master/contents/images/db-btree.png)

- 실제 데이터가 저장된 리프노드(Leaf nodes)
- 리프노드까지의 경로 역할을 하는 논리프노드(Non-leaf nodes)
- 경로의 출발점이 되는 루트 노드(Root node)

B+tree는 리프노드에 이르기까지에 대한 자식 노드에 포인터가 저장되어 있다. 즉, B+트리의 검색은 루트노드에서 어떤 리프 노드에 이르는 한 개의 경로만 검색하면 되므로 매우 효율적이다.

##### B+tree 사용 이유

- 왜 index 생성 시 b-tree를 사용하는지? hash table이 더 효율적이지 않은지?
  - SELECT 질의 조건에는 부등호 연산(<>)도 포함
  - hash table은 동등 연산에 특화된 자료구조이기 때문에 부등호 연산 사용 시 문제 발생

#### 주의할 점

- 인덱스는 따로 테이블의 형태로 관리가 된다. 자원을 소모한다는 의미. 때문에 무분별한 인덱스의 사용은 성능에 부정적인 영향을 미칠 수 있다.
- 또한 인덱스는 이진트리를 사용하기 때문에 기본적으로 정렬되어 있다. 이로인해 검색과 조회의 속도를 향상시킬 수 있지만 잦은 데이터의 변경(삽입, 수정 삭제)가 된다면 인덱스 데이블을 변경과 정렬에 드는 오버헤드 때문에 오히려 성능 저하가 일어날 수 있다.
  - INSERT : 테이블에는 입력 순서대로 저장되지만, 인덱스 테이블에는 정렬하여 저장하기 때문에 성능 저하 발생
  - DELETE : 테이블에서만 삭제되고 인덱스 테이블에는 남아있어 쿼리 수행 속도 저하
  - UPDATE : 인덱스에는 UPDATE가 없기 때문에 DELETE, INSERT 두 작업 수행하여 부하 발생
- 데이터의 중복이 높은 컬럼(카디널리티가 낮은 컬럼)은 인덱스로 만들어도 무용지물 (예: 성별)
- 다중 컬럼 인덱싱할 때 카디널리티가 높은 컬럼->낮은 컬럼 순으로 인덱싱해야 효율적

- [victolee - [DB이론\] 인덱스(Index)](https://victorydntmd.tistory.com/319)
- [Nathan - DB 성능을 위한 Index](https://brunch.co.kr/@skeks463/25)
- [인덱스 기본 원리](http://wiki.gurubee.net/pages/viewpage.action?pageId=26745270)



### 파티셔닝

- 배경

  - 서비스의 크기가 점점 커지고 DB에 저장하는 데이터의 규모 또한 대용량화 되면서, 기존에 사용하는 DB 시스템의 **용량(storage)의 한계와 성능(performance)의 저하** 를 가져오게 되었다.
  - 즉, VLDB(Very Large DBMS)와 같이 하나의 DBMS에 너무 큰 table이 들어가면서 용량과 성능 측면에서 많은 이슈가 발생하게 되었고, 이런 이슈를 해결하기 위한 방법으로 table을 '파티션(partition)'이라는 작은 단위로 나누어 관리하는 **'파티셔닝(Partitioning)'기법** 이 나타나게 되었다.

- 파티셔닝의 개념

  - 큰 table이나 index를, 관리하기 쉬운 partition이라는 작은 단위로 물리적으로 분할하는 것을 의미한다.
    - 물리적인 데이터 분할이 있더라도, DB에 접근하는 application의 입장에서는 이를 인식하지 못한다.
  - '파티셔닝(Partitioning)'기법을 통해 소프트웨어적으로 데이터베이스를 분산 처리하여 성능이 저하되는 것을 방지하고 관리를 보다 수월하게 할 수 있게 되었다.

- 파티셔닝의 목적

  1. 성능(Performance)
     - 특정 DML과 Query의 성능을 향상시킨다.
     - 주로 대용량 Data WRITE 환경에서 효율적이다.
     - 특히, Full Scan에서 데이터 Access의 범위를 줄여 성능 향상을 가져온다.
     - 많은 INSERT가 있는 OLTP 시스템에서 INSERT 작업을 작은 단위인 partition들로 분산시켜 경합을 줄인다.
  2. 가용성(Availability)
     - 물리적인 파티셔닝으로 인해 전체 데이터의 훼손 가능성이 줄어들고 데이터 가용성이 향상된다.
     - 각 분할 영역(partition별로)을 독립적으로 백업하고 복구할 수 있다.
     - table의 partition 단위로 Disk I/O을 분산하여 경합을 줄이기 때문에 UPDATE 성능을 향상시킨다.
  3. 관리용이성(Manageability)
     - 큰 table들을 제거하여 관리를 쉽게 해준다.

- 파티셔닝의 장점

  - 관리적 측면 : partition 단위 백업, 추가, 삭제, 변경
    - 전체 데이터를 손실할 가능성이 줄어들어 데이터 가용성이 향상된다.
    - partition별로 백업 및 복구가 가능하다.
    - partition 단위로 I/O 분산이 가능하여 UPDATE 성능을 향상시킨다.
  - 성능적 측면 : partition 단위 조회 및 DML수행
    - 데이터 전체 검색 시 필요한 부분만 탐색해 성능이 증가한다.
    - 즉, Full Scan에서 데이터 Access의 범위를 줄여 성능 향상을 가져온다.
    - 필요한 데이터만 빠르게 조회할 수 있기 때문에 쿼리 자체가 가볍다.

- 파티셔닝의 단점

  - table간 JOIN에 대한 비용이 증가한다.
  - table과 index를 별도로 파티셔닝할 수 없다.
    - table과 index를 같이 파티셔닝해야 한다.

- 파티셔닝의 종류

  1. 수평(horizontal) 파티셔닝
     - **샤딩(Sharding)** 과 동일한 개념
  2. 수직(vertical) 파티셔닝

  ![img](https://github.com/WeareSoft/tech-interview/raw/master/contents/images/types-of-partitioning.png)

- 파티셔닝의 분할 기준

  1. 범위 분할 (range partitioning)
  2. 목록 분할 (list partitioning)
  3. 해시 분할 (hash partitioning)
  4. 합성 분할 (composite partitioning)

  ![img](https://github.com/WeareSoft/tech-interview/raw/master/contents/images/partitioning.png)

> ⏫[Top](https://github.com/WeareSoft/tech-interview/blob/master/contents/db.md#4-database) ↩️[Back](https://github.com/WeareSoft/tech-interview#4-database) ℹ️[Home](https://github.com/WeareSoft/tech-interview#tech-interview)
>
> - https://gmlwjd9405.github.io/2018/09/24/db-partitioning.html
> - https://nesoy.github.io/articles/2018-02/Database-Partitioning

### 샤딩

> ⏫[Top](https://github.com/WeareSoft/tech-interview/blob/master/contents/db.md#4-database) ↩️[Back](https://github.com/WeareSoft/tech-interview#4-database) ℹ️[Home](https://github.com/WeareSoft/tech-interview#tech-interview)
>
> - http://mongodb.citsoft.net/?page_id=225#comment-91922
> - https://d2.naver.com/helloworld/14822
> - http://tech.kakao.com/2016/07/01/adt-mysql-shard-rebalancing/



https://github.com/gyoogle/tech-interview-for-developer/tree/master/Computer%20Science/Database

https://github.com/WooVictory/Ready-For-Tech-Interview/tree/master/Database

https://github.com/JaeYeopHan/Interview_Question_for_Beginner/tree/master/Database#%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4

https://github.com/KNU-CS-Study/Tech-Interview/blob/master/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/DB-intro/README.md

https://github.com/WeareSoft/tech-interview/blob/master/contents/db.md#%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%ED%92%80

~~https://github.com/huisam/interview/tree/main/DataBase#database~~

~~https://github.com/brave-people/brave-tech-interview/blob/main/contents/database.md~~

~~https://github.com/yoonje/developer-interview-questions-and-answers/blob/master/Database/README.md#dbms~~

~~https://github.com/ksundong/backend-interview-question#%EB%A9%B4%EC%A0%91-%EC%A0%84-%EC%A0%95%EB%B3%B4~~

https://kadamon.tistory.com/21

https://velog.io/@matisse/%EA%B8%B0%EC%88%A0-%EB%A9%B4%EC%A0%91-%EC%A7%88%EB%AC%B8-%EC%A0%95%EB%A6%AC
