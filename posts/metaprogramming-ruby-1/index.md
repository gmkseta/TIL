---
title: Metaprogramming Ruby - 1
date: "2021-04-01"
update: "2021-04-01"
series: "Metaprogramming Ruby"
tags: ["ruby"]
cover: "2021-04-01-03-27-27.png"
---

회사에서 조만간 루비를 안 쓰게 될 것 같다.

~~루비를 보내주는 마지막 공부.....~~

아니면 언젠가 이직하면 레일즈를 쓰는 회사로 이직을 하게될까?

## Metaprogramming Ruby

아무튼 Metaprogramming Ruby라는 책을 읽어 보려한다. 올리는 글은 챕터별 정리와 사견

되도록 우리나라에 출판된 번역본 책은 안 올리려고 하는데

이 책은 번역본도 없고 깃헙에 pdf로 올라와 있어서 한번 해본다.

## The M Word

```
메타 프로그래밍은 코드를 쓰는 코드이다.
```

일단은 이 정도가 제일 간단한 정의이다. 자세한 얘기 이전에 먼저 프로그래밍 언어 자체에 대해 살펴본다.

## 유령 마을 vs 시끌시끌한 시장

- 소스 코드를 변수, 클래스, 메서드 등의 활기찬 시민들로 가득 찬 세상으로 생각해 보자
- 많은 프로그래밍 언어에서 이 시민들은 유령 같다
  - C++를 예로 들면 컴파일러가 작업을 마치면 변수나 메서드 같은 것들은 형태를 잃는다.....!
  - 런타임에서 다 사라지고 유령 같지
- 루비와 같은 언어에서 런타임은 시끌시끌한 시장 같다.
  - 대부분의 언어 구조들이 여전히 생생하게 살아있고
  - 심지어 언어 구조까지 걸어갈 수 있고 그것에 관한 질문을 할 수도 있다.
    - 이를 `Introspection`이라고 한다.

```ruby
# the_m_word/introspection.rb
class Greeting
  def initialize(text)
		@text = text
	end
  def welcome
    @text
	end
end
```

```ruby
my_object = Greeting.new("Hello")
```

- `Greeting` 클래스를 정의하고 객체를 만들었다.

```ruby
my_object.class 														# => Greeting
```

- `my_object` 에게 클래스가 뭐냐고 물어보면 확실하게 `Greeting 이다~~~` 라고 답해줌
- 그럼 이제 그 클래스로부터 인스턴스 메서드의 리스트를 물어볼 수 있다.

```ruby
my_object.class.instance_methods(false)     # => [:welcome]
```

- 클래스는 메서드 이름을 포함하는 배열로 답을 해준다. `[:welcome]`
- false 인수는 상속받은 메서드는 나열하지 않는다는 뜻
- 그럼 객체를 보면서 인스턴스 변수에 대해 물어보자

```ruby
my_object.instance_variables                # => [:@text]
```

- 잘~ 답해준다.
- 루비에서 객체와 클래스는 일급 시민( FIrst-class citizens )이기 때문에 우리는 많은 정보들을 얻을 수 있다.

### -

우리는 루비에서 런타임에 언어의 구조를 읽을 수 있다 !

하지만 작성하는 것은??? 프로그램이 실행되는 동안 Greeting에 새 인스턴스 메서드를 추가하려면???

## 메타프로그래머 이야기

- 데이터베이스에 객체를 저장하기 위한 간단한 라이브러리를 구축해보자

### 첫 번째 시도

- 각 클래스를 데이터베이스 테이블에 매핑하고 각 객체를 레코드에 매핑한다.
- 객체를 생성하거나 그 속성에 액세스 할 때 객체는 SQL 문자열을 생성하여 데이터베이스로 보낸다.

```ruby
#the_m_word/orm.rb
class Entity
  attr_reader :table, :ident
  def initialize(table, ident)
    @table = table
    @ident = ident
    Database.sql "INSERT INTO #{@table} (id) VALUES (#{@ident})"
	end
  def set(col, val)
    Database.sql "UPDATE #{@table} SET #{col}='#{val}' WHERE id=#{@ident}"
	end
  def get(col)
    Database.sql ("SELECT #{col} FROM #{@table} WHERE id=#{@ident}")[0][0]
	end
end
```

- SQL을 알고있다면 읽을 만 할 듯
- `Entity`에서 id값, 테이블 이름을 갖고있고 `Entity`를 생성하고 나면 데이터베이스에 저장된다
- `Entity#set`은 컬럼의 값을 업데이트, `Entity#get`은 컬럼의 값을 갖고 온다

```ruby
class Movie < Entity
  def initialize(ident)
    super "movies", ident
  end
  def title
    get "title"
	end
  def title=(value)
    set "title", value
	end
  def director
    get "director"
	end
  def director=(value)
    set "director", value
	end
end

```

- `Entity`클래스로 `Movie`를 정의해봤다.

- `Movie` 클래스는 `title`, `director` 에 대한 reader , writer를 갖고있다.

- 다음과 같은 코드로 새 영화를 데이터베이스에 넣을 수 있다!

  ```ruby
  movie = Movie.new(1)
  movie.title = "Doctor Strangelove"
  movie.director = "Stanley Kubrick"
  ```

- 이제 데이터베이스에 id가 1인 영화가 생겼다!

- ( `director = "~~~"` 이 꼴은 `director=("~~~")` 이거랑 동일 )

**하지만 중복이 많다.**

데이터베이스의 컬럼에도 `title`을 갖고있고, `Movie`클래스에도 `@title` 필드를 갖고있다.

그리고 `title` 메서드를 갖고있고 두개의 `"title"` 문자열 상수도 있다.

## 메타프로그래밍 시작

- 메타프로그래밍 기반의 솔루션을 찾아보자

- 객체를 데이터베이스 테이블에 매핑하는 ActiveRecord 라이브러리를 사용해본다.

```ruby
class Movie < ActiveRecord::Base
end
```

```ruby
movie = Movie.create
movie.title = "Doctor Strangelove"
movie.title  # => "Doctor Strangelove"
```

- 이전 코드는 Movie에서 레코드를 매핑하는 객체를 만든 뒤 Movie의 title을 호출하여 접근했다.
- 테이블에 대한 이름도 필요했다.
- 하지만 이번 코드에선 이런 과정이 소스코드에 전혀 없다.
- 정의하지 않은 `title`, `title=` 이 어떻게 존재하는 것일까?

### ActiveRecord의 기본 작동 방식

- 테이블 이름은 간단하게 클래스의 `introspection` 을 통해서 규칙을 정한다.
  - 클래스의 이름이 `Movie`이므로 `ActiveRecord`는 이를 `Movie`라는 테이블에 매핑한다
- 그렇다면 객체의 속성에 접근하는 `title=` , `title` 같은 메서드는?? - **여기서 메타 프로그래밍!**
  - 데이터베이스 스키마에서 이름을 유추하고 자동으로 정의한다.
  - 런타임에 스키마를 읽고 `Movie`테이블에 `title`, `director`라는 두 개의 컬럼을 발견
  - 동일한 이름의 두 속성에 대한 접근자 메소드를 정의한다.

#### 이게 바로 introspection의 음 양!! 단순히 언어의 구조를 읽는 것이 아니라 쓰기까지 하는 것

- 메타 프로그래밍은 런타임에 언어 구조를 조작하는 코드를 작성하는 것이다
- ActiveRecord는 이 컨셉을 적용했다.
- 각 클래스의 특성에 대한 접근자 메소드를 작성하는 대신
- 상속받는 클래스에 대해 런타임에 이런 메소드를 정의하는 코드를 작성했다.

## 메타프로그래밍과 루비

맨 처음 유령 마을과 시끌시끌한 시장에 대해 얘기했던 게 기억나는가?

언어의 구문을 조작하려면 해당 구문이 런타임에 있어야한다.

몇 가지 언어들은 런타임에서 제어기능을 제공하는데 이에대해 간략히 살펴보자.

> Code Generators and Compilers
>
> 메타프로그래밍에서는 코드를 작성하는 코드를 작성한다. 하지만 그게 code generator와 컴파일러가 해주는 것 아닌가?
>
> 예를들어 Java code를 작성하고 코드 제너레이터로 XML 설정 파일을 만들 수 있다.
> 넓은 의미에서 이 XML 생성은 메타프로그래밍의 한 예이다.
>
> 메타프로그래밍의 또 다른 의미로, 프로그램을 사용하여 두 번째 고유 프로그램을 생성하거나 조작한 다음 두 번째 프로그램을 실행한다는 것도 있다!
> ( C++의 템플릿 )
>
> 하지만 이 책에서는 메타프로그래밍의 다른 의미, 런타임에 스스로 조작하는 코드에 초점을 맞춘다.
> Code Generator 및 Compiler의 정적 메타 프로그래밍과 구별되는 동적 메타 프로그래밍이라고 생각하면 된다.
>
> 또한 많은 언어에서 동적 메타프로그래밍을 할 수 있지만 루비에서는 더 우아하고 원활하게 할 수 있다!

- C로 작성된 프로그램은 런타임에 대부분의 정보가 손실되기 때문에 메타프로그래밍이나 Introspection을 지원하지 않는다.
- C++에서 몇몇 언어들의 구문들은 컴파일에서 살아남기 때문에 객체와 클래스에서 사용이 가능
- Java에서 컴파일과 런타임은 더 모호하다. 클래스 메서드를 나열하거나 슈퍼클래스까지 올라갈 수 있는 충분한 Introspection을 제공!

**루비는 매우 메타프로그래밍 친화적인 언어다. 컴파일 타임이 없으며 대부분의 언어 문법을 런타임에 사용 가능하다.**

**작성하는 코드와 런타임의 경계가 없다.**

**루비의 메타프로그래밍은 그저 전문가를 위한 모호한 예술이 아니고, ActiveRecord처럼 정교한 것을 만드는 데만 유용한 기능도 아니다**

**만약 고급 루비 코딩의 길을 가고싶다면 .... !**



## 사견

* 아직까진 쉬운 내용

* 다른 orm들도 메타프로그래밍을 쓰는 것으로 알고 있다.

  

  

