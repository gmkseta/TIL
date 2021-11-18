---
title: "[TypeScript] InterSection, Union, Type Guard"
date: "2021-04-09"
tags: ["ts", 'js']
cover: "./typescript.jpeg"
---

## Intersection

```typescript
interface User{
  name: string;
}
interface Action{
  do(): void;
}
function createUserAction(u: User, a: Action): User & Action {
  return { ...u, ...a };
}
const u = createUserAction({name: 'jay'}, {do(){ }});
//이렇게 합쳐진 애가 리턴되야할때 인터페이스를 다시 정의하는게 아니라 .. 
```



## Union

```typescript
// 또는임
function compare(x: string | number, y: string | number){
  //코드 추천에도 두 타입 모두에서 사용할 수 있는 메서드들만 나옴
  //string끼리, number끼리 하고싶으면 타입 가드를 해야함
  if(typeof x === 'number' && typeof y === 'number'){
    return x === y ? 0 : x > y ? 1 : -1;
  }
  if(typeof x === 'string' && typeof y === 'string'){
    return x.localCompare(y);
  }
  throw Error('not supported type');
}

//런타임 에러가 발생하는데 이전에 썻던 함수오버로딩을 저 앞에 선언해도됨 ? 저위에
function compare(x: string, y: string )
function compare(x: number, y: number )

[3,2,1].sort(compare)
['a','c','b'].sort(compare)
```

만약 인터페이스로 만든 애들을 타입 가드를 하려면? - 자바스크립트로 변환시 어차피 인터페이스는 없자나!!

```typescript
function process(v: User | Action){
  if((<Action>v).do){
    //하지만 이 안에서도 타입 가드가 된게 아니기때문에 작성 해줘야한다.
    (<Action>v).do()
  }
    //Action이라는 타입으로 assertion 되었기때문에 쓸수있음
}

//매번 작성이 어렵다.. 사용자 정의 타입가드를 만든다 - v is Action
function isAction(v: User | Action): v is Action{
  return (<Action>v).do !== undefined;
}

function process(v: User | Action){
  if((isAction(v)){
		v.do
  }else{
    
  }
}
```





