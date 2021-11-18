---
title: "[TypeScript] Class"
date: "2021-04-07"
tags: ["ts", 'js']
cover: "./typescript.jpeg"
---

ts에서는 접근 제한자가 있음 - `private` - 함수에서도 쓰는듯, 아무것도 안쓰면 기본이 퍼블릭임, protected

```typescript
interface User{
  
}
interface Bag{
  
}
class Car {
	wheel: Wheel;
	private gas: number;
  private store: object;
  constructor(wheel: Wheel){
    this.wheel = wheel;
    this.store = {};
  }
  put(id: string, bag: Bag){
    this.store[id] = bag;
  }
  get(id: string){
    return this.store[id]
  }
}

construcor(public wheel: Wheel){
  
}
//속성 알아서 정의됨
```

* protected 는 상속받은 곳에서도 사용 가능함 - 하위 타입에서



#### 인터페이스의 구현 

* implements , abstract 도 있음, ... extends... 다른 프로그래밍 언어랑 똑같음..
* 기억상 C++에서는 여러 인터페이스 구현이 안되었던거로 기억하는데 여기서는 그냥 되는거같음

```typescript
interface Car{
  wheel: Wheel;
  gas: number;
	go(): void;
}
interface Truck{
  capatity: number;
}
class VolvoTruck implements Car, Truck{
	constructor(public wheel: Wheel){
    
  }
}


```

 