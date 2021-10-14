# 프로그래머 피드백

 

* 코딩 하고 ~ 확인하고 ( 피드백 )  ~ 수정 하고~



* 사용자 피드백
  * 사용자가 직접 사용, 경험 후 제보
* Quality Assurance 
  * 전문 인적 자원에 의한 인수 테스트
* 프로그래머 테스트
  * 프로그래머가 직접 피드백 장치를 준비
* 도구 피드백
  * 컴파일 오류, 정적 검사 등 도구가 제공하는 피드백



## 오버 엔지니어링

* 요구 명세에 지정되어 있지 않은 성능 달성이나, 구현 설계 품질 개선에 빠져드는 경향
* 지나치면 불필요한 낭비
* TDD는 가장 중요한 목표를 우선 달성하도록 유도하고, 피드백을 제공 - 모든 테스트가 성공했습니다!!!

핵심은 **피드백** 이다.

절차가 중요한게 아닌 짧은 주기로 지속되는 피드백

피드백을 통해서 안정적으로 지식과 코드를 늘려가는 것이 목적





## 장난감

* 임의로 결정된 숫자를 플레이어가 맞추는 텍스트 콘솔 기반 게임

## 게임 설계

* 1부터 100까지 임의 정수
* 플레이어가 숫자 입력하면
  * 업 다운 
  * 일치면 라운드 종료
* 단일 / 다중 모드 
  * 단일 - 총 시도 
  * 다중 - 승자

## 요구사항 분석

 선택 - ~ 동작하는거



게임 모델 - 정수 생성기 인터페이스 - 난수 정수 생성기

![image](https://user-images.githubusercontent.com/72075148/137150637-e18540a6-2baa-4e68-bab4-ffd82f7e8a63.png)

* 모듈 구현





# 3-1 인터페이스

## 추상화

* 주워진 맥락에 관련된 정보들을 잊어버리는 과정이다?

### 협력과 계약

* 대부분의 코드는 다른 코드와 협력
* 협력에 필요한 것은 어떻게가 아닌 무엇이다.
* 인터페이스 - 
  * 무엇을 표현하는,
  * 클라이언트 코드에 반드시 필요한 정보
  * 협력하는 코드 사이의 **계약**
  * **추상화** 결과

### 인터페이스에 프로그래밍 한다.

* 정보 은닉
  * 효과적인 모듈화
    * 조직간 의사소통 최소화
    * 변경 여파 최소화
    * 시스템 이해 도움
  * 고개된 설계 결정과 숨겨진 설계 결정
    * 어려운 설계 결정과, 변경될 것 같은 설계 결정을 숨겨라
* 대부분의 시스템 정보는 대부분의 프로그래머에게 숨겨지는 것이 도움된다.



 

# 환경 변화와 적응력

캡슐화 상속 추상화 다형성 

Open-closed Principle

메세징 뭐 지역보존 지연된바인딩 다형성..말하는거 - 바인딩

Alan Kay의.. 지연된 바인딩 때문에 , ,

ocp - 상속만 염두한 정의

너무 근데 상속에만 어쩌구 

다형적 ocp? 

Composite 패턴을 ..어쩌구

### Testability 와 적응력

* 테스트는 다 가능하고, 용이성, 얼마나 쉬운가

단위테스트 하려면 하위 시스템은 쉽게 분리할 수 있어야함

적응력 높은 코드는 분리하기 쉬움



# 입력과 출력

### 직접 입력과 직접 출력

* 공개된 인터페이스를 통한 입출력
* 다루기 간단함

### 간접 입력과 출력

* 입력된 인터페이스를 통한 입력과 출력
* 다루기 복잡한

```javascript
function commentComposerFactory({ commentRefiner }) {
```

* commentRefiner는 직접 입력을 받은건데 commentRefiner의 아웃풋은 commentComposerFactory에게 간접 입력임

* AppModel의 generator는? 외부로부터 주입된 공개된 인터페이스를 통해 받은거고, 그를 통해 받은 answer은 간접 이지?

## 부작용

* 인터페이스 설계에 드러나지 않은 출력
  * 반환 값 외 출력
* 실패, 지연, 간접출력,, - 시스템 입장에서는 출력이고, 의존성 입장에서 출렦?

```javascript
import { useState } from "react";

function Form({ commentComposer, onNewComment }) {
  const [author, setAuthor] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const newComment = commentComposer({ author, content });
    onNewComment(newComment);
    setAuthor("");
    setContent("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="author"
        value={author}
        type="text"
        onChange={(e) => setAuthor(e.currentTarget.value)}
        placeholder="작성자"
      />
      <input
        name="content"
        value={content}
        type="text"
        onChange={(e) => setContent(e.currentTarget.value)}
        placeholder="내용"
      />
      <button name="submit">입력</button>
    </form>
  );
}

export default Form;

```

`onNewComment` 은 폼 기준 간접 출력 인터페이스를 제공한다..

간접 입력과 간접 출력은 테스트대역이라는걸..





