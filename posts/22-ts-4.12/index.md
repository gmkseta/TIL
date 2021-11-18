---
title: "[TypeScript] Index Type"
date: "2021-04-12"
tags: ["ts", 'js']
cover: "./typescript.jpeg"
---

```tsx
interface Props {
  [key: string]: string;
  name: string;
}
//인덱스 시그니쳐 매개 변수 형식은 string or Number
const p: Props = {
  name: 'a',
  a: 'd',
  b: 'e',
  // c: 3
}
let keys: keyof Props;

interface User {
  name: string;
  age: number;
  hello(msg: string): void;
}

let keysOfUser: keyof User;

keysOfUser = "name";

let helloMethod: User['hello'];
// helloMethod = function(msg: number){
// }
helloMethod = function(msg: string){

}



```

keyof  키워드  