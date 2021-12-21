# 팩토리 패턴

* 클래스 내에서 다른 클래스에 대한 객체를 생성하고 사용할 때 결합이 생김
* 만약 조건에 따라 다른 클래스를 사용해야한다면? 클래스 이름 등을 직접 지정해 객체를 생성하면 강한 결합 관계가 발생
* 동일 클래스 이름으로 인한 결합관계 발생

```python
class Hello:
  def greeting(self, _type):
    if _type:
      obj = ClassName1();
    else:
      obj = ClassName2();
    return obj.text()
```



## 의존성 주입

* 객체의 의존성은 내부적 발생과 외부적 발생

### 복합 객체

* 하나의 객체가 다른 객체의 정보를 가진 구조
* 객체의 정보는 클래스의 프로퍼티 값을 통해 다른 외부 객체를 가리킨다.
* 종속적이고 연관 관계를 갖게 됨

```python
class Hello:
  def __init__(self, obj):
    self.korean = obj
  def greeting(self):
    return self.korean.text()
```

* 외부에서 의존성을 주입, 생성자 메서드에서 외부로부터 객체르 받아서 사용한다.
* 종속적인 연관 관계가 된다.

## 의존 관계의 문제점

* 객체를 직접 생성하는 것은 강력한 결합 관계인 코드가 된다.
* 객체 간에 강한 의존 관계를 갖는 구조적 문제가 발생, 코드의 유연성이 떨어지고 변화와 발전을 방해
* 하지만 생성을 안 할순 없으니
* 객체 생성을 별개의 클래스로 구축하여 위임한다.

### 생성 위임

* 객체 생성을 담당할 별도의 클래스를 선언한다.
* 팩토리의 객체를 호출하는 것으로 대체한다.
* 객체의 요청과 생성을 별도의 클래스로 분리함으로써 느슨한 결합관계로 변경한다,.

### 객체 공장

* 객체의 생성 작업을 분리 방법은 클래스, 메서드 두개있음

## 팩토리 패턴

```python
class Factory:
  def getInstance():
    return Korean();
  
class Hello:
  def greeting(self):
    ko = Factory.getInstance()
    return ko.text()
```

* getInstance를 정적 타입으로 호출한다

* 불필요한 호출 증가로 성능 저하? 하지만 무의미할 정도
* 객체 생성을 다른 객체에 위임함으로써 내부적인 결합을 제거하고 동적으로 객체를 관리

### 클래스의 선택

```python
class Factory:
  def getInstance(_type):
    if _type=="ko":
      return Korean()
    elif _type=="en":
      return English()
    
    

class Hello:
  def greeting(self, _type):
    lng = Factory.getInstance(_type)
    return lng.text()
```

#### 형식 안정성

* "en", "ko" 등을 상수로 선언해서 사용하거나 이넘 사용

## Simple Factory

```python
class Hello:
  def greeting(self):
    lng = Hello.factory()
    return lng.text()
  def factory():
    return Korean()
```

* 간단하게 사용 가능!
* 정적 팩토리 패턴이라고 함, 객체에서 직접 객체 생성을 처리

## 장점

* 객체 생성 관련된 처리를 별도의 클래스 객체로 위임
  * 사용과 생성을 분리하는 과정에서 중복된 코드를 정리하는 효과
* 유연성과 확장성이 개선됨
  * 개발 과정에서 클래스 이름이 변경돼도 코드를 일일이 수정하지 않고 팩터리 객체를 통해 손쉽게 변경
* 어떤 객체를 생성할지 모르는 초기 단계 코드에 유용. 일단 객체를 먼저 호출해서 사용한 후 쉽게 수정

## 단점

* 별도의 새로운 클래스가 필요함, 관리할 파일이 늘어남
  * 단순 팩토리 사용 가능함





