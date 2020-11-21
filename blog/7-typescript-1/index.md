---
title: "[TypeScript] Intro - 1"
date: "2021-03-27"
tags: ["ts"]
cover: "./typescript.jpeg"
---

### TypeScript란?

타입스크립트는 자바스크립트의 슈퍼셋,  타입이 있고 컴파일 되어서 plain js를 만듦

오픈소스 프로그래밍 언어이고, 정적인 언어로 compile time에 타입을 검사한다.

장점

1. 강타입으로 대규모 어플리케이션 개발에 용이하다.
   - 일반적으로 약타입의 언어의 경우 런타임에서 타입 에러를 만나기 전 까지는 실행을 막지 않는다
   - 대규모 어플리케이션에서 ts를 사용 시 정적 타입검사를 하므로 런타임에서 타입으로 인한 에러가 날 일이 줄어든다는 뜻
2. 개발 툴이 편하다 / 코드 자동완성이나 suggestion이 편함.

하지만 강타입이냐 약타입이냐는 언어의 우위를 결정하는 요소가 아니고, 정적 타입검사와 동적 타입검사는 상호 배제적인 개념이 아니다.

[참고자료](https://basarat.gitbook.io/typescript/recap)

### 설치 및 실행

ts compiler 설치

```shell
npm install -g typescript
```

컴파일러 실행

```shell
tsc hello-world.ts
```

tsc -> typescript compiler

컴파일 시 hello-world.js가 만들어진다.

### 옵션

#### target

target 옵션 없이 컴파일 하면 , 예전버전의 자바스크립트로 변환된다. ( let / const 같은 것들이 모두 var로... 등 )

es6로 컴파일하고싶으면 다음과 같이 옵션을 주면 되는데.

```shell
tsc hello-world.ts --target es6
```

Document에 따르면 --target option은 다음과 같이 설정이 가능하다.

► `"ES3"` (default) <br/>
► `"ES5"`<br/>
► `"ES6"`/`"ES2015"`<br/>
► `"ES2016"`<br/>
► `"ES2017"`<br/>
► `"ES2018"`<br/>
► `"ES2019"`<br/>
► `"ES2020"`<br/>
► `"ESNext"`

<br/>

#### lib

ES6에서 나온 Promise를 사용하고 싶다면 --lib 옵션을 줘야한다. target 버전 외에서 나온 것들을 사용하고싶다면 마찬가지로 옵션을 줘야한다.

옵션을 따로 주지않으면 target에 따른 기본 라이브러리만 정의된다.

이 또한 Document에 따르면 다음 옵션들이 가능하고

► `ES5`, `ES6`, `ES2015`, `ES7`, `ES2016`, `ES2017`, `ES2018`, `ESNext`, `DOM`, `DOM.Iterable`, `WebWorker`, `ScriptHost`, `ES2015.Core`, `ES2015.Collection`, `ES2015.Generator`, `ES2015.Iterable`, `ES2015.Promise`, `ES2015.Proxy`, `ES2015.Reflect`, `ES2015.Symbol`, `ES2015.Symbol.WellKnown`, `ES2016.Array.Include`, `ES2017.object`, `ES2017.Intl`, `ES2017.SharedMemory`, `ES2017.String`, `ES2017.TypedArrays`, `ES2018.Intl`, `ES2018.Promise`, `ES2018.RegExp`, `ESNext.AsyncIterable`, `ESNext.Array`, `ESNext.Intl`, `ESNext.Symbol`,

es6/ es5에선 각각 기본 라이브러리가 정의되어있다.

`--target ES5`: `DOM,ES5,ScriptHost` <br/>
`--target ES6`: `DOM,ES6,DOM.Iterable,ScriptHost`

기본적으로 내가 지금 컴파일 한 옵션에 대한 json 형태의 config를 얻고싶다면, `--showConfig` 를 사용하면 된다.

```shell
tsc hello-world.ts --lib es5,dom,es2015.promise,es2015.iterable --module commonjs --showConfig
```

이러한 것들을 일일히 매번 컴파일 시 옵션으로 집어넣느냐? 하면 아니다. tsconfig라는 파일을 사용하면된다.

다음..
