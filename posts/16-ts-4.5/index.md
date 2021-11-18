---
title: "[TypeScript] Interface, Function type annotation"
date: "2021-04-04"
tags: ["ts", 'js']
cover: "./typescript.jpeg"

---

#### Interface

OOP에서의 인터페이스와 동일함

```typescript
interface Car{
  go(): void;
  stop(): void;
  weight: Number;
}

const myCar: Car = {
  go(){
  },
  stop()
  }
}
```

옵셔널 한 것

```typescript
interface Car{
  brand?: string;
}
```

타입스크립트에서는 가져야할 속성들을 정의하는것에 많이 쓰이는듯, ide에서 코드 자동완성에 용이

타입스크립트를 컴파일 할 경우 인터페이스 코드는 타입 체크할때만 쓰이므로 사라짐,



#### function type annotation

매개변수에 대한 타입,  반환형에대한 타입 정의

```typescript
function hello(name: string): string{
	return `${name}님 안녕하세요`
}


```

함수 시그니처 - 바디 없이 정의 할 시 ( 매개변수 타입)
함수 시그니쳐를 동일한걸 여러개 작성하는게 오버로드 시그니쳐라고 함 
구현체가 있어야함

```typescript

interface SportsCar{
	maxSpeed: Number
}
interface Truck{
  capacity: Number
}

function getCar(type: "스포츠카"): SportsCard
function getCar(type: "트럭"): Truck

function getCar(type: "스포츠카" | "아이스크림"){
  if(type === "스포츠카"){
    return {maxSpeed: 100}
  }else if(type === "아이스크림"){
    return {capacity: 1000}
  }else {
    throw new Error("Not Found")
  }
}
```

