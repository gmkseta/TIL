---
title: "선언형 vs 명령형 프로그래밍"
date: "2021-03-31"
tags: ["cs", "js", "fp"]
cover: "./logo.png"
---

명령형 프로그래밍과 선언형 프로그래밍에 관해 제대로 알고있지 않은 것 같아 정리한다.

## Imperative vs Declarative

먼저 빠르게 명령형과 선언형에 관해서 비교를 해보자면

- 식당에 안내데스크에서,
  - 명령형 방식 : 저쪽 테이블이 비어 있는 게 보이는데요. 제 남편과 저는 저쪽으로 걸어가서 앉을 거예요.
  - 선언형 방식 : 2명 자리 부탁드립니다.
- 집을 물어볼 때
  - 명령형 방식 : 신사역에서 내려서 M번출구로 쭉 직진하다가 3블록 뒤에 오른쪽골목으로 빠져서 미용실쪽에서 오른쪽으로 돌면 한의원 맞은편이야.
  - 선언형 방식 : 내 주소는 서울 특별시 강남구 논현동 10-13 이야 .

## 명령형 프로그래밍

- 무엇을 어떻게 ( How ) 할것 인가에 대해 서술한다.
- 알고리즘을 명시하고 목표를 명시하지 않음
- 프로그래밍의 상태와 상태를 변경시키는 구문의 관점에서 연산을 설명하는 패러다임, 수행할 명령들을 순서대로 써 놓은 것이다.
- 앨런 튜링의 튜링머신
- 절차적 / 객체 지향적 프로그래밍

## 선언형 프로그래밍

- 프로그램이 명령의 수행이 아닌 **함수의 계산**이라는 시각으로 "how" 가 아닌 '**what**' 에 초점을 맞춘다.
- 선언형 프로그래밍이란 알고리즘을 명시하지 않고 목표만을 명시한다.
- 람다 대수
- 함수형 프로그래밍

#### 선언적 접근 방식에는 명령적 추상화 계층이 있다.

- 식당의 안내 데스크 직원은 우리를 테이블로 안내하기위한 모든 단계를 알고있다고 가정하는것이다.
- 주소를 알면 위치를 알 수 있다는 가정을 하는 것이다.

많은 선언적 접근 방식에서는 근본적으로 명령적 추상화를 가지고 있다.

## 명령형 언어? 선언형 언어?

- 명령형 언어라고 해서 선언형 프로그래밍이 불가능 한 것은 아니다.

---

참조

https://ui.dev/imperative-vs-declarative-programming/
https://en.wikipedia.org/wiki/Church_encoding
https://nesoy.github.io/articles/2018-05/Functional-Programming
https://ko.wikipedia.org/wiki/%ED%95%A8%EC%88%98%ED%98%95_%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D
https://medium.com/@alexnault/functional-programming-with-javascript-in-3-tips-f282934947e5
https://sungjk.github.io/2017/07/17/fp.html
https://easywritten.org/post/real-advantages-of-functional-programming/
https://ko.wikipedia.org/wiki/%EB%AA%85%EB%A0%B9%ED%98%95_%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D
https://madplay.github.io/post/functional-programming-object-oriented-programming
https://boxfoxs.tistory.com/430
https://www.hanbit.co.kr/media/channel/view.html?cms_code=CMS4313717600
https://codechaser.tistory.com/81
https://evan-moon.github.io/2019/12/15/about-functional-thinking/
