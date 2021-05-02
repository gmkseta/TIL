---
title: M Ruby - 6. Code That Writes Code
date: "2021-05-02"
update: "2021-05-02"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

* 메타프로그래밍은 단문장으로 정의할 수 있는 접근법이 아니다.
* 여태 배운 트릭들을 잘 조합해서 어떻게 문제들을 해결하는지에 대한 장

## 

## 과제

```ruby
class Person
 >> include CheckedAttributes
  attr_checked :age do |v|
    v >= 18
	end 
end
me = Person.new
me.age = 39# OK
me.age = 12# Exception
```

* attr_accessor 처럼 클래스 매크로 `attr_checked`
* 모든 클래스에서 사용하여 더럽게 만드는 것 보단...
  * CheckedAttributes모듈을 포함하는 경우에 클래스가 사용 가능

## 계획

1. add_checked_attribute라는 Kernel method 메서드를 eval을 통해 추가한다. - 단순한 유효성 검사 어트리뷰트를 클래스에 추가
2. eval을 제거하기 위해 add_checked_attribute를 리펙터링한다
3. 블록을 통해 속성을 유효성 검증 한다.
4. add_checked_attributes를 attr_checked라는 클래스 매크로로 변경한다. 모든 클래스에서 사용 가능
5. 모듈을 추가해서 선택된 클래스만 사용 가능하게 한다.

## Kernel#eval

* instance_eval, class_eval을 이전에 배웠지? Kernel#eval 도 있다

```ruby
array = [10, 20]
el = 30
eval("array << el") # => [10,20,30]
```

* 위의 예시는 의미가 없지만 코드 문자열을 즉시 evaluate하는건 의미가 있다

### REST client 예시

* `gem install rest-client` 
* REST Client는 간단한 http 클라이언트 라이브러리이다.
* http 메서드와 함께 일반 루비 명령을 실행할 수 있는 인터프리터가 포함

```ruby
restclient http://www.twitter.com
   > html_first_chars = get("/")[0..14]
   => "<!DOCTYPE html>"


module RestClient
  class Resource
    def get(additional_headers={}, &block) # ...
    def post(payload, additional_headers={}, &block) # ...
    def put(payload, additional_headers={}, &block) # ...
    def delete(additional_headers={}, &block) # ...
```

* 소스를 보면 네 가지의 기본 HTTP 메서드가 리소스 클래스에 정의되어 있다.
* 인터프리터에서 이 메서드들을 사용할 수 있도록 특정 url의 리소스 메서드에 위임하는 최상위 메서드를 정의한다.

```ruby
def  get(path, *args, &b)
  r[path].get(*args, &b)
end
```

* 하지만 이런 것들을 일일이 정의하는 것이 아닌

```ruby
POSSIBLE_VERBS = ['get', 'put', 'post', 'delete']
POSSIBLE_VERBS.each do |m|
  eval <<-end_eval
    def  #{m}(path, *args, &b)
        r[path].#{m}(*args, &b)
		end 
	end_eval
end
```

* here document - heredoc  이라고 알려진 구문을 사용
* <<- 시퀀스로 시작하여 end_eval로 끝나는데
* <<- end_eval 은 end_eval이라는 문구가 나오면 끝난다는 것

### Binding Objects

* 바인딩은 객체로 패키지된 전체 스코프이다.
* 바인딩을 생성해서 로컬 스코프를 캠쳐하고, 이동할 수 있다는 아이디어
* 나중에 바인딩 객체를 eval과 함께 사용하여 해당 스코프에서 코드를 실행할 수 있다.

```ruby
class MyClass
  def my_method
		@x = 1
		binding
	end 
end
b = MyClass.new.my_method
```

* 바인딩 객체는 스코프를 포함하지만 코드는 포함하지 않는다, 따라서 블록보다 순수한 형태의 클로저라고 생각할 수 있다.
* 바인딩을 evaluate할 추가 인수로 전달하여 캡쳐된 스코프의 코드를 eval 가능

```ruby
eval "@x", b       # => 1
```



* TOPLEVEL_BINDING이라는 미리 정의된 상수, 최상위 스코프의 바인딩

```ruby
class AnotherClass
  def my_method
    eval "self", TOPLEVEL_BINDING
  end
end
AnotherClass.new.my_method    # => main
```



* 이런 바인딩 오브젝트를 유용하게 쓴 잼이 Pry
* Object#pry 를 정의하고, 이 함수를 디버거로 사용할 수 있다.
* 중단점을 설정하는 대신 현재 바인딩을 호출하는 줄을 코드에 추가한다.

```ruby
# code...
require "pry"; binding.pry
# more code...
```

* ruby interpreter를 현재 바인딩에서 열고 ~

#### IRB 예시

* irb는 표준 입력이나 파일을 파싱하고 각 줄을 통과시켜 eval하는 단순한 프로그램

```ruby
eval(statements, @binding, file, line)
```

* irb 소스코드의 깊은 곳에 있는 eval 호출
* statements는 그냥 루비 코드
* binding -  다른 맥락에서 코드를 eval하기 위해 이 인수를 변경 가능하다. 
  * 특정 객체에서 중첩된 irb세션을 열 때 기존 irb 세션의 객체 이름 뒤에 irb를 입력함
  * 해당 객체 맥락에서 eval 될 것
* file, line은 예외가 났을 때 스택을 주적하는데 사용됨

```ruby
x=1/0
ZeroDivisionError: divided by 0
from exception.rb:2:in `/'
```

#### String of Code vs Block

* 문자열의 코드는 결국 블록과 다를바가 없다.
* 하지만 되도록 블록으로..

#### eval()의 문제

* 꿀이지만 그만큼 위험이 따름
  * ide에서 하이라이팅이 잘 안 될 수도 있다.
  * 정적 분석으로 에러를 찾기가 아려워서 ide에서도 워닝을 못뱉음
* 위의 에러들은 사실 보안 이슈에 비하면 사소하지

#### 코드 인젝션

```ruby
def explore_array(method)
  code = "['a', 'b', 'c'].#{method}"
  puts "Evaluating: #{code}"
  eval code
end
loop { p explore_array(gets()) }
```

* 마지막 줄의 무한 루프는 표준 입력에서 문자열을 받아다가 expect_array의 메서드로 넣는다.
* code를 eval하고 print

```ruby
➾ find_index("b")
❮ Evaluating: ['a', 'b', 'c'].find_index("b")
1

➾ map! {|e| e.next }
❮ Evaluating: ['a', 'b', 'c'].map! {|e| e.next }
   ["b", "c", "d"]
```

* 이 코드를 사용자가 입력한다면 

```ruby
➾ object_id; Dir.glob("*")
❮ ['a', 'b', 'c'].object_id; Dir.glob("*") => [your own private information here]
```

* 악의적인 사용자가 컴퓨터에서 임의 코드를 실행할 수 있다.
* code injection attack

##### 코드 인젝션 막기

* 구문을 분석할 수도 있겠지만 악성 코드 작성 방법은 많으니까 효과적이지 않을 수 있다.
* 사용자가 직접 작성한 문자열만 악성 코드를 포함할 수 있으므로 사용자가 작성한 문자열에 대한 eval을 금지할 수도 있다.
  * 많이 복잡한 경우는 문자열이 어디서 왔는지 알기 어려울지도... 추적 계속 해야하니
* 이런 어려움 때문에 어떤 프로그래머들은 eval을 전면 금지하자고 하기도 함 
  * 이는 꽤 인기 있는 선택
  * 잘못될 수 잇는 것에 대해 편집증적인 경향
* eval을 안쓰면 사례별로 대체 기법을 찾아야 한다.
  * 동적 메서드와 동적 디스패치로 대체 가능

```ruby
POSSIBLE_VERBS.each do |m|
  define_method m do |path, *args, &b|
    r[path].send(m, *args, &b)
	end 
end

def explore_array(method, *arguments)
  ['a', 'b', 'c'].send(method, *arguments)
end
```

* 하지만 사용자가 block을 못씀, 임의의 문자열을 코드로 삽입하도록 해야한다..
* eval과 eval을 안쓰는 방식에서 선택이 어렵지....
* 이하 eval을 그나마 안전하게 쓰는 기능을 제공

#### Tainted Objects and Safe Levels

* 루비는 잠재적으로 안전하지 않은 객체에 대해 - 특히 외부 소스에서 온 객체를 tainted로 자동 표시한다.
* tainted ( 오염된 ) 객체는 프로그램이 web form, file, command line, 혹은 시스템 변수에서 읽는 문자열

```ruby
# read user input
user_input = "User input: #{gets()}"
puts user_input.tainted?
➾x=1 ❮ true
```

* 루비는 오염된 객체를 잘 보완해주는 safe level이라는 개념을 제공한다
* $SAFE 전역 변수로 안전 수준을 설정하면, 잠재적인 위험한 작업을 허용하지 않는다.
  * 0 - 3 까지
  * 1이상이면 tainted 문자열을 eval 못함
  * 2이면 대부분의 파일 관련 작업을 수행할 수 없음

```ruby
$SAFE = 1
user_input = "User input: #{gets()}"
eval user_input
```

* 안전 수준에 의존하여 디스크 액세스 같은 위험한 작업을 허용하지 않도록 할 수 있다.

#### ERB 예시

* ERB는 루비 기본 템플릿 시스템임
* HTML에 ruby code를 내장하여 사용하는 코드 프로세서

```erb
<p><strong>Wake up!</strong> It's a nice sunny <%= Time.new.strftime("%A") %>.</p>
```

`<%= .. %>` 안에 ruby code를 넣어두면 evaluate

```ruby
require 'erb'
erb = ERB.new(File.read('template.rhtml'))
erb.run
❮ <p><strong>Wake up!</strong> It's a nice sunny Friday.</p>
```

```ruby
  class ERB
    def result(b=new_toplevel)
      if @safe_level
        proc {
          $SAFE = @safe_level
          eval(@src, b, (@filename || '(erb)'), 0)
        }.call
			else
        eval(@src, b, (@filename || '(erb)'), 0)
      end
		end
#...
```

* new_toplevel은 TOPLEVEL_BINDING의 복사본을 반환하는 메서드
* 안전수준이 설정 되어있으면 포함
  * 샌드박스를  구축한다.
  * 별도의 범위에서 코드를 실행하기 위해 clean room을 사용함
  * 안전 수준은 proc 안에서만 적용이 됨
  * 
* 아니면 바로 eval

## 1단계 일단 간단하게 eval로

checked_attribute를 만들 계획을 세웠던 대로 진행!

1. eval을 사용하여 add_checked_attribute라는 커널 메서드를 작성
2. eval을 제거

```ruby
require 'test/unit'
class Person; end
class TestCheckedAttribute < Test::Unit::TestCase
  def setup
    add_checked_attribute(Person, :age)
    @bob = Person.new
	end
  def test_accepts_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
	end
  def test_refuses_nil_values
    assert_raises RuntimeError, 'Invalid attribute' do
      @bob.age = nil
		end 
  end
  def test_refuses_false_values
    assert_raises RuntimeError, 'Invalid attribute' do
      @bob.age = false
		end 
  end
end
# Here is the method that you should implement.
def add_checked_attribute(klass, attribute)
  # ...
end
```

```ruby
def add_checked_attribute(klass, attribute)
  eval "class #{klass}
        def #{attribute}=(value)
          raise 'Invalid attribute' unless value
          @#{attribute} = value
        end
        def #{attribute}()
          @#{attribute}
		    end 
  end"
end
```

* `add_checked_attribute` 를 한 뒤 String클래스

```ruby
class String
  def my_attr=(value)
    raise 'Invalid attribute' unless value
    @my_attr = value
	end
  def my_attr()
    @my_attr
	end 
end
```

* Open Class로 처리가 되고, 두 새로운 메서드를 가지게 된다.

## 2단계 Eval 빼기

* eval을 뿌시자
* 일반 루비 메서드로 대체!
* 왜 eval을 뿌셔야하는 강박관념이 생겼을까... ? 
  * 팀원들만 사용하는데 코드 인젝션의 표적이 되나? 아니지
  * 하지만 이 메서드가 나중에 세상에 드러날 수 있으니...?
  * Strings of Code를 안 쓰고 만들면 더 명확하고 우아하게 제공 가능하고 하이라이터들이 덜 홀란스러워 할 것이다.
* 플랫 스코프 기억하니?

```ruby
def add_checked_attribute(klass, attribute)
  klass.class_eval do
    define_method "#{attribute}=" do |value|
      raise 'Invalid attribute' unless value
      instance_variable_set("@#{attribute}", value)
    end
    define_method attribute do
      instance_variable_get "@#{attribute}"
		end
  end
end
```

* 해단 클래스의 스코프에 들어가야 한다.
* eval을 제거하면 클래스 키워드를 사용할 수 없으므로 class_eval을 사용하여 스코프에 들어간다.
* 런타임에서 메서드의 이름을 알 수 없으니 define_method를 사용해야한다.

## 3단계 블록으로 검증

* 블록으로 속성 검증이 가능해야한다, - 유연하게
*  하지만 지금은 0혹은 false 할당시 예외
* 새로운 테스트 필요함

```ruby
require 'test/unit'
class Person; end
class TestCheckedAttribute < Test::Unit::TestCase
  def setup
    add_checked_attribute(Person, :age) {|v| v >= 18 }
    @bob = Person.new
	end
  def test_accepts_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
	end
  def test_refuses_invalid_values
    assert_raises RuntimeError, 'Invalid attribute' do
			@bob.age = 17
		end 
  end
end
def add_checked_attribute(klass, attribute, &validation)
  # ... (The code here doesn't pass the test. Modify it.)
end	
```

```ruby

def add_checked_attribute(klass, attribute, &validation)
  klass.class_eval do
    define_method "#{attribute}=" do |value|
      raise 'Invalid attribute' unless validation.call(value)
      instance_variable_set("@#{attribute}", value)
		end
    define_method attribute do
      instance_variable_get "@#{attribute}"
		end 
  end
end

```

## 4단계 클래스 매크로!

* 일단 테스트 케이스를 변경

```ruby
class Person
  attr_checked :age do |v|
   v >= 18
  end
end
class TestCheckedAttributes < Test::Unit::TestCase
  def setup
    @bob = Person.new
	end
  def test_accepts_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
	end
  def test_refuses_invalid_values
    assert_raises RuntimeError, 'Invalid attribute' do
			@bob.age = 17
		end 
 	end
end
```

* Class 클래스에서 정의한다!

```ruby
class Class
  def attr_checked(attribute, &validation)
    define_method "#{attribute}=" do |value|
      raise 'Invalid attribute' unless validation.call(value)
      instance_variable_set("@#{attribute}", value)
    end
    define_method attribute do
      instance_variable_get "@#{attribute}"
    end
  end
end
```

## Hook Methods

* 클래스가 상속될 때 코드를 실행 할 수 있다!

```ruby
class String
  def self.inherited(subclass)
    puts "#{self} was inherited by #{subclass}"
  end
end
class MyString < String; end
String was inherited by MyString
```

* 상속 메서드는 클래스의 인스턴스 메서드
* 원래는 아무런 작업도 수행하지 않지만 재정의 가능

### More Hooks

* 라이프 사이클에 연결이 가능하도록 모듈에서도 제공! 

```ruby
module M1
  def self.included(othermod)
    puts "M1 was included into #{othermod}"
  end
end
module M2
  def self.prepended(othermod)
    puts "M2 was prepended to #{othermod}"
  end
end
class C
  include M1
  prepend M2
end
❮ M1 was included into C M2 was prepended to C


module M
  def self.method_added(method)
    puts "New method: M##{method}"
  end
  def my_method; end
end
❮ New method: M#my_method
```

* include/prepend시 실행 가능
* 모듈을 재정의하여 객체를 확장할 때 코드 실행 가능

이런 훅들은..

* singleton method에서는 못쓴다

```ruby
module M; end
class C
	def self.include(*modules)
		puts "Called: C.include(#{modules})"
		super 
  end
	include M
end

```

* 다른 쪽에서 동일한 이벤트에 연결 가능함!
* Module#included 을 오버라이딩 하는 것과, Module#include를 오버라이딩 하는 것은 차이가 있음
* include에는 실제 작업이 있으므로 super를 포함 꼭 시켜야함

### VCR 예시

* VCR 잼은 HTTP 요청을 녹화하고 리플레이하는 잼이다.
* VCR의 Request 클래스에 Normalizers:Body가 포함되어있다.
* Body 모듈은 body_from 같이 http message body를 다루는 클래스 메서드를 추가한다.
* 하지만 클래스는 일반적으로 클래스 메서드가 아닌 모듈을 포함해서 인스턴스 메서드를 갖고오지 않는가?
* 어떻게 얘는 mixin할까

```ruby
module VCR
  module Normalizers
    module Body
      def self.included(klass)
        klass.extend ClassMethods
			end
      module ClassMethods
        def body_from(hash_or_string)
          #...
```

* include를 시키면 Body의 included 훅을 호출
* Request을 ClassMethods 모듈로 확장한다.
* 확장 메서드는 요청의 싱글톤 클래스에 ClassMethods의 메서드를 포함시킨다.

ClassMethods - plus - hook 관용구는 꽤 흔하고 레일즈 코드에서 광범위하게 썼다.

하지만 다른 매커니즘으로 지금 변경되었고 VCR이나 다른 잼에서 이 예를 찾을 수 있다.

## 5단계 필요한 클래스에서만!

* checkedAttributes라는 모듈을 포함한 클래스에서만 사용할 수 있도록 변경

```ruby
require 'test/unit'
class Person
  include CheckedAttributes
  attr_checked :age do |v|
    v >= 18
	end 
end
class TestCheckedAttributes < Test::Unit::TestCase
  def setup
    @bob = Person.new
	end
  def test_accepts_valid_values
    @bob.age = 18
    assert_equal 18, @bob.age
	end
  def test_refuses_invalid_values
    assert_raises RuntimeError, 'Invalid attribute' do
			@bob.age = 17
		end 
  end
end
```

```ruby
module CheckedAttributes
  def self.included(base)
    base.extend ClassMethods
	end
  module ClassMethods
    def attr_checked(attribute, &validation)
      define_method "#{attribute}=" do |value|
        	raise 'Invalid attribute' unless validation.call(value)
	        instance_variable_set("@#{attribute}", value)
			end
      define_method attribute do
        instance_variable_get "@#{attribute}"
			end 
    end
	end 
end
```

굿!

## 정리

* 메타프로그래밍 문제를 풀었다. 그 과정에서 eval과 이에 대한 문제점 및 해결 방안을 배움
* hook methods를 알게되었다.



