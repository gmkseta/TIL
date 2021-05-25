---
title: M Ruby - 3. Methods
date: "2021-04-15"
update: "2021-04-15"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

# Methods

- 자바나 C처럼 강타입 언어는 컴파일러가 모든 메서드 호출에 대해 수신 객체가 일치하는 메서드를 갖고있는지 확인한다.
  - 정적 유형 검사라고 하며 정적 타입 언어가 이를 채택해서 사용함
- 파이썬이나 루비같은 동적 언어들은 컴파일러가 확인하지 않음
- 루비에서는 boilerplate method가 문제가 안되는데 이에 대해 알아보자~

## 중복 문제

- 99$를 이상을 쓰는 컴퓨터 장비를 찾기

### 레거시 시스템

- DS(Data Source)라는 이름의 클래스 뒤에 레거시 시스템에 데이터들이 저장되어있다

```ruby
class DS
  def initialize # connect to data source...
  def get_cpu_info(workstation_id) # ...
  def get_cpu_price(workstation_id) # ...
  def get_mouse_info(workstation_id) # ...
  def get_mouse_price(workstation_id) # ...
  def get_keyboard_info(workstation_id) # ...
  def get_keyboard_price(workstation_id) # ...
  def get_display_info(workstation_id) # ...
  def get_display_price(workstation_id) # ...
  # ...and so on
```

- `DS#initialize` 새 DS object를 만들 때 디비와 연결 된다.
- 다른 메서드들(수십 개의)은 워크스테이션 id를 갖고 컴퓨터 부품에 대한 설명과 가격을 반환한다.

```ruby
ds = DS.new
ds.get_cpu_info(42) # => "2.9 Ghz quad-core"
ds.get_cpu_price(42) # => 120
ds.get_mouse_info(42) # => "Wireless Touch"
ds.get_mouse_price(42)  # => 60
```

### Double, Treble,... Trouble

- 각 어플리케이션에 맞는 객체로 DB를 래핑해야한다.
- 즉, 각 컴퓨터가 객체여야 한다.
- 이 객체는 각 구성요소에 대해 단일 메서드를 갖고있고 해당 구성 요소의 가격을 모두 설명하는 문자열을 반환한다.
- 100$이상이면 주의를 끌기위해 별을 붙인다.

```ruby
#methods/computer/duplicated.rb

class Computer
  def initialize(computer_id, data_source)
    @id = computer_id
    @data_source = data_source
  end
  def mouse
    info = @data_source.get_mouse_info(@id)
    price = @data_source.get_mouse_price(@id)
    result = "Mouse: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
  def cpu
    info = @data_source.get_cpu_info(@id)
    price = @data_source.get_cpu_price(@id)
    result = "Cpu: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
  def keyboard
    info = @data_source.get_keyboard_info(@id)
    price = @data_source.get_keyboard_price(@id)
    result = "Keyboard: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
# ...
end
```

- 중복이 많다.
- 메서드가 많다
- 각 메서드에 대한 테스트를 작성해야한다.

## 동적 메서드

동적으로 메서드를 호출하고 정의하는 방법과 중복 코드를 제거하는 방법

### 함수 동적으로 호출하기

```ruby
class MyClass
  def my_method(my_arg)
    my_arg * 2
  end
end
obj = MyClass.new
obj.my_method(3)  # => 6
```

- 다른 방법으로 `MyClass#my_method` 대신 `Object#send` 을 사용할 수 있다.

```ruby
obj.send(:my_method, 3)
```

- 똑같이 my_method를 호출하지만 send를 사용해서 호출된다.
- send를 사용하면 호출할 메서드를 결정하기 위해 마지막까지 기다릴 수 있다.
- 이를 동적 디스패치라고 한다.

#### Pry 예시

- Pry는 irb의 좋은 대안 ( command line interpreter )
- Pry 객체는 인터프리터의 설정을 갖고있음 - memory_size나 quite같은

```ruby
require "pry"
pry = Pry.new
pry.memory_size = 101
pry.memory_size
pry.quiet = true
# => 101

Pry.memory_size # 각 속성의 기본값을 반환하는 메서드도 있다.
```

- Pry 인스턴스를 설정하려면 `Pry#refresh` 라는 메서드를 호출하면 된다.
- 속성 이름을 새 값에 매핑하는 해시를 사용

```ruby
pry.refresh(:memory_size => 99, :quiet => false)
pry.memory_size       # => 99
pry.quiet             # => false
```

- refresh는 할 일이 많음
  - 각 속성을 (self.memory_size 등) 검토하고 기본값으로 초기화해야하며
  - 해시 인수에 동일한 특성에 대한 새 값이 있나 확인 후 있으면 설정

```ruby

def refresh(options={})
  defaults[:memory_size] = Pry.memory_size
  self.memory_size = options[:memory_size] if options[:memory_size]
  defaults[:quiet] = Pry.quiet
  self.quiet = options[:quiet] if options[:quiet]
  # same for all the other attributes...
end

```

- 이 두 줄은 각 속성마다 반복되어야 한다.

```ruby
def refresh(options={})
  defaults   = {}
  attributes = [ :input, :output, :commands, :print, :quiet,
                 :exception_handler, :hooks, :custom_completions,
                 :prompt, :memory_size, :extra_sticky_locals ]
  attributes.each do |attribute|
    defaults[attribute] = Pry.send attribute
  end
  # ...
  defaults.merge!(options).each do |key, value|
    send("#{key}=", value) if respond_to?("#{key}=")
  end

  true
end
```

- send로 기본 값을 읽는다.
- 옵션 해시와 merge한다
- memory_size=value 꼴로 call attribute accessor을 사용
- respond_to? 는 Pry#memory_size= 이 있으면 true를 반환

#### Privacy Matters

- `Object#send` 는 private method를 포함하여 모든 메서드를 쓸수 있다.
- 이러한 종류의 캡슐화 위반.... 불편하면 `public_send` 를 사용한다.
- 하지만 야생의 루비코드는 이러한 우려를 거의 신경쓰지않음....
- 오히려 많은 루비 프로그래머들이 send를 private method쓰려고 씀...
- 동적 호출 봤고 동적 정의 보자~

### 메서드를 동적으로 정의하기

```ruby
class MyClass
  define_method :my_method do |my_arg|
    my_arg * 3
  end
end

obj = MyClass.new
obj.my_method(2)  # => 6

require_relative '../test/assertions'
assert_equals 6, obj.my_method(2)
```

- `Module#define_method` 를 사용, method name 하고 block만 넘기면 된다.
- `Myclass` 내에서 실행 되므로 MyClass의 인스턴스 메서드로 정의됨
- 동적 메서드라고 한다
- define_method 키워드를 쓰면 런타임에 정의된 메서드의 이름을 결정 가능

#### Computer 클래스 리팩터링

```ruby
class Computer
  def initialize(computer_id, data_source)
    @id = computer_id
    @data_source = data_source
  end
  def mouse
    info = @data_source.get_mouse_info(@id)
    price = @data_source.get_mouse_price(@id)
    result = "Mouse: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
  def cpu
    info = @data_source.get_cpu_info(@id)
    price = @data_source.get_cpu_price(@id)
    result = "Cpu: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
  def keyboard
    info = @data_source.get_keyboard_info(@id)
    price = @data_source.get_keyboard_price(@id)
    result = "Keyboard: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
# ...
end
```

**Step 1: 다이나믹 디스패치 추가**

```ruby
  class Computer
    def initialize(computer_id, data_source)
      @id = computer_id
      @data_source = data_source
    end
    def mouse
      component :mouse
    end
    def cpu
      component :cpu
    end
    def keyboard
      component :keyboard
    end
    def component(name)
      info = @data_source.send "get_#{name}_info", @id
      price = @data_source.send "get_#{name}_price", @id
      result = "#{name.capitalize}: #{info} ($#{price})"
      return "* #{result}" if price >= 100
      result
    end
end
```

- 각 메서드를 component 메서드에 위임한다.
- 하지만 아직도 중복이 많다.

**Step 2: 동적 메서드 정의**

```ruby
class Computer
  def initialize(computer_id, data_source)
    @id = computer_id
    @data_source = data_source
  end
  def self.define_component(name)
    define_method(name) do
      info = @data_source.send "get_#{name}_info", @id
      price = @data_source.send "get_#{name}_price", @id
      result = "#{name.capitalize}: #{info} ($#{price})"
      return "* #{result}" if price >= 100
      result
    end
  end
  define_component :mouse
  define_component :cpu
  define_component :keyboard
end

```

- 여기서 self는 Computer임
- `define_component`는 클래스 메서드

**Step 3: 인트로스펙션으로 뿌리기**

- 최소한의 중복만 있지만 완전히 제거가 가능하다.
- `define_component` 에 대한 호출을 다 지운다.
- 인트로스펙션으로 모든 컴포넌트의 이름을 추출한다..

```ruby
class Computer
  def initialize(computer_id, data_source)
    @id = computer_id
    @data_source = data_source
    data_source.methods.grep(/^get_(.*)_info$/) { Computer.define_component $1 }
  end
  def self.define_component(name)
    define_method(name) do
      #...
    end
  end
end
```

- 블록을 grep에 `$1` 에 저장 된다.
- 중복 코드가 다 사라졌다.
- 요소를 추가하거나 유지 관리할 필요가 없으며 DS에 새 컴포넌트를 추가하면 컴퓨터 클래스에서 자동으로 지원한다

## method_missing

- Ghost Method와 Dynamic Proxies...
- 루비에서는 컴파일러가 메서드 정의를 강제하지 않으니 없는 메서드를 호출할 수도있다.

```ruby
class Lawyer; end
nick = Lawyer.new
nick.talk_simple
❮ NoMethodError: undefined method `talk_simple' for #<Lawyer:0x007f801aa81938>
```

- 메서드 조회가 어떤식으로 진행되는지 기억하나?
  - nick의 클래스로 들어가 인스턴스 메서드를 탐색
  - Object로 이동한다음 ... BasicObject로 이동...
  - method_missing..

```ruby
nick.send :method_missing, :my_method
❮ NoMethodError: undefined method `my_method' for #<Lawyer:0x007f801b0f4978>
```

### Overriding method_missing

- unknown messages를 인터셉트하여 override가 가능하다
- 각 메시지는 `method_missing` 에서 함수 이름과 매개변수 그리고 호출시 불러진 블록을 포함한다.

```ruby
class Lawyer
    def method_missing(method, *args)
      puts "You called: #{method}(#{args.join(', ')})"
      puts "(You also passed it a block)" if block_given?
    end
end
  bob = Lawyer.new
  bob.talk_simple('a', 'b') do
# a block
end
❮ You called: talk_simple(a, b)
(You also passed it a block)
```

#### 고스트 메서드

- 유사한 메서드를 많이 정의해야 할 경우 method_missing을 통해 직접 정의를 내리고 호출에 응답할 수 있다.
- 만약 뭔가를 물었는데 이해 못하면 이렇게 하세요 라고 하는 것과 같다.
- 호출자 쪽에선 method_missing에 의해 처리되는 일반 호출처럼 보인다.
- 수신자에선 이에 상응하는 메서드가 없다..
- 이를 고스트메서드라고 한다.

##### The Hashie Example

- Hashie Gem.... Hashie::Mash ..
- Mash는 루비의 더 강력한 버전의 OpenStruct class
  - 루비의 변수처럼 동작하는 hash같은 객체
- 만약 새 속성이 필요하면 지정만 하면 사용이 가능함

```ruby
require 'hashie'
icecream = Hashie::Mash.new
icecream.flavor = "strawberry"
icecream.flavor                 # => "strawberry"
```

```ruby
module Hashie
  class Mash < Hashie::Hash
    def method_missing(method_name, *args, &blk)
      return self.[](method_name, &blk) if key?(method_name)
      match = method_name.to_s.match(/(.*?)([?=!]?)$/)
      case match[2]
      when "="
        self[match[1]] = args.first
      # ...
      else
        default(method_name, *args, &blk)
      end
    end
  # ...
  end
end
```

- method이름이 =으로 끝나면 method_missing은 속성의 값을 갖고오기 위해 '=' 을 잘라낸 다음 값을 저장.
- 호출된 메서드의 이름이 일치하지 않으면 기본값만 반환한다.

#### 다이나믹 프록시

- 고스트 메서드는 좋긴 한데 어떤 객체들은 거의 전적으로 의존함
- 이런 객체들은 다른 언어로 작성된 객체, 웹서비스 의 래퍼이기도 함
- 메서드 호출을 method_missing을 통해 수집하여 래핑된 객체에 전달한다.

##### The Ghee Example

- Ghee를 통해 gist에 접근하는 방법

```ruby
require "ghee"
gh = Ghee.basic_auth("usr", "pwd")  # Your GitHub username and password
all_gists = gh.users("nusco").gists
a_gist = all_gists[20]

a_gist.url            # => "https://api.github.com/gists/535077"
a_gist.description    # => "Spell: Dynamic Proxy"

a_gist.star
```

- nusco의 gist를 찾아 측정 gist를 선택
- url, desc를 찍고 star를 남김
- github의 api는 gist 외에도 수십 가지 유형의 객체를 노출한다.
- ghee는 이 모든 객체를 지원해야한다

```ruby
class Ghee
  class ResourceProxy
  # ...
    def method_missing(message, *args, &block)
      subject.send(message, *args, &block)
    end
    def subject
      @subject ||= connection.get(path_prefix){|req| req.params.merge!params }.body
    end
  end
end

```

- 먼저 어떻게 사용하는지를 알아야함
- github의 각 유형에 Ghee는 하위 클래스를 정의한다. ( `Ghee::ResourceProxy`)

```ruby
class Ghee
  module API
    module Gists
      class Proxy < ::Ghee::ResourceProxy
        def star
          connection.put("#{path_prefix}/star").status == 204
        end
# ...
      end
    end
end
```

- 만약 객체의 상태를 변경하는 메서드를 호출할 때 ( star처럼 ) Ghee는 해당 github url http 호출을 한다.
- 하지만 url이나 desc같이 속성에서 읽기만 하는 호출은 `Ghee::ResourceProxy#method_missing`에서 끝난다.
- missing_method는 메시지를 subject에게 포워드한다.
- subject의 구현을 자세히 보면 이 메서드가 github api http 호출을 한다.
- JSON형식의 github 객체를 받아서 해시 같은 객체로 변환함
- 그럼 다시 method_missing에서 url attribute를 반환함

음 우아하지만 메타프로그래밍이 너무 많이 들어가 있어서 헷갈린다.

1. Ghee는 github 객체를 동적 해시로 저장한다. 액세스 할 수있다.
2. Ghost Method를 호출하여 이러한 해시 특성을 확인할 수 있다.
3. Ghee는 또한 이러한 해시를 프록시 객체 안에 래핑하여 추가적인 메소드를 통해 더욱 풍부하게 한다.
   - 프록시는 특정 코드가 필요한 메소드를 구현 ( star 처럼 )
   - url과 같이 데이터만 읽는 메서드를 래핑된 해시에 전달

이러한 2단계 디자인 덕에 코드를 매우 압축적으로 유지한다.

github api 의 변화에 자동 적응

#### Refactoring the Computer Class (Again)

```ruby
class Computer
  def  initialize(computer_id, data_source)
    @id = computer_id
    @data_source = data_source
  end
  def method_missing(name)
    super if !@data_source.respond_to?("get_#{name}_info")
    info = @data_source.send("get_#{name}_info", @id)
    price = @data_source.send("get_#{name}_price", @id)
    result = "#{name.capitalize}: #{info} ($#{price})"
    return "* #{result}" if price >= 100
    result
  end
end

```

#### respond_to_missing?

- 만약 컴퓨터에 respond_to? 를 사용하면 ..

```ruby
cmp = Computer.new(0, DS.new)
cmp.respond_to?(:mouse)       # => false
```

- 문제가 될 수 있음
- 다행히 이를 위한 메커니즘

```ruby
class Computer
  def respond_to_missing?(method, include_private = false)
    @data_source.respond_to?("get_#{method}_info") || super
  end
end
```

### const_missing

- Rake에서 충돌 가능성이 높은 클래스 이름을 모듈로 변경했다는 것..
- 이름 변경 후 이전 버전, 현재 버전 몽키패치

```ruby
class Module
    def const_missing(const_name)
      case const_name
      when :Task
        Rake.application.const_warning(const_name)
        Rake::Task
      when :FileTask
        Rake.application.const_warning(const_name)
        Rake::FileTask
      when :FileCreationTask
    end
  end
end
```

- 존재하지 않는 상수를 참조할 때 루비는 상수의 이름을 심볼로 전달
- 클래스 이름은 상수이므로 ...
- 더이상 사용되지 않는 클래스 이름을 사용중임을 경고

```ruby
require 'rake'
  task_class = Task
❮ WARNING: Deprecated reference to top-level constant 'Task' found [...] Use --classic-namespace on rake command
or 'require "rake/classic_namespace"' in Rakefile

task_class # => Rake::Task

```

### 리팩터링 마무리

- 두 가지 다른 방법으로 풀었다.
- 동적 메서드와 동적 디스패치를 사용
- 고스트 메서드를 사용

## 빈 슬레이트

- 디스플레이가 작동하지 않는다..

```ruby
my_computer = Computer.new(42, DS.new).
my_computer.display # => 0
Object.instance_method.grep /^d/ #=> [:dup, display, ...]
```

- 이미 있으므로 metho_missing에 도달하지 않는다.

### BasicObject

- 베이직오브젝트는 소수의 인스턴스 메서드만 있음

```ruby
im = BasicObject.instance_methods
im # => [:==, :equal?, :!, :!=, :instance_eval, :instance_exec, :__send__, :__id__]
```

- 슈퍼 클래스를 지정하지 않으면 Object에서 상속되며
- 빈 슬레이트를 원하면 대신 BasicObject에서 직접 상속할 수 있다.
- 하지만 특정 메서드를 제거하는게 더 빠를때도

### Removing Methods

- `Module#undef_method` 혹은 `Module#remove_method` 를 사용하여 클래스에서 메서드를 제거할 수 있음
- `undef_method` 는 상속된 메서드를 모함한 모든 메서드를 제거함

#### The Builder Example

- Builder gem은 XML 제너레이터

```ruby
require 'builder'
  xml = Builder::XmlMarkup.new(:target=>STDOUT, :indent=>2)
  xml.coder {
    xml.name 'Matsumoto', :nickname => 'Matz'
    xml.language 'Ruby'
}
#This code produces the following snippet of XML:
❮ <coder>
<name nickname="Matz">Matsumoto</name> <language>Ruby</language>
</coder>
```

- 빌더는 중첩된 태그, 속성 등을 지원하기위해 ...
- 핵심 아이디어는 이름과 언어와 같은 호출은 모든 호출에 대해 XML태그를 생성하는 `XmlMarkup#method_missing` 에 의해 처리됨

```ruby
xml.semester {
  xml.class 'Egyptology'
  xml.class 'Ornithology'
}
❮ <semester> <class>Egyptology</class> <class>Ornithology</class>
</semester>
```

XmlMarkup이 Object의 하위 클래스인 경우 충돌하지만 메서드를 제거하는 Blank Slate를 상속함

```ruby
  class BlankSlate
    # Hide the method named +name+ in the BlankSlate class.  Don't
    # hide +instance_eval+ or any method beginning with "__".
    def self.hide(name)
      # ...
      if instance_methods.include?(name._blankslate_as_name) &&
          name !~ /^(__|instance_eval$)/
        undef_method name
      end
    end
# ...
    instance_methods.each { |m| hide(m) }
end
```

- 모든 메서드를 다 제거하진 않는다? instance_eval하고 루비에 의해 예약 메소드를 보관 - send
- 제거는 가능하지만 제거 안함

### Computer Class 고치기

```ruby
class Computer < BasicObject
```

BasicObject에는 `response_to?` 가 없음

`response_to_missing` 다시 제거

## 마무리

- 동적 메서드 및 독적 디스패치로 리팩토링 하였고
- 고스트 메서드로도 수정함,
- 고스트 메서드는 위험할 수 있음
  - super를 항상 호출 하고, response_to_missing 재정의 를 하면 방지
  - 가끔 버그를 일으킬 수 있음
  - 메서드목록에서 반환 안됨
- 하지만 고스트 메서드가 유일한 실행 가능한 선택일수도..
- 메서드가 많거나 런타임에 필요한 메서드 호출을 모를때
- Builder - XML 예제처럼
- 스타일에 따라 다르긴 하겠지만 의심스러우면 동적 방법, 필요하면 고스트
