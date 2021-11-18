---
title: "[TypeScript] 변수, 타입"
date: "2021-04-04"
tags: ["ts", 'js']
cover: "./typescript.jpeg"

---

`var` 는 함수단위의 유효범위를 갖는다.

`const, let` 은 블록단위의 유효범위를 갖는다.

```js
if(true){
  var a = 1
}
console.log(a)

if(true){
  let b = 1
}
console.log(b) // err

for(var i = 0; i < 3; i++){
  setTimeout(function(){
    console.log(i);
  }, 300)
}
for(let i = 0; i < 3; i++){
  setTimeout(function(){
    console.log(i);
  }, 300)
}
```



### Type

* number
* string
* boolean
* undefined
* null
* object
* syumbol
* any

모든 타입의 상위는 any, 하위로는 null/undefined

즉 any 은 string / number ... 등이 될 수 있고,  string, number...  은 null , undefined가 될 수 있음

```js
let a: string;
a = null;
a = undefined;
let b: null;
b = 'a'; // X
```



```js
let objectValue: object;
objectValue = new String(22)// String(22) X
let strArr: string[];
strArr = ['1', '2'];


//선언과 동시에 초기화 시 알아서 타입 추론해서 넣음
let a = "aa"


//inline type definition
let obj: { property: string };


let tuple2: [number, string];
tuple2 = [1,2]// X
tuple2 = [1, "a"]// 0
```









