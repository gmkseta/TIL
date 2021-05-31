---
title: M Ruby - 12. Attribute Methods의 진화
date: "2021-05-31"
update: "2021-05-31"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

* 대규모 시스템에서 메타크로그래밍을 사용할 때 어떤일이 발생하는지 여전히 궁금하다!!
* 이를 살펴보기 위해 Rails의 가장 인기 있는 기능중 하나인 attribute method에 대해 살펴본다.
* 참고로 모든 라인을 이해하려고 하지 말고 아이디어 만을 이해하려고 하자

## Attribute Methods의 사용

```ruby
require 'active_record'
ActiveRecord::Base.establish_connection :adapter => "sqlite3",
                                        :database => "dbfile"
ActiveRecord::Base.connection.create_table :tasks do |t|
  t.string   :description
  t.boolean  :completed
end
```

* 위 처럼 데이터베이스에 tasks라는 테이블을 만든다면

```ruby
class Task < ActiveRecord::Base; end
task = Task.new
task.description = 'Clean up garage'
task.completed = true
task.save
task.description    # => "Clean up garage"
task.completed?     # => true
```

* `ActiveRecord::Base` 에서 상속하는 빈 Task 클래스를 정의할 수 있고, 해당 클래스의 객체를 사용하여 데이터베이스와 상호작용이 가능하다.
* 2개의 쓰기 accessor( 이하 접근자 )
  *  description = , completed = 
* 1개의 읽기 접근자
  * description
* 1개의 쿼리 접근자
  * completed?
* 4개의 접근자 모두 정의한 것이 아닌 Active Record에서 generated된 것이다.
* 이러한 자동 생성 접근자를 attributes methods라고 한다.

## 복잡한 역사

### Rails 1: 간단한 시작

* 첫 버전에서는 단지 몇 줄의 코드

```ruby
module ActiveRecord
  class Base
    def initialize(attributes = nil)
      @attributes = attributes_from_column_definition
      # ...
    end
    def attribute_names
      @attributes.keys.sort
    end
    alias_method :respond_to_without_attributes?, :respond_to?
    def respond_to?(method)
      @@dynamic_methods ||= attribute_names +
                        attribute_names.collect { |attr| attr + "=" } +
                        attribute_names.collect { |attr| attr + "?" }
      @@dynamic_methods.include?(method.to_s) ? true : 
      respond_to_without_attributes?(method)
    end
    def method_missing(method_id, *arguments)
      method_name = method_id.id2name
      if method_name =~ read_method? && @attributes.include?($1)
        return read_attribute($1)
      elsif method_name =~ write_method?
        write_attribute($1, arguments[0])
      elsif method_name =~ query_method?
        return query_attribute($1)
      else super
      end 
    end
    def read_method?()  /^([a-zA-Z][-_\w]*)[^=?]*$/ end
    def write_method?() /^([a-zA-Z][-_\w]*)=.*$/    end
    def query_method?() /^([a-zA-Z][-_\w]*)\?$/     end
    def read_attribute(attr_name)         # ...
    def write_attribute(attr_name, value) #...
    def query_attribute(attr_name)        # ...
```

* 생성자를 먼저 살펴보자
  * `@attributes` 변수는 데이터베이스의 속성 이름으로 채워진다.
* method_missing을 보자
  * 해당 속성의 이름은 Ghost Method의 이름이 된다.
  * description= 과 같은 메서드를 호출할 때 method_missing은 속성의 이름과, write_method의 정규식에 일치한 다는 것을 알 수 있다.
  * 따라서 write_attribute("description")을 호출하게 된다. 다른 것 들도 비슷한 프로세스이다.
* 3장에서 봤을때 method_missing과 함께 respond_to? 를 재정의 하는 것이 좋은 아이디어라는 것을 배웠다 
  * 예를 들어 `my_task.description` 이 호출 가능하면 `my_task.respond_to?(:description)` 이 true를 반환해야한다.
  * 재정의된 respond_to? 는 nil guard를 사용하여  `@@dynamic_methods` 에 한 번만 계산하고 클래스 변수에 저장한다.

### Rails 2: 성능에 초첨맞추기

* method_missing에 대한 설명을 기억하는가?
* 존재하지 않는 메서드를 호출하면 Ruby는 해당 메서드를 찾기위해 조상 체인으로 타고 올라간다.
* 메서드를 찾지 못하고 BasicObject에 도달하면 맨 아래에서 다시 시작하여 method_missing을 호출한다.
* 일반적으로 Ruby가 전체 조상 체인을 한 번 이상 걸어야 하기 때문에 일반 메서드보다 느리다.
* 대부분 성능 차이는 무시할 수 있지만 attributes method는 매우 자주 호출 된다.
* define_method를 사용하고 method_missing을 모두 제거하여 고스트메서드를 동적 메서드로 대체함으로써 이 성능 문제 해결이 가능하다.
* 흥미롭게도 그들은 Ghost Method와 Dynamic Method를 모두 포함하는 혼합 솔루션을 택했다.

```ruby
module ActiveRecord
  module AttributeMethods
    def method_missing(method_id, *args, &block)
      method_name = method_id.to_s
      if self.class.private_method_defined?(method_name)
        raise NoMethodError.new("Attempt to call private method", method_name, args)
      end
      # If we haven't generated any methods yet, generate them, then
      # see if we've created the method we're looking for.
      if !self.class.generated_methods?
        self.class.define_attribute_methods
        if self.class.generated_methods.include?(method_name)
          return self.send(method_id, *args, &block)
        end
      end
# ...
    end
    def read_attribute(attr_name)         # ...
    def write_attribute(attr_name, value) # ...
    def query_attribute(attr_name)        # ...
```

* `Task#description=` 같은 메서드를 처음 호출하면 호출이 method_hissing으로 전달 된다.
* 작업을 수행 전 private method 호출은 에러를 발생시킨다.
* 그 다음 `define_attribute_methods` 을 호출한다. 
* 다음에 description= 또는 다른 접근자를 호출할 때 호출은 method_missing에 의해 처리되지 않는다.
* 대신 고스트메서드가 아닌 실제 메서드를 호출한다.
* method_missing은 dynamic dispatch를 사용하여 이를 호출하고 결과를 받을 수 있다.
* 이 프로세스는 `generated_methods?`로 인해 한 번만 발생하고 건너뛴다.

```ruby
def define_attribute_methods
  return if generated_methods?
  columns_hash.each do |name, column|
    unless instance_method_already_implemented?(name)
      if self.serialized_attributes[name]
        define_read_method_for_serialized_attribute(name)
      elsif create_time_zone_conversion_attribute?(name, column)
        define_read_method_for_time_zone_conversion(name)
      else
        define_read_method(name.to_sym, name, column)
      end 
    end
    unless instance_method_already_implemented?("#{name}=")
      if create_time_zone_conversion_attribute?(name, column)
        define_write_method_for_time_zone_conversion(name)
      else
        define_write_method(name.to_sym)
      end 
    end
    unless instance_method_already_implemented?("#{name}?")
      define_question_method(name)
    end 
  end
end
```

* `instance_method_already_implemented?` 속성 이름의 메서드가 이미 존재하면 이 코드는 다음 속성으로 건너뛴다.
* `define_read_method`, `define_write_method` 와 같이 실제 작업을 수행하는 다른 메서드에 위임하는 것 외에는 거의 뭔가를 하지 않는다.

```ruby
def define_write_method(attr_name)
  evaluate_attribute_method attr_name,
     "def #{attr_name}=(new_value);write_attribute('#{attr_name}', new_value);end",
     "#{attr_name}="
end
def evaluate_attribute_method(attr_name, method_definition, method_name=attr_name)
  unless method_name.to_s == primary_key.to_s
    generated_methods << method_name
  end
  begin
    class_eval(method_definition, __FILE__, __LINE__)
  rescue SyntaxError => err
    generated_methods.delete(attr_name)
    if logger
      logger.warn "Exception occurred during reader method compilation."
      logger.warn "Maybe #{attr_name} is not a valid Ruby identifier?"
      logger.warn err.message
    end 
  end
end
```

* `define_write_method` 는 class eval을 통해서 String Code를 빌드한다.
* `description=` 을 호출하면 evaluate_attribute_method가 다음 문자열을 eval한다.

```ruby
def description=(new_value);write_attribute('description', new_value);end
```

* 속성에 처음 접근할 때 해당 속성은 고스트 메서드이다.
* method_missing을 통해 실제 메서드로 전환한다.
* 모든 열에 대한 읽기, 쓰기, 쿼리 접근자를 동적으로 정의한다.
* 하지만 모든 속성 접근자에 적용되지는 않는다.

#### 동적으로 유지되는 속성

* ActiveRecord를 통해 속성 접근자를 정의하고 싶지 않은 경우가 있다.
* 계산된 필드 같이 데이터베이스 열이 지원하지 않는 속성을 생각해보자

```ruby
my_query = "tasks.*, (description like '%garage%') as heavy_job"
task = Task.find(:first, :select => my_query)
task.heavy_job?  # => true
```

* heavy_job 같은 속성은 객체마다 다를 수 있기 때문에 액세스하기 위해 동적 메서드를 생성할 필요가 없다.

```ruby
module ActiveRecord
  module AttributeMethods
    def method_missing(method_id, *args, &block)
      # ...
      if self.class.primary_key.to_s == method_name
        id
      elsif md = self.class.match_attribute_method?(method_name)
        attribute_name, method_type = md.pre_match, md.to_s
        if @attributes.include?(attribute_name)
          __send__("attribute#{method_type}", attribute_name, *args, &block)
        else
          super 
        end
      elsif @attributes.include?(method_name)
        read_attribute(method_name)
      else super
      end 
    end
    private
      # Handle *? for method_missing.
      def attribute?(attribute_name)
        query_attribute(attribute_name)
      end
      # Handle *= for method_missing.
      def attribute=(attribute_name, value)
        write_attribute(attribute_name, value)
      end
```

* method_missing 의 후반부를 보면 객체의 식별자에 액세스 하는 경우는 해당 값을 반환한다.
* 속성 접근자를 호출하는 경우는 동적 디스패치 또는 read_attribute에 대한 직접 호출을 사용하여 접근자를 호출한다
* 그렇지 않으면 super를 사용하여 상위 체인으로 호출을 보낸다

### Rails 3,4 : 더 특별한 클래스

* 1에서는 수 십줄의 코드
* 2에서는 자체 파일과 수백 줄의 코드
* 3에서는 테스트를 포함하지 않은 9개의 소스 코드 파일

* Rails가 커짐에 따라 속성 메서드와 관련된 작은 트릭 및 성능 최적화, 코너 케이스를 발견했다.
* Rails 4에서는 더 나아가 속성 접근자를 정의할때 이를 UnboundMethod로 변환하여 메서드 캐시에 저장한다.

```ruby
module ActiveRecord
  module AttributeMethods
    module Read
      extend ActiveSupport::Concern
      module ClassMethods
        if Module.methods_transplantable?
          def define_method_attribute(name)
            method = ReaderMethodCache[name]
            generated_attribute_methods.module_eval { define_method name, method }
          end 
        else
          def define_method_attribute(name)
            # ...
          end 
        end
```

* define_method_attribute 라는 메서드를 정의한다.
* concern으로 인해 궁극적으로는 ActiveRecord::Base의 클래스 메서드가 된다.
* Module.methods_transplantable?에 따라 다르게 정의된다.
  * UnboundMethod를 다른 클래스 객체에 바인딩할 수 있나? - ruby 2.0 이상일 경우
* define_method_attribute는 메서드 캐시에서 UnboundMethod를 검색하고 메서드를 define_method로 현재 모듈에 바인딩한다.
* 메서드 캐시는 ReaderMethodCache라는 상수에 저장된다.
* generated_attribute_methods 은 클린 룸을 제공,

```ruby
module ActiveRecord
  module AttributeMethods
    module Read
      ReaderMethodCache = Class.new(AttributeMethodCache) {
        private
        # We want to generate the methods via module_eval rather than
        # define_method, because define_method is slower on dispatch.
        # Evaluating many similar methods may use more memory as the instruction
        # sequences are duplicated and cached (in MRI).  define_method may
        # be slower on dispatch, but if you're careful about the closure
        # created, then define_method will consume much less memory.
        #
        # But sometimes the database might return columns with
        # characters that are not allowed in normal method names (like
        # 'my_column(omg)'. So to work around this we first define with
        # the __temp__ identifier, and then use alias method to rename
        # it to what we want.
        #
        # We are also defining a constant to hold the frozen string of
        # the attribute name. Using a constant means that we do not have
        # to allocate an object on each call to the attribute method.
        # Making it frozen means that it doesn't get duped when used to
        # key the @attributes_cache in read_attribute
        def method_body(method_name, const_name)
          <<-EOMETHOD
          def #{method_name}
            name = ::ActiveRecord::AttributeMethods::AttrNames::ATTR_#{const_name}
            read_attribute(name) { |n| missing_attribute(n, caller) }
          end
          EOMETHOD
        end
}.new
```

* ReaderMethodCache는 AttributeMethodCache의 하위 클래스인 익명 클래스의 인스턴스이다.
* 이 클래스는 String of Code를 반환하는 단일 메서드를 정의한다.

```ruby
module ActiveRecord
  module AttributeMethods
    AttrNames = Module.new {
      def self.set_name_cache(name, value)
        const_name = "ATTR_#{name}"
        unless const_defined? const_name
          const_set const_name, value.dup.freeze
        end 
      end
      }    
    class AttributeMethodCache
      def initialize
        @module = Module.new
        @method_cache = ThreadSafe::Cache.new
      end
      def [](name)
        @method_cache.compute_if_absent(name) do
          safe_name = name.unpack('h*').first
          temp_method = "__temp__#{safe_name}"
          ActiveRecord::AttributeMethods::AttrNames.set_name_cache safe_name, name
          @module.module_eval method_body(temp_method, safe_name),
                              __FILE__, __LINE__
          @module.instance_method temp_method
        end 
      end
      private
      def method_body; raise NotImplementedError; end
    end
```

* AttrNames를 보자, set_name_cache라는 단일 메서드가 있는 모듈이다.
  * 이름과 값이 주어지면 메서드는 그 값으로 관습적으로 명명된 상수를 정의한다.
    * "description" => "ATTR_description" 
  * AttrNames는 클린 룸과 유사하다.
  * 속성의 이름을 나타내는 상수를 저장하기 위해서만 존재한다.
* AttributeMethodCache를 보자 [] 메서드는 속성의 이름을 사용하고 해당 속성에 대한 접근자를 UnboundMethod로 반환
  * 속성 접근자는 Ruby 메서드지만 모든 속성 이름이 유효한 Ruby 메서드 이름은 아니다.
    * 속성의 이름을 16진수 시퀀스로 디코딩하고 기존의 안전한 메서드 이름을 만들어 문제를 해결한다.
  * 접근자에 대한 안전한 이름이 있으면 method_body를 호출하여 접근자의 본문을 정의하는 코드 문자열을 가져오고
  * 단순히 @module이라는 이름의 클린룸 내부에 접근자를 정의한다.
  * 마지막으로 클린룸에서 새로 생성된 접근자 메서드를 가져와 UnboundMethod로 반환한다.
* 후속 호출에서 AttributeMethodCache#[]은 더 이상 메서드를 저장할 필요가 없다.
* eotls @method_cache.compute_if_absent가 결과를 저장하고 반환한다
* 동일한 접근자가 여러 클래스에 정의된 경우 시간을 단축한다.
* ReaderMethodCache에서 method_body를 재정의하고 일기 접근자에 대한 코드 문자열을 반환함으로써 일반 AttributeMethodCache를 읽기 접근자를 위한 캐시로 바꾼다.
* WriterMethodCache도 있다.

## 교훈

* 코드에서 몇 가지 특수한 경우를 다뤄야하나?
  * 극단적인 경우에는 처음부터 완벽하고 되돌리지 않아도 되는 코드를 작성하기 위해 항상 노력할 수 있다.
    * Do It Right First Time . 
  * 하지만 다른 경우에는 당장의 명백한 문제를 해결하는 간단한 코드를 작성하고 나중에 더 특별한 경우를 발견하면 더 포괄적으로 만들 수 있다.
    * 이 접근 방식을 진화적 설계 라고 부르겠다.
* 이 두 가지 접근 방식 간의 올바른 균형을 맞추는 게 중요하다.
* Rails1 에서는 간단하고 단순한 솔루션, 2에서는 사용자의 요구사항에 따른 최적화 처럼 진화적인 설계의 좋은 예시이다.
* 다음을 포함하여 여러 대안이 있었다.
  * 고스트 메서드에만 의존하여 접근자를 동적으로 정의하지 않는다.
  * initialize 메소드에서 개체를 생성할 때 접근자를 정의한다.
  * 다른 속성이 아닌 액세스 중인 속성에 대해서만 접근자를 정의한다.
  * 항상 계산된 필드에 대한 접근자를 포함하여 각 개체에 대한 모든 접근자를 정의한다.
  * String of Code 대신 define_method를 사용하여 접근자를 정의한다.
* 몇 가지 대안의 디자인을 시도한 다음 실제 시스템에서 코드를 프로파일리하여 성능의 병목 현상이 발생한 위치를 찾은 다음 최적화하는 것을 쉽게 상상할 수 있다.
* 이전 예제는 최적화에 중점을 뒀지만 동일한 원칙이 모든 측변에 적용된다.
* private 메서드를 호출하기위해 method_missing을 쓰는 것을 막는 코드를 생각해보자
  * 모든 경우를 다 잡는건 어렵다.
  * 합리적인 수의 특별한 경우를 다루고 더 많은 특별한 경우가 보이면 코드를 변경하는 것이 더 쉽다.
* Rails의 접근 방식은 진화적 설계에 치우져져 있다.
  * 루비는 메타프로그래밍을 사용할 때 유연한 언어이므로 코드를 쉽게 발전시킬 수 있다.
  * 완벽한 메타프로그래밍 코드를 미리 작성하는 것은 어렵다. 모든 경우를 찾기 힘드니까.
* 한 문장으로 요약하자면 코드를 최대한 단순하게 유지하고 필요한 만큼 복잡도를 추가하라 라는 뜻
* 시작할 때 일반적인 경우에 코드를 올바르게 만들고 나중에 특별한 경우를 더 추가할 수 있을 정도로 간단하게 만들라. 
* 이것은 대부분의 코드에 대한 좋은 경험 법칙이지만 메타프로그래밍이 관련된 경우 특히 관련이 있다!



