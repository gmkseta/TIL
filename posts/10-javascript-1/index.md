---
title: "함수형 프로그래밍(Functional Programming)"
date: "2021-03-30"
tags: ["cs", "js", "fp"]
cover: "./logo.jpg"
---

주 언어가 python , c++ 이라고 하며 살았지만, 어느새 js, ruby만 하고있어서

제대로된 공부의 필요성을 느낀다.

공부하다보니 함수형 프로그래밍에 대해 대학시절 시험을 위해 공부했었지만, 제대로 알긴하는지 기억도 못하던 차 공부겸 기록

짧은 지식이다보니 늘 그렇듯 장황하게 글을 쓸수없고 키워드에대한 기록이 전부인거같다.

---

대학교 시절 프로그래밍을 배울 때 **절차지향 프로그래밍** 과 **객체지향 프로그래밍** 에 대해서는 배우지만

함수형 프로그래밍을 가르치지는 않는 것 같다. 요즘은 자바스크립트 때문에 많이들 개인적으로 공부 하는 것 같지만...

난 학창시절에 Go , Erlang 을 접하면서 함수형 언어와 함께 처음 알게되었던것같다.

## 함수형 프로그래밍(FP) 이란?

함수형 프로그래밍을 논할 때 lambda calculus 를 빼놓고 말하기는 어렵다.

함수형 프로그래밍의 개념들의 많은 부분이 Alonzo Church 의 LambdaCalculus( 람다 대수 )에서 가져왔는데

객체지향 프로그래밍이 객체라는 기본 단위로 이들의 상호작용을 서술하는 방식이라면

프로그래밍을 수학으로써 풀어서 서술하는 방식이며, 함수의 응용을 강조한다고 생각하면 된다.

![church_encoding](https://wikimedia.org/api/rest_v1/media/math/render/svg/4234d6babd69a13a183ee913a1efd0c3264da618)

### 함수형 프로그래밍은 선언형 프로그래밍이다.

객체, 절차 지향 프로그래밍은 명령형 프로그래밍이고 함수형 프로그래밍은 선언형 프로그래밍이다.

#### [선언형이란 ?](/11-cs)

### 함수형 프로그래밍에 필요한 개념

- First Class Object
  - Argument 로 전달 할 수 있다
  - 함수의 리턴값이 될 수 있다
  - 값을 수정하거나 할당 할 수 있다.
- High-Order Function
  - 함수를 Argument 로 받는 함수
  - 함수를 리턴하는 함수
- Immutability
  - 데이터가 변할 수 없다, 불변성 데이터
  - 데이터 변경이 필요한 경우 원본 데이터 구조를 변경하지 않고 그 데이터의 복사본을 만들어 작업을 진행한다.
- Pure Function
  - side effect 없이 함수의 실행이 외부에 영향을 끼치지 않는다.
- Function composition
- Currying
  - 여러 인자가 있는 함수를 하나의 인자를 갖는 함수로 분리시키는 것

### 그래서 어떻게 하나 ?

순수 함수를 작성하고, 상태와 데이터가 변하는 것을 피하면서 프로그래밍 하는것, 변경 가능한 데이터 및 부작용을 피하여 소프르웨어를 서술한다.

대입문(assignment statements) 없이 프로그래밍 한다

- 모든 데이터는 변경이 불가능 해야한다.
- 함수는 순수 함수로 만든다 인자를 받고 데이터나 다른 함수를 반환해야한다.
- 루프 보다는 재귀

### 왜 함수형 프로그래밍을 하나 ?

- 함수형 코드는 명령형 / 객체지향 코드보다 간결하고 예측이 쉽다.
- 동시성 측면에서 우리가 기존에 세마포어나 뮤텍스를 사용해서 여러 프로세스가 동시에 한 메모리를 참조하고 변경하는 경우를 방지했는데, 함수형 프로그래밍은 더 이상 이러한 기술을 사용하지 않아도 병렬처리를 안전하게 할 수 있다.
- 불변성을 지향하기 때문에 프로그램 동작의 예측이 쉬워져서 아닐까 한다.
- 함수 단위의 코드 재사용이 쉽다.

### 왜 여태 뜨지 못했나?

- 코드가 간결하다고 하지만 그런 간결한 코드를 읽기 위해서는 학습이 필요하다.
- 우리가 배워온건 객체지향적인 프로그래밍 방식이다, 즉 함수형 적으로 사고하지 못한다면 쉽지않다.


글 쓰다보니 이외 다른 배경지식들에 대한 글을 써야할 필요성을 느낀다,

명령형 프로그래밍 - 튜링머신

선언형 프로그래밍 -

---

참조

https://evan-moon.github.io/2019/12/15/about-functional-thinking/

https://en.wikipedia.org/wiki/Church_encoding

https://nesoy.github.io/articles/2018-05/Functional-Programming

https://ko.wikipedia.org/wiki/%ED%95%A8%EC%88%98%ED%98%95_%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D

https://medium.com/@alexnault/functional-programming-with-javascript-in-3-tips-f282934947e5

https://sungjk.github.io/2017/07/17/fp.html

https://easywritten.org/post/real-advantages-of-functional-programming/

https://ui.dev/imperative-vs-declarative-programming/

https://medium.com/korbit-engineering/%ED%95%A8%EC%88%98%ED%98%95-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%EC%9D%B4%EB%9E%80-e7f7b052411f

https://nesoy.github.io/articles/2018-05/Functional-Programming

https://velog.io/@kyusung/%ED%95%A8%EC%88%98%ED%98%95-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%9A%94%EC%95%BD

https://uzihoon.com/post/4de52810-5201-11ea-a189-4bd78d8bfce2

https://blog.ull.im/engineering/2019/04/07/functional-programming-with-javascript-in-3-steps.html
