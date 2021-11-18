---
title: "[JS] 클로저 Closure - 2"
date: "2021-04-02"
tags: ["js"]
cover: "./logo.png"
---

## 반복문 클로저


ECMAScript 2015의  let 키워드 소개 전에는 클로저와 관련된 일반적인 문제는 루프 안에서 클로저가 생성되었을 때 발생한다.

```js
<p id="help">Helpful notes will appear here</p>
<p>E-mail: <input type="text" id="email" name="email"></p>
<p>Name: <input type="text" id="name" name="name"></p>
<p>Age: <input type="text" id="age" name="age"></p>
function showHelp(help) {
  document.getElementById('help').innerHTML = help;
}

function setupHelp() {
  var helpText = [
      {'id': 'email', 'help': 'Your e-mail address'},
      {'id': 'name', 'help': 'Your full name'},
      {'id': 'age', 'help': 'Your age (you must be over 16)'}
    ];

  for (var i = 0; i < helpText.length; i++) {
    var item = helpText[i];
    document.getElementById(item.id).onfocus = function() {
      showHelp(item.help);
    }
  }
}

setupHelp();
```

어떤 필드에 포커스를 주더라도 나이에 관한 도움말이 표시된다.

onfocus 이벤트에 연결된 함수가 클로저이기 때문

이 클로저는 함수 정의와 setupHelp 함수 범위에서 캡처된 환경으로 구성된다.

루프에서 세 개의 클로저가 만들어졌지만 각 클로저는 값이 변하는 변수가 (item.help) 있는 같은 단일 환경을 공유

onfocus 콜백이 실행될 때 콜백의 환경에서 item 변수는 (세개의 클로저가 공유한다) helpText 리스트의 마지막 요소를 가리키고 있음



함수 팩토리를 사용해서 해결

```js
function showHelp(help) {
  document.getElementById('help').innerHTML = help;
}

function makeHelpCallback(help) {
  return function() {
    showHelp(help);
  };
}

function setupHelp() {
  var helpText = [
      {'id': 'email', 'help': 'Your e-mail address'},
      {'id': 'name', 'help': 'Your full name'},
      {'id': 'age', 'help': 'Your age (you must be over 16)'}
    ];

  for (var i = 0; i < helpText.length; i++) {
    var item = helpText[i];
    document.getElementById(item.id).onfocus = makeHelpCallback(item.help);
  }
}

setupHelp();
```

단일 환경을 공유하는 콜백대신, `makeHelpCallback` 함수는 각각의 콜백에 새로운 lexical environment을 생성한다.



익명 클로저를 사용

```js
function showHelp(help) {
  document.getElementById('help').innerHTML = help;
}

function setupHelp() {
  var helpText = [
      {'id': 'email', 'help': 'Your e-mail address'},
      {'id': 'name', 'help': 'Your full name'},
      {'id': 'age', 'help': 'Your age (you must be over 16)'}
    ];

  for (var i = 0; i < helpText.length; i++) {
    (function() {
       var item = helpText[i];
       document.getElementById(item.id).onfocus = function() {
         showHelp(item.help);
       }
    })(); // Immediate event listener attachment with the current value of item (preserved until iteration).
  }
}

setupHelp();
```

ES2015의 `let` 키워드를 사용 가능

```js
function showHelp(help) {
  document.getElementById('help').innerHTML = help;
}

function setupHelp() {
  var helpText = [
      {'id': 'email', 'help': 'Your e-mail address'},
      {'id': 'name', 'help': 'Your full name'},
      {'id': 'age', 'help': 'Your age (you must be over 16)'}
    ];

  for (var i = 0; i < helpText.length; i++) {
    let item = helpText[i];
    document.getElementById(item.id).onfocus = function() {
      showHelp(item.help);
    }
  }
}

setupHelp();
```

위의 경우 var 대신 let을 사용하여 모든 클로저가 블록 범위 변수를 바인딩할 것이므로 추가적인 클로저를 사용하지 않아도 완벽하게 동작



```javascript
var i;
for (i = 0; i < 10; i++) {
  setTimeout(function() {
    console.log(i);
  }, 100);
}
```

10이 10번 출력됨,

 `setTimeout()`에 인자로 넘긴 익명함수는 모두 0.1초 뒤에 호출된다.  0.1초 동안에 이미 반복문이 모두 순회되면서 `i`값은 이미 10이 된 상태. 그 때 익명함수가 호출되면서 이미 10이 되어버린 `i`를 참조한다.

```javascript
var i;
for (i = 0; i < 10; i++) {
  (function(j) {
    setTimeout(function() {
      console.log(j);
    }, 100);
  })(i);
}
```

이 코드에서 `i`는 iife 내에 `j`라는 형태로 주입, 클로저에 의해 각기 다른 환경속에 포함

10개의 환경이 생길 것이고, 10개의 서로 다른 환경에 10개의 서로 다른 j가 생김

## 성능

클로저가 필요하지 않는데 불필요하게 사용하는 것은 메모리, 처리속도에서 낭비

```js
function MyObject(name, message) {
  this.name = name.toString();
  this.message = message.toString();
  this.getName = function() {
    return this.name;
  };

  this.getMessage = function() {
    return this.message;
  };
}
```

앞의 코드는 클로저의 이점을 이용하지 않음으로 다음과 같이 다시 쓸 수 있다.

```js
function MyObject(name, message) {
  this.name = name.toString();
  this.message = message.toString();
}
MyObject.prototype = {
  getName: function() {
    return this.name;
  },
  getMessage: function() {
    return this.message;
  }
};
```

그러나 프로토타입을 다시 정의하는 것은 권장되지 않음으로 기존 프로토타입에 추가하는 다음 예제가 더 좋다.

```js
function MyObject(name, message) {
  this.name = name.toString();
  this.message = message.toString();
}
MyObject.prototype.getName = function() {
  return this.name;
};
MyObject.prototype.getMessage = function() {
  return this.message;
};
```

위의 코드는 같은 결과를 가진 더 깨끗한 방법으로 작성할 수도 있다:

```js
function MyObject(name, message) {
    this.name = name.toString();
    this.message = message.toString();
}
(function() {
    this.getName = function() {
        return this.name;
    };
    this.getMessage = function() {
        return this.message;
    };
}).call(MyObject.prototype);
```



## 

http://meetup.toast.com/posts/86
http://meetup.toast.com/posts/90
http://unikys.tistory.com/309
https://opentutorials.org/course/743/6544
https://developer.mozilla.org/ko/docs/Web/JavaScript/Closures
http://blog.javarouka.me/2012/01/closure.html