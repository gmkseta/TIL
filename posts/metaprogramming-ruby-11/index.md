---
title: M Ruby - 11.alias_method_chain의 흥망성쇠
date: "2021-05-25"
update: "2021-05-25"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

* 이전 두 장에서 Rails의 모듈 설계와 그 설계가 시간이 지남에 따라 어떻게 변했는지 살펴봤다.
* 이 장에서는 Rails 역사의 더 극적인 변화에 대해 이야기 해보도록 하겠다.
* 결국 Rails 코드베이스에서 거의 완전히 폐기된 `alias_method_chain`이라는 메서드가 어떻게 흥하고 망했는지

## alias_method_chain의 부흥

* Include - Extend 트릭에서 흥미로운 코드 조각을 보여줬었다.

```ruby
module ActiveRecord
  module Validations
    def self.included(base)
      base.extend ClassMethods
      # here
      base.class_eval do
        alias_method_chain :save, :validation
        alias_method_chain :save!, :validation
      end
      # here
end
```

* ActiveRecord::Base에 Validations 모듈이 포함되어 있으면 표시된 라인이 Base를 다시 열고 alias_method_chain을 호출한다.

### alias_method_chain를 썻던 이유

* Greeting 메서드를 정의하는 모듈이 있다고 가정한다. 다음 코드처럼 보일 수 있다.

```ruby
module Greetings
  def greet
    "hello"
  end 
end
class MyClass
  include Greetings
end
MyClass.new.greet  # => "hello"
```

* 만약 Greetings를 선택적인 기능으로 감싸고 싶다고 가정해보자.
* 예를들어 인사말이 더 열정적이였으면 좋겠다

```ruby
class MyClass
  include Greetings
  def greet_with_enthusiasm
    "Hey, #{greet_without_enthusiasm}!"
  end
  alias_method :greet_without_enthusiasm, :greet
  alias_method :greet, :greet_with_enthusiasm
end
MyClass.new.greet  # => "Hey, hello!"
```

* 새로운 두 가지 메서드를 정의한다. 
  * `greeting_without_enthusiasm`는 원래 Greeting의 별칭이다.
    * 두 번째는 `greeting_with_enthusiasm` 은 `greeting_without_enthusiasm`을 호출하고 그 위를 추가단어로 감싼다
* 이런식의 래핑하는 아이디어는 레일즈에서 일반적이다.
* method, method_with_feature 및 method_without_feature가 생긴다
* 별칭을 여기저기 작성하는 대신 Rails에서는 이러한 작업을 수행하는 메타프로그래밍 방법을 제공했다.
* ActiveSupport 라이브러리의 일부였었다.

### alias_method_chain의 구현

```ruby
class Module
  def alias_method_chain(target, feature)
    # Strip out punctuation on predicates or bang methods since
    # e.g. target?_without_feature is not a valid method name.
    aliased_target, punctuation = target.to_s.sub(/([?!=])$/, ''), $1
    yield(aliased_target, punctuation) if block_given?
    with_method = "#{aliased_target}_with_#{feature}#{punctuation}"
    without_method = "#{aliased_target}_without_#{feature}#{punctuation}"
    alias_method without_method, target
    alias_method target, with_method
    case
    when public_method_defined?(without_method)
      public target
    when protected_method_defined?(without_method)
      protected target
    when private_method_defined?(without_method)
      private target
    end 
  end
end
```

* 대상의 메서드 이름과 추가 기능의 이름을 사용한다.
* target_without_feature / target_with_feature 라는 이름의 두가지 새 메서드 이름을 eval한다.
* 원래 대상을 target_without_feature으로 저장하고, target_with_feature의 별칭을 target으로 지정한다.
  * target_with_feature라는 메서드가 동일한 모듈 어딘가에 있다고 가정함
* 마지막 스위치 케이스는 target_without_feature의 원래 대상과 동일한 접근 제한자를 설정함

### ActiveRecord::Validation에서의 사용

```ruby
def self.included(base)
  base.extend ClassMethods
  # ...
  base.class_eval do
    alias_method_chain :save, :validation
    alias_method_chain :save!, :validation
  end
# ...
end
```

* 이 줄은 Validation을 포함시키는 ( ActiveRecord::Base ) 클래스를 다시 열고 save를 해킹한다
* 유효성 검사를 자동으로 save 할때마다 추가할 수 있다.
* save_without_validation이라고 하면 유효성 검사를 안하고 저장 가능하다.
* 이 모듈은 save_with_validation 및 save_with_validation!을 구현해야겠지?

```ruby
module ActiveRecord
  module Validations
    def save_with_validation(perform_validation = true)
      if perform_validation && valid? || !perform_validation
        save_without_validation
      else
        false
      end 
    end
    def save_with_validation!
      if valid?
        save_without_validation!
      else
        raise RecordInvalid.new(self)
      end 
    end
    def valid?
      #...
```

* 실제 유효성 검사는 `valid?` 에서 일어난다.
* `Validation#save_with_validation`은 유효성 검사가 실패하거나 호출자가 유효성 검사를 명시적으로 비활성화 한 경우 false를 반환한다.
* 그렇지 않으면 원래 save_without_validation을호출한다.
* `!` 에서는 에러를 발생시킨다.

## alias_method_chain의 끝

* Rails 2에서의 많은 모듈이 alias_method_chain을 사용하여 include하는 메서드의 기능을 래핑했다.
* 결과적으로 alias_method_chain은 Rails와 수 십개의 타사 라이브러리에서 모두 사용되었다.
* alias_method_chain는 그저 Around Alias의 캡슐화일 뿐이고 [예전 챕터](https://blog.seongjun.kr/metaprogramming-ruby-5)에서의 문제점을 그대로 갖고있다.
* 설상가상으로 alias_method_chain많이 사용되면서 실제 메서드의 버전 추적이 어려워진다.
* 그러나 alias_method_chain의 가장 치명적인 문제는 대부분의 경우 불필요하다는 것,
* 객체 지향 적인 관점에서 기존 메서드 주위에 기능을 래핑하는 보다 우아하고 내장된 방법을 제공한다.

```ruby
module Greetings
  def greet
   "hello"
  end 
end
class MyClass
  include Greetings
end
MyClass.new.greet  # => "hello"

module EnthusiasticGreetings
  def greet
    "Hey, #{super}!"
  end
end
class MyClass
  include EnthusiasticGreetings
end
MyClass.ancestors[0..2]  # => [MyClass, EnthusiasticGreetings, Object]
MyClass.new.greet        # => "hello"
```

* `EnthusiasticGreetings` 을 포함할 때 해당 모듈이 클래스의 조상 체인에 있는 클래스보다 더 높아진다.
* 따라서 greet 함수는 모듈의 greet를 재정의한다.
* `EnthusiasticGreetings` 같은 중개 모듈을 삽입하고 오버라이드 및 super를 호출할 수 있다
* 하지만 만약 클래스가 Rails같은 라이브러리의 일부이며 소스코드에서 직접 작업하지 않고 해당 라이브러리를 확장하므로 모든 경우에 그럴 수 있는게 아니다
* 이 제한으로 인해 alias_metho_chain을 쓰는 것

```ruby
module EnthusiasticGreetings
  def greet
    "Hey, #{super}!"
  end
end
class MyClass
  prepend EnthusiasticGreetings
end
MyClass.ancestors[0..2]  # => [EnthusiasticGreetings, MyClass, Object]
MyClass.new.greet        # => "Hey, hello!"

```

* Arounded Aliases에 대한 현대적인 대안인 prepended wrapper를 사용
* MyClass의 조상 체인에서 MyClass#greet보다 낮아서 재정의가 잘 된다.

## 교훈

* 이 책을 통해 메타프로그래밍이 얼마나 편리하고 우아하고 멋진지에 대해 배웠다

* 하지만 alias_method_chain에 대한 이야기는 경고에 가깝다.

* 메타프로그래밍 코드는 때때로 복잡해질 수 있으며 심지어 더 전통적이고 단순한 기술을 간과하게 만들 수 있다.

* 메타프로그래밍을 피하고 평범한 구식 OOP을 사용할 수 있다.

* 코드를 너무 똑똑하게 만드려는 유혹에 저항하라는 교훈

* 메타프로그래밍보다 목표를 달성하는 더 간단한 방법이 있는지 자문해본다.

  























