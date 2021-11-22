---
title: "ActiveRecord"
date: "2021-11-08"
---

# ActiveRecord 패턴

<img src="https://user-images.githubusercontent.com/72075148/141689387-5704430d-cf75-4b41-bce6-66829b283cba.jpg" alt="IMG_0255" style="zoom: 33%;" />

- 데이터베이스의 데이터를 접근하는 방법
- 테이블 혹은 뷰는 클래스에 Wrapping되어있음
- 일반적으로 ORM에서 사용됨
- 리펙토링으로 유명한 **마틴 파울러**가 **PofEAA**에서 명명
- **DTO** 의 특수한 형태
- **DTO** 처럼 퍼블릭 변수와, getter, setter을 제공하지만 save나 find 같은 메서드도 제공한다.

> Unfortunately we often find that developers try to treat these data structures as though they were objects by putting business rule methods in them. This is awkward because it creates a hybrid between a data structure and an object. - CleanCode
>
> 안타깜게도 개발자들은 이러한 데이터 구조를 마치 객체인 것 처럼 취급하여 비즈니스 규칙 메서드를 넣어둔다. 데이터 구조와 객체가 짬뽕 되기 때문에 어색하다.

## Rails에서의 ActiveRecord

- 기본적인 사용법은 쉽고 널렸으니 패쓰.
-

https://karoldabrowski.com/blog/active-record-pattern-or-anti-pattern-overview/

https://karoldabrowski.com/blog/active-record-pattern-or-anti-pattern-overview/

https://juzer-shakir.medium.com/rails-active-record-basics-32852cc1b2b9

https://charcodes24.medium.com/ruby-object-inheritance-and-the-power-of-activerecord-628c3cd21fcb

https://en.wikipedia.org/wiki/Active_record_pattern

https://www.sitepoint.com/community/t/dao-vs-orm-vs-activerecord-vs-tablegateway-vs-ahhhh/2473/20

https://darrengwon.tistory.com/930
