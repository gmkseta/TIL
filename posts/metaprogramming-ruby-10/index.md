---
title: M Ruby - 10. Active Support's Concern Module
date: "2021-05-16"
update: "2021-05-16"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

- 이전 장에서 모듈을 포함하면 인스턴스와 클래스 메서드 모두를 얻는 것을 알게되었다.
- Active Support 라이브러리에 있는 Concern 덕분에 가능 한 것
- 이전에 어떻게 되어있었고 어떤식으로 진화하는지 알아보자

## Concern 이전의 레일즈

- 레일즈는 수년동안 많이 변경되었지만 기본 아이디어는 크게 변경되지 않았다
- 그 중 하나가 ActiveRecord::Base 개념이다.
- 이 클래스는 인스턴스 메서드와 클래스 메서드를 모두 정의하는 수십 개의 모듈로 이뤄져있다.
- 이러한 메서드를 Base에 넣는 메커니즘이 변경되었다.

### Include, Extend 사용

- Rails2에서의 유효성 검사는 `ActiveRecord::Validations` 에 정의되어있다 ( 그때는 Active Model 없었음 )
- Validation은 독특한 트릭 사용

```ruby
module ActiveRecord
  module Validations
# ...
    def self.included(base)
      base.extend ClassMethods
      # ...
    end
    module ClassMethods
      def validates_length_of(*attrs) # ...
      # ...
      end
      def valid?
      # ...
      end
      # ...
  end
end
```

- 낯익지 않나? VCR 예제에서 본 것 ( HTTP call )

1. valid? 같은 Validation의 인스턴스 메서드는 Base의 인스턴스 메서드가 된다.
2. Ruby는 hook method를 호출해서 base를 인수로 전달한다.
3. Validations::ClassMethod를 이용하여 base를 extend 한다.

결과적으로 Base는 인스턴스 메서드와 클래스 메서드 모두 다 갖고올 수 있다.

- include-and-extend 트릭이라고 부르도록 하겠다..

- 수 많은 ruby, rails 프로젝트에서 이렇게 사용했다....

- 편리하지만 몇 개의 문제가 있다.

  - 클래스 메서드를 정의하는 각각의 모든 모듈은 해당 includer를 확장하는 훅도 정의해야한다.

  - 해당 훅이 수십 개의 모듈에 걸쳐 복제된다. 결과적으로 사람들이 이럴 가치가 있나? ..흠 한 줄 더 추가해서 해결이 가능..

    ```ruby
    include Validations
    extend Validations::ClassMethods
    ```

  - 하지만 더 깊은 문제가 있다!

### The Problem of Chained Inclusions

- 다른 모듈을 포함하는 모듈을 포함한다고 가정해보자.
- ActiveRecord::Validations는 ActiveModel::Validations 을 include한다.

```ruby
module SecondLevelModule
  def self.included(base)
    base.extend ClassMethods
  end
  def second_level_instance_method; 'ok'; end
  module ClassMethods
    def second_level_class_method; 'ok'; end
  end
end
module FirstLevelModule
  def self.included(base)
    base.extend ClassMethods
  end
  def first_level_instance_method; 'ok'; end

  module ClassMethods
    def first_level_class_method; 'ok'; end
  end
  include SecondLevelModule
end
class BaseClass
  include FirstLevelModule
end

```

- 두 모듈 모두 BaseClass의 조상에 있으니 두 모듈의 인스턴스 메서드를 모두 호출 가능하다.

- include와 extend 덕분에 클래스 메서드도 사용 가능하다.

- 하지만...

  `BaseClass.second_level_class_method # => NoMethodError`

- SecondLevelModule.included를 호출할 때 기본 매개변수는 BaseClass가 아니라 FirstLevelModule

- 결과적으로 SecondLevelModule::ClassMethods의 메서드는 FirstLevelModule의 클래스 메서드..

```ruby
module FirstLevelModule
  def self.included(base)
    base.extend ClassMethods
    base.send :include, SecondLevelModule
end
```

- 이러한 구현은 덜 유연하다..
- 다른 모듈과 첫 번째 레벨의 모듈을 구별해야하고, 각 모듈은 그것이 첫 번째 레벨인지 알아야한다..
- 그리고 이 시대에는 Module#include가 프라이빗 메서드라 호출 못했음 ( Dynamic Dispatch 를 사용해야함) , 최근엔 Public

## ActiveSupport::Concern

- `ActiveSupport::Concern`은 included-and-extend 트릭을 을 캡슐화하고 연결된 include문제를 수정한다.

```ruby
require 'active_support'
module MyConcern
  extend ActiveSupport::Concern
  def an_instance_method; "an instance method"; end
  module ClassMethods
    def a_class_method; "a class method"; end
  end
end
class MyClass
  include MyConcern
end
MyClass.new.an_instance_method  # => "an instance method"
MyClass.a_class_method          # => "a class method"
```

- 어떻게 이게 되는걸까?

### Concern 코드 보기

```ruby
module ActiveSupport
  module Concern
    class MultipleIncludedBlocks < StandardError #:nodoc:
      def initialize
        super "Cannot define multiple 'included' blocks for a Concern"
      end
    end
    def self.extended(base)
      base.instance_variable_set(:@_dependencies, [])
    end
    #...
```

- Concern의 코드는 짧지만 복잡하다.
- excended및 append_features 메서드만 정의한다.

#### Module#append_features

```ruby
module M
  def self.append_features(base); end
end
class C
  include M
end
C.ancestors
# => [C, Object, Kernel, BasicObject]
```

- included는 일반적으로 비어있는 Hook 메서드였고 재정의 하려는 경우에만 존재했다.
- append_features는 실제 include가 일어나는 곳에 있다.
- append_features는 포함된 모듈이 이미 포함하는 모듈의 조상체인에 있는지 확인하고 그렇지 않으면 체인에 추가한다.
- 일반적으로는 included를 재정의하지만 append_features를 재정의..해버리면 모듈이 전혀 포함 안 되게 할 수 있다.

#### Concern#append_features

```ruby
module ActiveSupport
  module Concern
    def append_features(base)
```

- Extension이 기억 나나?
- append_features는 Concern의 인스턴스 메서드이므로 Concern을 확장하는 모듈의 클래스 메서드가 된다.
- 즉 Validations라는 모듈이 Concern을 확장하면 Validations.append_features 클래스 메서드를 얻지
  - 싱글톤 클래스들이 갖던거 기억하나?
  - 아뇨.. ㅜㅜ
- Concern을 확장하는 모듈은 @\_dependencies 클래스 변수를 얻는다.
- append_features의 재정의를 얻는다.

#### Inside Concern#append_features

```ruby
module ActiveSupport
  module Concern
    def append_features(base)
      if base.instance_variable_defined?(:@_dependencies)
        base.instance_variable_get(:@_dependencies) << self
        return false
      else
        return false if base < self
        @_dependencies.each { |dep| base.send(:include, dep) }
        super
        base.extend const_get(:ClassMethods) \
          if const_defined?(:ClassMethods)
        # ...
end end

```

- 어렵지만 기본 아이디어는 간단하다.
- 다른 concern에 concern을 include하지마!
- 대신 concern이 서로를 include 하려할 때 종속성 그래프에 연결하기만 하면 된다.
- 스스로 include하는 것이 아닌, 모든 종속성을 한번에 includer로 돌아서 include한다.
- self는 concern이다, 클래스 메서드로 실행이 되고, base는 관심사거나 이를 포함하는 모듈이다.
- 맨 처음 concern을 include하려고하면?
  - @\_dependencies 클래스 변수가 있는 것이 문제
  - 이를 조상 체인에 자신을 추가하는 대신 dependencies에 자신을 추가하고 include가 실제로 안 되었음을 알리기 위해 false
  - 예를들어 ActiveModel::Validations 이고, ActiveRecord::Validations에 포함되는 경우임!
- 만약 Concern이 아닌 경우 -

  - 이미 이 포함자의 조상인지 확인한다. ( base < self )
  - 아닌 경우 종속성을 포함시킨다.
  - 예를들어 ActiveRecord::Validations이고, ActiveRecord::Base에 포함되는 경우임!

- 모든 종속성을 포함자의 조상 체인으로 롤링한 후에도 super으로 표준 append_features를 호출하여 조상 체인에 자신을 추가해야한다.
- ClassMethod 모듈로 includer를 확장해야한다. 이에대한 참조를 얻으려면 Kernel#const_get이 필요함
- Concern의 모듈 범위가 아닌 self의 범위에서 상수를 읽기 위함

### Concern Wrap Up

- ActiveSupport::Concern은 몇 줄의 코드로 단일 모듈로 래핑된 최소한의 종속성 관리 시스템
- 그 코드는 복잡하지만, Active Model의 소스를 보면 알 수 있듯이 Concern을 사용하는 것은 쉽다

```ruby
module ActiveModel
  module Validations
    extend ActiveSupport::Concern
      # ...
    module ClassMethods
      def validate(*args, &block)
      # ...
```

- 일부는 이런 호출들 뒤에 숨겨진 너무 많은 마법들이 있고, 이런 숨겨진 복잡성엔 숨겨진 비용이 따른다고 한다.
- 또 다른 일부는 Concern이 Rails 모듈을 최대한 슬림하고 단순하게 유지하는 데 도움을 준 것에.... 굿굿..

## 교훈

- 대부분의 언어에서는 구성 요소를 함께 묶는 방법이 많지 않다
- 클래스에서 상속하거나 객체에 위임할 수 있다.
  - 멋지게 만들고 싶다면 종속성 관리를 전문으로 하는 라이브러리 또는 전체 프레임워크를 사용할 수 있다.
- Rails의 개발자의 프레임워크의 일부를 함께 묶는 방법...
  - 처음에는 아마도 모듈을 포함하고 확장했을 것이고
  - 나중에는 코드에 메타프로그래밍의 마법의 가루를 뿌리고 include-and-extend 트릭을 사용
  - 나중에 Rails가 계속 성장하면서 이 관용구가 가장자리에서 삐걱거리기 시작했고..
  - include-and-extend를 메타프로그래밍이 많은 ActiveSupport::Concern으로 대체했습니다.
  - 그들은 한 번에 한 단계씩 자체 종속성 관리 시스템을 발전시켰습니다.
- 수년에 걸쳐 우리는 소프트웨어 설계가 "처음부터 제대로 하는" 일이 아니라는 것을 배웠다.
- 이것은 모듈이 상호 작용하는 방식과 같이 근본적인 것을 변경하기 위해 메타프로그래밍을 사용할 수 있는 Ruby와 같은 가단성 언어에서 특히 그렇다..
- 메타프로그래밍은 영리해지는 것이 아니라 융통성에 관한 것
  - 코드를 작성할 때 처음부터 완벽한 디자인을 위해 애쓰지 않고 복잡한 메타프로그래밍 트릭이 필요할 때까지 사용하지 않는다.
  - 대신 작업을 수행하는 가장 확실한 기술을 사용하여 코드를 단순하게 유지하려고 한다.
  - 어쩌면 어느 시점에서 내 코드가 엉키거나 완고한 중복을 발견할 수 있다..
  - 그 때 메타프로그래밍과 같은 더 좋은 방법을 찾게된다.
  - 이 책은 메타프로그래밍 성공 사례로 가득 차 있으며 ActiveSupport::Concern도 그 중 하나이다,....
  - 그러나 Concern의 복잡한 코드와 약간 논쟁의 여지가 있는 성격은 메타프로그래밍의 어두운 면을 암시한다...
  - 이것은 Rails의 가장 악명 높은 메소드에 대한 이야기를 살펴볼 다음 장의 주제
