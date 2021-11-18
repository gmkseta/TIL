---
title: "[JS] 클로저 Closure - 1"
date: "2021-04-01"
tags: ["js"]
cover: "./logo.png"
---

## 내부함수

함수 안에서 또다른 함수를 선언할 수 있으며, 내부함수(hello)에서 외부함수(world)의 지역변수에 접근 할 수 있다.

```js
function world(){
  var text = "hello world";
  function hello(){
    console.log(text)
  }
  hello();
}

world()
```

* `world`는 지역변수 `text`와 함수 `hello`를 정의한다.
* `hello` 는 내부함수이며, `world` 안에서만 사용 할 수 있다.
* `hello` 안에서 외부함수의 `text`변수에 접근이 가능하고, 만약 hello 안에 `text` 라는 변수가 있었으면 `text` 가 아닌  `this.text`로 사용 가능하다.

## 클로저(Closure)

```javascript
function world(){
  var text = "hello world";
  function hello(){
    console.log(text)
  }
  return hello();
}
var helloWorld = world()
helloWorld()
```

* 이전 예제와 동일한 결과이지만 `hello` 함수가 실행 되기 전 , `world` 함수에서 리턴되어 `helloWorld` 변수에 저장이 된다.
* 몇몇 프로그래밍 언어에서 함수 안의 지역변수들은 그 함수가 처리되는 동안에만 존재 하는 것으로 우린 배웠다. 함수 실행이 끝나면 소멸된다.
* 하지만 자바스크립트에서는 달리 함수를 리턴하고 그 리턴하는 함수는 클로저를 만들어준다.
* 클로저가 생성된 시점의 유효범위(scope) 내에 있는 모든 지역변수로 구성된다.

( mdn 에서의 예제 )

```javascript
function makeAdder(x) {
  var y = 1;
  return function(z) {
    y = 100;
    return x + y + z;
  };
}

var add5 = makeAdder(5);
var add10 = makeAdder(10);
//클로저에 x와 y의 환경이 저장됨

console.log(add5(2));  // 107 (x:5 + y:100 + z:2)
console.log(add10(2)); // 112 (x:10 + y:100 + z:2)
//함수 실행 시 클로저에 저장된 x, y값에 접근하여 값을 계산
```

* 인자 x를 받아서 함수를 리턴하고 반환되는 함수는 z를 받아와서 x+z+y를 반환한다.
* 리턴된 함수들은 모두 클로저이며 ( `add5, add10`)
* 이 둘은 함수의 코드를 공유하지만 서로 다른 맥락(어휘)적 환경을 저장한다. 
* 내부함수에서 y에 접근하여 100을 대입하였고, 이는 클로저가 리턴 된 후에도 외부 함수의 변수들에 접근이 가능하다는 뜻
* 클로저에 단순 값 형태로 전달되는 것이 아니다.

## Private method 흉내

javascript에서 객체지향프로그래밍을 한다고 하면 prototype을 통해 객체를 다루곤한다..

```javascript
function Counter(){
  this._counter = 0;
}
Counter.prototype.increment = function(){
  this._counter += 1;
}
Counter.prototype.decrement = function(){
  this._counter -= 1;
}
Counter.prototype.value = function(){
	return this._counter
}
var counter = new Counter();
counter.increment()
counter.increment()
console.log(counter.value) // 2
counter.decrement()
console.log(counter.vlaue) // 1
counter._counter = 10
console.log(counter.vlaue) // 10
```

다음과같이 `_counter` 를 private variable 로 쓰고싶었지만 외부에서 접근이 가능하며 변경또한 쉽게 되어버린다.

MDN의 예시

```javascript
var makeCounter = function() {
  var privateCounter = 0;
  function changeBy(val) {
    privateCounter += val;
  }
  return {
    increment: function() {
      changeBy(1);
    },
    decrement: function() {
      changeBy(-1);
    },
    value: function() {
      return privateCounter;
    }
  }
};

var counter1 = makeCounter();
var counter2 = makeCounter();
alert(counter1.value()); /* 0 */
counter1.increment();
counter1.increment();
alert(counter1.value()); /* 2 */
counter1.decrement();
alert(counter1.value()); /* 1 */
alert(counter2.value()); /* 0 */
```

* 자바스크립트에서 위와같이 private method를 흉내내는 것이 가능하다.
* 코드에 제한적인 접근만을 허용하고, 불필요한 메서드가 공용 인터페이스를 혼란스럽지 않도록 만든다.
* 클로저들이 `counter.increment` `counter.decrement` `counter.value` 가 공유하는 어휘적 환경을 만든다
* 각 클로저는 고유한 privateCounter 변수를 참조하며, 서로 영향을 주지 않는다.



계속..

References



http://meetup.toast.com/posts/86
http://meetup.toast.com/posts/90
http://unikys.tistory.com/309
https://opentutorials.org/course/743/6544
https://developer.mozilla.org/ko/docs/Web/JavaScript/Closures
http://blog.javarouka.me/2012/01/closure.html