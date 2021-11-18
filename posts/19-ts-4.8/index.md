---
title: "[TypeScript] Generic"
date: "2021-04-08"
tags: ["ts", 'js']
cover: "./typescript.jpeg"
---

## Generic

타입을 파라미터화 할 수 있어서, 한가지 타입만 쓰는것이 아닌 다양한 파라미터를 처리 할 수 있도록

```typescript
function createPromise<T>(x: T, timeout: number){
  return new Promise((resolve: (v: T) => void, reject)=>{
    setTimeout(()=>{
      resolve(x);
    }, timeout)
  })
}
createPromise<string>('1', 100).then(v = console.log(v));
createPromise<number>(1, 100).then(v = console.log(v));

function createPromise<T>(x: T, timeout: number){
  return new Promise<T>((resolve, reject)=>{
    setTimeout(()=>{
      resolve(x);
    }, timeout)
  })
}
createPromise('1', 100).then(v = console.log(v));
createPromise(1, 100).then(v = console.log(v));

function createTuple<T, U>(v: T, v2: U): [T, U]{
  return [v, v2]
}

const t1 = createTuple('user1', 1000);


```



특정 타입의 하위 타입으로 범위를 고정시킬 수도 있다.

```typescript
interface DB<T>{
  add(v: T): void;
  get(): T;
}
class D<T> implements DB<T>{
  add(v: T): void {
    throw new Error("Method not implemented.");
  }
  get(): T {
    throw new Error("Method not implemented.");
  }
}

interface JSONSerializer{
  serialize(): string;
}

class LocalDB<T> implements DB<T>{
	constructor(private localStorageKey: string){
    
  }
  add(v: T){
    localStorage.setItem(this.localStorageKey, JSON.stringify(v));
  }
  get(): T{
    const v = localStorage.getItem(this.localStorageKey);
    return (v) ? JSON.parse(v) : null;
  }
}

class LocalDB<T extends JSONSerializer> implements DB<T>{
	constructor(private localStorageKey: string){
    
  }
  add(v: T){
    localStorage.setItem(this.localStorageKey, v.serialize());
  }
  get(): T{
    const v = localStorage.getItem(this.localStorageKey);
    return (v) ? JSON.parse(v) : null;
  }
}
interface User{
  name: string
}
const userDb = new LocalDB<User>('user');
userDb.add({name: 'jay'});
const userA = userDb.get();
userA.name;
```



* 전달받은 타입에 따라 조건부 타입도 가능 , 
  * 메서드에서 반환되어질 타입을 타입 파라미터에 전달되어지는 타입에 따라 다르게 동작하는 코드를 작성할 수 있다.

```typescript
interface Veigtable{
  v: string;
}
interface Meat{
  m: string;
}
interface Cart<T>{
  getItme)(): T extends Veigtable ? Veigtable : Meat
}

const cart1: Cart2<Veigtable> = {
  getItem(){
    return {
      v: ''
    }
  }
}
```











