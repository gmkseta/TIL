---
title: M Ruby - 4. Blocks
date: "2021-04-22"
update: "2021-04-22"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

# Blocks

- 블록은 스코프를 제어하기 위한 강력한 도구
- 블록은 단지 호출 가능한 객체의 큰 구성원
- 블록을 저장하고 나중에 실행하는 등 이런 객체와 다른 호출 가능한 객체를 최대한 활용하는 방법 설명 예정

## The Day of the Blocks

### Roadmap

- 블록 기초
- 범위 개요 및 블록 클로져를 사용한 변수의 범위 이동
- 블록을 호출 가능한 객체로 변환하여 따로 두는 방법, Procs나 람다처럼 나중에 호출

### The Basics of Blocks

```ruby
def a_method(a, b)
  a + yield(a, b)
end

a_method(1, 2){ |x, y| (x+y)*3} #=> 3
```

- 중괄호나 `do..end` 로 정의할 수 있다.
- 메서드를 호출할 때만 블록을 정의 가능
- 블록은 메서드로 바로 전달되며 메소드는 `yield` 키워드로 블록을 다시 호출 가능
- 블록은 인수를 가질수도 있다. 예시처럼 인수를 제공 가능
- 블록은 메서드처럼 마지막 줄을 반환
- `Kernel#block_given?` 으로 블록이 포함되어 있는지 확인 가능

```ruby
def a_method
  return yield if block_given?
  'no block'
end
a_method
a_method { "here's a block!" }
# => "no block"
# => "here's a block!"
```

## Blocks Are Closures

- 코드가 실행할 때 지역변수, 인스턴스 변수, 셀프등이 필요..
- 코드와 바인딩으로 이뤄져서 뭔가 실행되는 것
- 이런 엔티티들은 객체에 바인딩된 것이므로 바인딩이라고 부르겠다?
- 블록이 어디서 바인딩을 주워오는지....
- 블록을 정의하는 순간 바인딩을 잡은 다음 블록을 메서드로 전달할 때... 함께 바인딩을 전달한다..

```ruby
def my_method
  x = "Goodbye"
  yield("cruel")
end
x = "Hello"
my_method {|y| "#{x}, #{y} world" } # => "Hello, cruel world"
```

- 블록을 생성할 때 x같은 로컬 바인딩을 캡쳐한다.
- 블록을 별도의 바인딩 집합이 있는 메서드로 전달한다.
- 여전히 블록의 코드는 블록에서 아예 안보이는 메서드의 x가 아닌 블록이 정의되었을 떄 있었던 x를 본다.

```ruby
def just_yield
  yield
end
top_level_variable = 1
just_yield do
  top_level_variable += 1
  local_to_block = 1
end
top_level_variable  # => 2
local_to_block      # => Error!
```

- 블록 내에서 추가 바인딩 정의도 가능하지만 블록 이후에 사라짐
- 이런 특성때문에 블록을 클로져라고 하기도 하는듯
- 다른 사람들은 블록이 로컬바인딩을 캡쳐하여 옮긴다고 함
- 클로져를 실제로 어떻게 쓸까? 이를 이해하려면 바인딩의 위치, 즉 범위를 자세히 쌀펴야한다.

### Scope

#### Changing Scope

- `Kernel#local_variables` 를 통해 바인딩의 이름을 추적하여 스코프 보는 예시

```ruby
v1 = 1
class MyClass
  v2 = 2
  local_variables # => [:v2]
  def my_method
    v3 = 3
    local_variables
  end
  local_variables # => [:v2]
end
obj = MyClass.new
obj.my_method # => [:v3]
obj.my_method # => [:v3]
local_variables # => [:v1, :obj]

```

- 루비에서는 자바나 C#처럼 내부의 스코프에서 외부의 스코프를 볼수있게 하지 않음, 즉 뚜력하게 구분됨
- 새로운 범위를 들어가자마자 새로운 바인딩으로 대체됨
- 클래스 내에서 v1이 다시 표시 안되는 것 처럼
- 정의 끝날때까지.... 스코프 닫히고 다시 최상위로...
- 만약 my_method를 재정의? 당연히 새 바인딩 세트

### Scope Gates

- 이전 스코프를 버리고 새 스코프를 여는 위치
  - Class definitions
  - Module definitions
  - Methods

```ruby
v1 = 1
class MyClass # SCOPE GATE: entering class
  v2 = 2
  local_variables # => ["v2"]
  def my_method # SCOPE GATE: entering def
    v3 = 3
    local_variables
  end# SCOPE GATE: leaving def
  local_variables # => ["v2"]
end # SCOPE GATE: leaving class
obj = MyClass.new
obj.my_method # => [:v3]
local_variables # => [:v1, :obj]
```

- 클래스나 모듈은 즉시 코드가 실행 됨
- 메서드는 메서드 호출 시 실행됨
- 바인딩이 변하는 위치를 알았는데 만약 변수를 하나 넘기고싶다면?

### Flattening the Scope

```ruby
my_var = "Success"
  class MyClass
    # We want to print my_var here...
    def my_method
      # ..and here
    end
  end

```

- my_var을 두 개의 장벽을 거쳐서 어떻게 전달하지..?

```ruby
 my_var = "Success"
➤ MyClass = Class.new do
➤ # Now we can print my_var here...
➤ puts "#{my_var} in the class definition!"
    def my_method
      # ...but how can we print it here?
    end
end
```

- Class를 Scope Gate가 아닌 메서드 호출로 바꿔서 전달한다면?
- 이제 메서드에 전달하려면..?

```ruby
my_var = "Success"
MyClass = Class.new do
  "#{my_var} in the class definition"
  define_method :my_method do
    "#{my_var} in the method"
  end
end
MyClass.new.my_method

require_relative "../test/assertions"
assert_equals "Success in the method", MyClass.new.my_method

Success in the class definition
Success in the method
```

- Scope Gate를 메서드호출로 변경하면 한 스코프가 다른 스코프의 변수를 볼 수 있다.
- 엄밀히 말하면 이걸 nested lexical scopes라고 부르고, 루비 코더들은 flattening the scope라고 함
- flat scope

#### Sharing the scope

- 저거 알면 이제 스코프로 하고싶은거 다 할 수 있다.
- 만약 몇 가지 메서드 간에 변수를 공유, 다른 사람이 해당 변수를 못하도록

```ruby
def define_methods
  shared = 0
  Kernel.send :define_method, :counter do
    shared
  end
  Kernel.send :define_method, :inc do |x|
    shared += x
  end
end

define_methods

counter       # => 0
inc(4)
counter       # => 4
```

- 두개의 커널 메서드를 정의함
- `Kernel#counter`, inc는 공유변수를 사용 가능
- 하지만 다른 메서드에서는 확인 불가능
- 이 공유 스코프는 실제로 많이 사용되지 않지만, 강력한 트릭이자 스코프으 ㅣ힘을 보여주는 에시
- 스코프게이트, 플랫 스코프 및 공유 스코프를 함께 쓰면 스코프를 비틀거나 구부려서 원하는 위치에서 필요한 변수를 정확하게 확인 가능

### Clousure Wrap Up

- 각 스코프에는 여러 바인딩이 포함, 스코프는 스코프 게이트로 구분 된다 - class module def
- 만약 Scope Gate를 통해 바인딩된 변수를 전달하려면 블록을 쓸 수 있다.
- 블록은 클로져다, 블록을 정의하면 현재 환경에서 바인딩을 캡쳐하여 이동한다.
- 따라서 Scope Gate를 메서드 호출로 바꾸고 클로저의 현재 바인딩을 캡쳐하고 클로져를 메서드로 전달 가능
- Class.new, Module,new def를 Module define_method로 변경 가능
- 기본적인 클로저 관련 매쥑 플랫 스코프
- 스코프 게이트로 보호되는 동일한 플랫 스코프에서 여러 메서드를 정의하는 경우 이런 메서드가 바인딩 공유 가능 - 공유 스코프

## instance_eval()

- 컨텍스트에서 블록을 eval하는 `BasicObject#instance_eval`

```ruby
class MyClass
  def initialize
    @v = 1
  end
end
obj = MyClass.new
obj.instance_eval do
  self        # => #<MyClass:0x3340dc @v=1>
  @v          # => 1
end
```

- 블록은 리시버를 self로 해서 같이 evaluated 하므로 private method, instance variables에 접근이 가능하다.

```ruby
v=2
obj.instance_eval { @v = v }
obj.instance_eval { @v } # => 2
```

- instance_eval로 전달된 블록은 다른 블록처럼 해당 위치에서의 바인딩.
- Flat Scope에서 evaluated되므로 .... v도 접근되고 @v도 접근이 가능
- instance_eval로 전달되는 블록을 context probe라고 함?!
  - 코드 조각이 객체 내부에서 동작....하는것...같이...

### Breaking Encapsulation

- Context Probe를 쓰면 캡슐화에 큰 피해
- 실용적으로는 캡슐화가 방해되는 상황이 있다...?
- 캡슐화를 깨는 또 다른 납든할 수 있는 이유는 거의 테스트!

#### The Padrino Example

- Padrino 는 Logger class를 정의함
- Logger는 설정을 인스턴스 변수에 저장함
- Padrino의 테스트는 응용프로그램의 로거 구성을 변경해야한다.
- 새 로거를 만들고 구성하는 문제를 겪지 않고 context probe를 사용하여 구성을 변경한다.

```ruby
describe "PadrinoLogger" do
  context 'for logger functionality' do
    context "static asset logging" do
      should 'not log static assets by default' do
        # ...
        get "/images/something.png"
        assert_equal "Foo", body
        assert_match "", Padrino.logger.log.string
      end
      should 'allow turning on static assets logging' do
        Padrino.logger.instance_eval{ @log_static = true }
        # ...
        get "/images/something.png"
        assert_equal "Foo", body
        assert_match /GET/, Padrino.logger.log.string
        Padrino.logger.instance_eval{ @log_static = false }
      end
    end
    # ...
```

- 첫 테스트는 아무것도 기록하지 않는 것을 확인
- 두 번째 테스트에서는 instance_eval로 로거의 구성을 변경하고 정적 파일 로깅을 활성화
- 기록을 확인하고, 다시 비활성화
- 루비의 다른 많은 것들과 마찬가지로 캡슐화는 무시할 수 있는 유연한 도구이며 이러한 위험을 받아들일지... 는 우리에게 달려있다.

### Clean Rooms

- 단지 객체를 생성한다 블록 안을 evaluate하기위해?
- 이 객체는 Clean Room이라고 불린다.

```ruby
class CleanRoom
  def current_temperature
   # ...
  end
end
clean_room = CleanRoom.new
clean_room.instance_eval do
  if current_temperature < 20
    # TODO: wear jacket
  end
end
```

- 클린 룸은 클록을 eval 할 수 있는 환경일 뿐
- 이상적인 클린룸은 메서드 및 인스턴스 변수가 많지 않음 - 블록과 충돌때문에..?
- BasicObject의 인스턴스는 Blank Slates이므로 좋은 클린룸을 제공한다.
  - 너무 깨끗해서 String같은 표준 루비 상수도 없음. 절대경로 써야함 ::String 처럼

## Callable Objects

- 블록 사용은 두 단계의 과정
  - 일부 코드를 따로 두고
  - 블록을 호출하여 실행
- "코드 패키지 우선, 나중에 호출"은 블록에만 국한된 게 아니다
- proc 블록은 객체로 변경된 블록
- lambda proc을 약간 변형한 것
- methods

### Proc Objects

- 루비의 대부분은 객체지만 블록은 아니다?
- 뭔 상관? -> 블록을 저장하고 나중에 쓰려한다. 그러려면 객체가 필요함
- 이 문제를 해결하기위해 Proc, 객체로 변환된 블록임

```ruby
inc = Proc.new {|x| x + 1 }
# more code...
inc.call(2) # => 3
```

- Deferred Evaluation이라 함
- 몇 가지 방법이 더 있음
- lambda 로 만드는 것은 조금 차이가 있지만 대부분 원하는 것을 얻을 수 있다.

```ruby
dec = lambda {|x| x - 1 }
dec.class # => Proc
dec.call(2) # => 1
p = ->(x) { x+ 1 } #=> called stabby lambda operator
```

### The & Operator

- 메서드로 블록을 넘겨서 사용하는 경우 대부분 yield로 충분하지만, 아닌 경우도 있음
  - 블록을 다른 메서드에게 넘기고 싶다거나
  - 블록을 Rroc로 변환하고싶다거나
- 둘다 모두 블록을 사용하겠다고 말 해줘야함, - 블록을 바인딩하기 위해서는 "&" 가 필요함
- 인수 목록의 마지막이여야 하고 &기호를 사용해야함

```ruby
def math(a, b)
  yield(a, b)
end
def do_math(a, b, &operation)
  math(a, b, &operation)
end
do_math(2,3){|x,y|x*y} #=>6
```

- & 의 뜻은 "나는 이 메서드로 전달되는 블록을 Proc으로 바꾸고 싶다" 라는 뜻이다.

```ruby
def my_method(&the_proc)
  the_proc
end
p = my_method {|name| "Hello, #{name}!" }
p.class         # => Proc
p.call("Bill")  # => "Hello, Bill!"
```

- 바로 리턴해보면 Proc임
- 다시 Proc을 블록으로 변경하고 싶다면? &를 또 쓰면 댐?

```ruby
def my_method(greeting)
  "#{greeting}, #{yield}!"
end
my_proc = proc { "Bill" }
my_method("Hello", &my_proc)
```

- &는 my_proc을 블록으로 변환하고 그 블록을 메서드로 전달한다.

### The Higline example

- 콘솔 입력 및 출력을 자동화 하는 잼
- 쉼표로 구분된 사용자 입력을 수집하여 배열로 분할 가능

```ruby
require 'highline'
hl = HighLine.new
friends = hl.ask("Friends?", lambda {|s| s.split(',') })
puts "You're friends with: #{friends.inspect}"
❮ Friends?
➾ Ivana, Roberto, Olaf
❮ You're friends with: ["Ivana", " Roberto", " Olaf"]
```

- `HighLine#ask` 는 post processing 코드를 Proc으로 받아서 쓴다.
- 왜 블록이 아닌 Proc이냐? - 다른 HighLine 메커니즘을 위해 예약되어있음

```ruby
 name = hl.ask("Name?", lambda {|s| s.capitalize })
   puts "Hello, #{name}"
❮ Name?
➾ bill
❮ Hello, Bill
```

### Procs vs Lambdas

- 미묘하게 다른데 많이 혼란스러울 것 이다.
- 대략적인 중요한 차이점 두가지
  - 반환 키워드와 관련
  - 인수 확인과 관련

#### Procs, Lambdas and return

- 리턴 키워드가 다른 것을 의미한다

```ruby
def double(callable_object)
  callable_object.call * 2
end
l = lambda { return 10 }
double(l) # => 20

def another_double
  p = Proc.new { return 10 }
  result = p.call
  puts result
  return result * 2  # unreachable code!
end
another_double # => 10
```

```ruby
p = Proc.new { return 10 }
double(p)     # => LocalJumpError
p = Proc.new { 10 }
double(p)     # => 20
```

- proc.call 하는 순간 그 리턴코드가 리턴 되어버리네...
- 블록이 언랩되는 느낌인가?

#### Procs, Lambdas, and Arity

- 두 번째 차이점은 argument를 확인하는 것

```ruby
p = Proc.new {|a, b| [a, b]}
p.call(1, 2, 3)   # => [1, 2]
p.call(1)         # => [1, nil]
l = ->(a,b){ [a,b]}
l.call(1,2,3) # => ArgumentError: wrong number of arguments (given 3, expected 2)
l.call(1) # => ArgumentError: wrong number of arguments (given 1, expected 2)
```

- 람다는 에러, Proc은 초과인수 버림

- 일반적으로 람다를 많이

### Method Objects

```ruby
class MyClass
  def initialize(value)
    @x = value
  end
  def my_method
    @x
  end
end
object = MyClass.new(1)
m = object.method :my_method
m.call
```

- `Kernel#method` 로 메서드 자체를 메서드 객체로 얻을 수 있다.
- 호출도 가능함.
- ruby 2.1부터는 `Kernel#singleton_method` 라는 것도 있다는데..
- Proc이랑 Lambda랑 유사 하지만... 중요한 차이
- Lambda는 정의된 범위에서 eval
- 메서드는 객체의 범위 에서 eval

#### Unbound Methods

- 클래스 또는 모듈에서 분리된 메서드
- `Metdhod#unbind`를 통해서 메서드를 Unbound 메서드로 만들 수 있음
- instance_method로도 만들 수 있음

```ruby
module MyModule
  def my_method
    42
  end
end
unbound = MyModule.instance_method(:my_method)
unbound.class              # => UnboundMethod
```

- unbound method를 호출할 순 없지만 호출할 수 있는 일반 메서드르 생성하는 데 사용 가능하다.
- bind를 사용하여 객체에 바인딩 하면 된다.
- 기존에는 클래스에서 가져온 동일한 클래스의 객체에만 바인딩 가능했지만 2.0부터는 다됨.

```ruby
String.class_eval do
  define_method :another_method, unbound
end
"abc".another_method # => 42
```

- 매우 특이한 케이스에만 사용됨

##### The Active Support Example

- Active Support는 여러 유틸 중에서 해당 파일에 정의된 상수를 사용할 떄 자동으로 Ruby 파일을 로드하는 클래스 및 모듈 세트가 포함되어 있다.
- 이 "Autoloading" 시스템은 `Kernel#load` 함수를 재정의 하는 Loadable이라는 모듈을 포함한다.
- 클래스에 Loadable이 포함된 경우 Loadable#load는 상위 체인의 Kernel#load보다 낮아진다.
- 따라서 Loadable#load가 호출 됨
- 경우에 따라 Loadable#load를 제거하고 바닐라 Kernel#load를 사용하기도 하는데
- 루비에는 언 인클루드가 없으므로 조상을 제거할 수 없다. 이럴떄..

```ruby
module Loadable
  def self.exclude_from(base)
    base.class_eval { define_method(:load, Kernel.instance_method(:load)) }
  end

  #...
```

- unboundmethod의 좋은 예고, 구체적인 문제에 대한 솔루션이기도 함
- 즉 두 개의 로드 메서드가 동일하고 혼란스럽게 만드는 솔루션..

## Callable Objects Wrap-Up

- evaluate 가능한 코드 조각, 고유한 스코프를 가짐
- Blocks - (objects는 아니지만 callable함 ) - 정의된 스코프 내에서 evaluated
- Procs - Proc 클래스 객체임 블록과 마찬가지로 정의된 범위 내에서 eval
- Lambdas - 똑같이 Procs의 객체지만 약간 다름, 똑같이 클로저고 정의되는 범위 안에서 eval
- Method - 객체에 바인딩 된 메서드는 해당 객체의 범위 안에서 eval, 리바인드 가능,

각 오브젝트 마다 미묘하게 다른 동작이 나타난다.

메서드와 람다는 callable object로부터 반환하는 반면 Procs와 Block은 호출 가능한 객체의 원래 컨턱스트에서 반환을 한다.

또한 다른 아리티를 가진 호출에 대해 다르게 반응한다.

메서드가 더 엄격, 람다가 그만큼 엄격, 프록과 블록이 덜 엄격

그럼에도 & 로 각 객체들이 변환 가능

## Writing a Domain-Specific Language

- RedFlag라는 영엄부 직원을 위한 모니터링 유틸리티
- 주문이 늦을 때 총 매출이 너무 낮을 때 기본적으로 여러 가지 일이 발생할 때마다 메시지
- DSL정도만 작성하면 된다.

```ruby
event "we're earning wads of money" do
    recent_orders = ...   # (read from database)
    recent_orders > 1000
end
```

- true 반환 시 메일, false는 패스
- 시스템은 몇 분마다 모든 이벤트를 확인

### Your First DSL

```ruby
 def event(description)
    puts "ALERT: #{description}" if yield
end
load 'events.rb'
```

```ruby
event "an event that always happens" do
  true
end
event "an event that never happens" do
  false
end
```

### Sharing Among Events

- 이벤트를 작성하는 사람들은 이벤트 간에 데이터를 공유하고 싶어할 것이다...
- DSL로 될까?두 개의 개별 이벤트가 동일한 변수에 액세스할 수 있나?

```ruby
def monthly_sales
  110   # TODO: read the real number from the database
end
target_sales = 100
event "monthly sales are suspiciously high" do
    monthly_sales > target_sales
end
  event "monthly sales are abysmally low" do
    monthly_sales < target_sales
end

```

- flat scope가 있지~

```ruby
❮ ALERT: monthly sales are suspiciously high
```

- 하지만 변수들이 최상위 범위를 혼란스럽게 함.

```ruby
setup do
    puts "Setting up sky"
    @sky_height = 100
end
setup do
    puts "Setting up mountains"
    @mountains_height = 200
end
event "the sky is falling" do
    @sky_height < 300
end
event "it's getting closer" do
    @sky_height < @mountains_height
end
event "whoops... too late" do
    @sky_height < 0
end

# Setting up sky
#Setting up mountains
#ALERT: the sky is falling
#Setting up sky
#Setting up mountains
#ALERT: it's getting closer
#Setting up sky
#Setting up mountains

```

- 세 이벤트 각각 이전의 모든 설정을 실행한다.
- @변수로 , 이벤트가 변수를 읽을 수 있음
- 모든 공유변수는 설정에서 초기화되고 이벤트에서 사용되므로 변수를 쉽게 추적 가능

```ruby
def event(description, &block)
  @events << {:description => description, :condition => block}
end
@events = []
load 'events.rb'
```

- 새 이벤트 메서드는 이벤트 조건을 블록해서 Proc으로 변환,
- 이벤트의 설명과 proc을 해시에 래핑하고 이벤트 배열에 저장
- 배열은 글로벌 변수 및 최상위 인스턴스 변수이므로 이벤트 메서드 외부에서 초기화할 수 있다.

```ruby
def setup(&block)
  @setups << block
end
def event(description, &block)
  @events << {:description => description, :condition => block}
end
@setups = []
@events = []
load 'events.rb'
@events.each do |event|
  @setups.each do |setup|
    setup.call
  end
  puts "ALERT: #{event[:description]}" if event[:condition].call
end
```

- 하지만 setups과 events는 글로벌 변수같다..

### Removing the "Global" Varaibles

- Shared scope?

```ruby
lambda {
  setups = []
  events = []
  Kernel.send :define_method, :setup do |&block|
    setups << block
end
  Kernel.send :define_method, :event do |description, &block|
    events << {:description => description, :condition => block}
end
  Kernel.send :define_method, :each_setup do |&block|
    setups.each do |setup|
      block.call setup
end end
  Kernel.send :define_method, :each_event do |&block|
    events.each do |event|
      block.call event
end end
}.call

load 'events.rb'
each_event do |event|
  each_setup do |setup|
setup.call
end
  puts "ALERT: #{event[:description]}" if event[:condition].call
end
```

- 추악한 글로벌 변수들은 사라졌지만...
- 예전처럼 간단하진 않다

### Adding a Clean Room

```ruby

event "define a shared variable" do
  @x = 1
end
event "change the variable" do
  @x = @x + 1
end

```

- 이벤트가 설정을 통해 변수를 공유하기를 원하지만 이벤트가 서로의 변수를 공유할 필요는 없다.
- 기능인지 버그인지는 우리에게 달려있다.
- 이벤트가 가능한 독립적으로 동작해야한다면 클린룸에서 실행 가능

```ruby
each_event do |event|
  env = Object.new
  each_setup do |setup|
    env.instance_eval &setup
  end
  puts "ALERT: #{event[:description]}" if env.instance_eval &(event[:condition])
end
```

- 이제 해당 설정은 클린룸 역할을 하는 오브젝트의 컨텍스트에서 eval된다
- 설정 및 이벤트의 인스턴스 변수는 최상위 인스턴스 변수가 아니라 클린룸의 인스턴스 변수
- 최상위 인스턴스 변수가 아닌 클린룸의 인스턴스 변수이므로 .. 이벤트는 인스턴스 변수를 공유 못함
- BasicObject를 사용할 수도 있지만 일반적인 메서드가 없음.

## Wrap Up

- Scope Gate가 무엇인지
- 플랫 스코프와 공유 스코프를 사용하여 범위를 통해 바인딩을 표시하는 방법
- 객체의 범위 - instance_eval, instance_exec 또는 클린룸에서 코드를 실행하는 방법
- 블록을 객체(Proc)로 반환하고 돌리는 방법
- 메소드를 객체로 (Method, UnboundMethod)로 변환하는 방법 및 되돌리기
- Callable Object 유형간의 차이
-
