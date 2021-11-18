---
title: 1. Tailwindcss ? 왜쓰는걸까
date: '2021-03-22'
tags: ['frontend', 'tailwindcss', 'css']
cover: './tailwindcss-pre.png'
---

###### 많은 내용이 맨 아래 링크를 참고하여 작성되었고 주관도 살짝 들어갔습니다

---

최근 회사에서 tailwindcss 사용을 고려하게되면서 알게된 내용을 글로 쓰고자한다.  잘하면 관련 글을 몇가지 더 쓸지도?... 

일단 tailwindcss는 bootstrap, semantic ui같은 프론트엔드 라이브러리이며 utilify-first css의 개념을 기반으로 만들어졌다. 

## Concept : Atomic CSS ( functional css, utility-first css...)

css를 작성하는 많은 방법론이 있다.

몇개월정도 한 프로젝트를 잡고 씨름을 해본사람이라면 모두 알겠지만, 시간이 지날수록 코드가 너무 방대해져서 유지보수가 어려워지는 현상을 다들 겪었을꺼같다.

이러한 현상들을 해결하기 위해 사람들이 만든 CSS 방법론들을 많이 사용하게된다.

사람들이 많이 사용하는 고전적인 OOCSS, SMACSS 혹은  BEM 등의 방법론이 있는데 Atomic css는 이들과는 정 반대의 아이디어로 구성이 된다.

기본적으로 페이지의 요소를 재사용가능한 객체로써 다루지않으며 객체라는 개념 없이 각 클래스를 하나의 목적만 가진 유틸리티 클래스로 스타일링 한다.

예를들어 우리가 맨 처음에 css에대해 배울때 하나의 카드에 대한 마크업을 한다면,

```html
<div class="card">
   card
</div>
```

이런식으로 html을 작성 후 css에 `.card` 에 대한 스타일을 작성하기 마련이다 하지만 atomic css에서는

```html
<div class="padding-sm border-radius-sm bg-white">
	card
</div>
```

이런식으로 마크업하게된다. 

아래 내용은 tailwindcss document에 있는 core concepts의 첫번째 내용이다.

전통적으로, 웹에서 스타일링이 필요할때마다, 우린 css를 작성한다.

```html
<div class="chat-notification">
  <div class="chat-notification-logo-wrapper">
    <img class="chat-notification-logo" src="/img/logo.svg" alt="ChitChat Logo">
  </div>
  <div class="chat-notification-content">
    <h4 class="chat-notification-title">ChitChat</h4>
    <p class="chat-notification-message">You have a new message!</p>
  </div>
</div>

<style>
  .chat-notification {
    display: flex;
    max-width: 24rem;
    margin: 0 auto;
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: #fff;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }
  .chat-notification-logo-wrapper {
    flex-shrink: 0;
  }
  .chat-notification-logo {
    height: 3rem;
    width: 3rem;
  }
  .chat-notification-content {
    margin-left: 1.5rem;
    padding-top: 0.25rem;
  }
  .chat-notification-title {
    color: #1a202c;
    font-size: 1.25rem;
    line-height: 1.25;
  }
  .chat-notification-message {
    color: #718096;
    font-size: 1rem;
    line-height: 1.5;
  }
</style>
```

tailwind을 쓰면 너는 이미 있는 클래스들로 바로 html에서 작성한다.

```html
<div class="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
  <div class="flex-shrink-0">
    <img class="h-12 w-12" src="/img/logo.svg" alt="ChitChat Logo">
  </div>
  <div>
    <div class="text-xl font-medium text-black">ChitChat</div>
    <p class="text-gray-500">You have a new message!</p>
  </div>
</div>
```



## 장점??

이런 접근 방식은 직접 css를 작성하지 않고도 마크업이 가능하다. 

스타일을 수정할 때, css파일이 아닌 html을 수정하게 되며, 마크업과 스타일을 동시에 개발할 수 있게된다.

클래스의 이름을 다시 만들 필요가 없고, css파일이 커지지 않는다는 장점이 있다.

특정 마크업을 지울때도 딱히 css파일에서 찾아서 지워줄 필요도 없다.

물론 맨처음에 이런 코드를 봤을때는 이게 인라인 스타일하고 뭐가 다른가 싶은 생각을 했었다. 


하지만 확실한 장점은 class 이름을 뭘로 지을까 하는 고민을 줄이며 우리의 글로벌한 css를 수정할 때 어떤 사이드이펙트가 날까 고민하는 것도 줄이게된다.

이런식으로 미리 정의된 유틸리티 클래스로 작업하게되면 생산성이 증가하는 것 같다.



---

참고

https://tailwindcss.com/docs

https://www.browserlondon.com/blog/2019/06/10/functional-css-perils/

https://locastic.com/blog/i-was-wrong-about-utility-first-css-and-here-is-why/

https://medium.com/actualize-network/modern-css-explained-for-dinosaurs-5226febe3525


