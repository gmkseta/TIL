---
title: M Ruby - 9. The Design of Active Record
date: "2021-05-10"
update: "2021-05-10"
series: "Metaprogramming Ruby"
tags: ["ruby", "book"]
cover: "2021-04-01-03-27-27.png"
---

* ActiveRecord는 루비의 객체를 데이터베이스 레코드에 매칭하는 Rails 라이브러리이다.
* 이러한 기능을 object relational mapping이라고 하고, 관계형 데이터베이스와 객체지향 프로그래밍을 모두 잘 활용 가능하다.
* 액티브 레코드가 하는 일 보다는 어떻게 하는지에 대해 관심있게 확인!

## 짧은 예시

```ruby
require 'active_record'
ActiveRecord::Base.establish_connection :adapter => "sqlite3",
                                        :database => "dbfile"
class Duck < ActiveRecord::Base
  validate do
    errors.add(:base, "Illegal duck name.") unless name[0] == 'D'
  end
end
```

* `ActiveRecord::Base` 는 데이터베이스 연결같은 클래스 메서드 뿐만 아니라 매핑되는 모든 클래스의 슈퍼 클래스이다.

```ruby
class Duck < ActiveRecord::Base
  validate do
    errors.add(:base, "Illegal duck name.") unless name[0] == 'D'
  end
end
```

* 유효성 검사를 하는 클래스 매크로이다.
  * Duck의 이름은 D로 시작해야한다!
  * 만약 다른 이름을 저장하려 하면 예외
* convention에 따라서 Duck은 ducks 테이블애 매핑된다.
  * ActiveRecord는 데이터베이스 스키마를 봐서 ducks에 name이 있다는 것을 알고, 그 필드에 접근 가능한 Ghost Method를 정의한다.

```ruby
my_duck = Duck.new
my_duck.name = "Donald"
my_duck.valid?         # => true
my_duck.save!

duck_from_database = Duck.first
duck_from_database.name         # => "Donald"
duck_from_database.delete

```

## ActiveRecord의 매커니즘

* 앞의 예는 간단하지만 사실 더 많은 것들을 할 수 있다.
* 하지만 ActiveRecord::Base 에서는 그런 메서드들에 대한 추적이 없다.
* 따라서 초보자에겐 어떤 메서드가 어디서왔고 어떻게 들어오는지 이해하기 어렵다

### Autoloading 매커니즘

```ruby
require 'active_support'
require 'active_model'
# ...
module ActiveRecord
  extend ActiveSupport::Autoload
  autoload :Base
  autoload :NoTouching
  autoload :Persistence
  autoload :QueryCache
  autoload :Querying
  autoload :Validations
  # ...
```

* ActiveRecord는 두 개의 라이브러리에 크게 의존한다.
  * ActiveSupport, ActiveModel
* `autoload` 는 ActiveSupport의 메서드임
*  `ActiveSupport::Autoload` 를 extend 하고 autoload는 ActiveRecord의 클래스 메서드가 된다.
* ActiveRecord는 autoload 클래스 매크로를 통해 수십개의 모듈을 등록한다.

### ActiveRecord::Base

```ruby
module ActiveRecord
  class Base
    extend ActiveModel::Naming
    extend ActiveSupport::Benchmarkable
    extend ActiveSupport::DescendantsTracker
    extend ConnectionHandling
    extend QueryCache::ClassMethods
    extend Querying
    extend Translation
    extend DynamicMatchers
    extend Explain
    extend Enum
    extend Delegation::DelegateCache
    include Core
    include Persistence
    include NoTouching
    include ReadonlyAttributes
    include ModelSchema
    include Inheritance
    include Scoping
    include Sanitization
    include AttributeAssignment
    include ActiveModel::Conversion
    include Integration
    include Validations
    include CounterCache
    include Locking::Optimistic
    include Locking::Pessimistic
    include AttributeMethods
    include Callbacks
    include Timestamp
    include Associations
    include ActiveModel::SecurePassword
    include AutosaveAssociation
    include NestedAttributes
    include Aggregations
    include Transactions
    include Reflection
    include Serialization
    include Store
    include Core
	end
  ActiveSupport.run_load_hooks(:active_record, Base)
end
```

* 모듈을 통해 기능들을 조립하는 클래스는 흔하지 않지만 ActiveRecord::Base는 이 작업을 대규모로 수행한다.
* 그냥 수십 개의 모듈을 확장하거나 포함할 뿐이다.
* `run_load_hooks` 코드를 통해 이러한 모듈 일부가 로드된 후 자체 configuration코드를 실행 가능
* 모듈의 소스코드가 필요하지 않고 그냥 Include를 한다, 이 덕분에 최소한의 코드로 많은 모듈을 사용 가능하다.

```ruby
module ActiveRecord
  module Persistence
    def save(*)  # ...
    def save!(*) # ...
    def delete   # ...
```

* Base의 특정 메서드가 어디서 왔는지 그리 어렵지 않을 수 있다
* 저장과 같은 persistence 메서드는 위와 같은 코드에서 확인이 가능하다.

### 유효성 검증 모듈

`ActiveRecord::Validations` - 관련 모듈인가...?

```ruby
module ActiveRecord
  module Validations
    include ActiveModel::Validations
    # ...
    def valid?(context = nil) # 
```

* 하지만 실제로 validate 메서드는 없음
* `ActiveModel::validations` 에 있다~

이런 모듈을 포함하여 조금 헷갈리는 세부사항이 있다.

일반적으로 클래스는 모듈을 포함함으로써 인스턴스 메서드를 얻는다.

하지만 validate는 ActiveRecord의 클래스 메서드이다. 어떻게 Base는 클래스 메서드를 얻을 수 있지?

ActiveModel, ActiveRecord는 왜 두 모듈로 나뉘었나?

크게 두 가지 작업 

1. 저장 및 로드와 같은 데이터베이스 작업을 처리
2. 객체 모델을 다루는 것, 객체 속성을 관리하거나 유효한지 추적하는 것

라이브러리의 저자들은 두개의 분리된 라이브러리로 분할하기로 결정해서 active_model이  탄생한 것

특히 `valid?` 는 나름 데이터베이스쪽에 관계가 있어서 남았고,

`validate` 는 데이터베이스와 관계 없이 객체의 속성에만 관심이 있으므로 ActiveModel로 갔다

## 교훈

* 수많은 모듈을 포함해서 굉장히 큰 클래스가 된다.
* Base는 300개 이상의 인스턴스 메서드와 550개 이상의 클래스 메서드를 갖고있다..
* ActiveRecord::Base는 궁극의 오픈클래스

수백개의 메서드를 가진 거대한 클래스? 이해하기 힘들고 어렵지 않나?

* 액티브 레코드의 대부분의 메서드는 궁극적으로 하나의 클래스 안으로 굴러들어간다.
* 일부 모듈은 메타프로그래밍을 사용하여 더 많은 메서드를 정의하는 것을 고민하지 않고..
* 엎친 데 덮친 격으로 액티브 레코드로 작업하는 추가 라이브러리도 액티브 레코드를 확장함..

스파게티 덩어리가 되지 않을까? ~~하지만 그렇지 않다...?~~ - 

* 많은 사람들이 자신의 목적을 위해 액티브 레코드를 몽키패치하고,.. 
* 엑레의 소스코드는 빠르게 진화한다...
* 안정적이게 유지가 되고 프로덕션에서 만족하며 사용중...

액티브 레코드에서 배운 중요한 가이드라인...

* design techniques는...  상대적이고 사용하는 언어에 따라 다르다,
* 루비에서는 다른 언어들과 다른 관용구를 사용한다.
* 오래된 좋은 규칙들이 갑자기 쓸모없어지는 것이 아니다, 
* 루비에서도 다른 언어와 마찬가지로 디자인의 기본 원칙( 디커플링, simplicity, 중복 없음)이 적용된다.
* 하지만 이를 달성하기 위한 기술이 매우 다르다.
* ActiveRecord::Base를 보면 매우 큰 클래스지만 소스코드에는 복잡한 코드가 없다
* 대신 느슨하게 결합되고 테스트하기 쉬우며 재사용하기 쉬운 모듈을 조합하여 런타임에 구성된다.

```ruby
require 'active_model'
class User
  include ActiveModel::Validations
  attr_accessor :password
  validate do
    errors.add(:base, "Don't let dad choose the password.") if password == '1234'
	end 
end

user = User.new
user.password = '12345'
user.valid?        # => true
user.password = '1234'
user.valid?        # => false

```

* 위처럼 필요한 경우만 포함도 가능함









