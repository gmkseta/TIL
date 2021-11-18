---
title: '[짧] Rake Task 사용 시 parameter 사용'
date: '2021-03-25'
tags: ['Rails', '짧', '팁']
cover: './img.png'

---

Rake Task를 만들어서 사용할 때 파라미터를 사용하고 싶을때 찾아서 기록해놓은 내용이다.

기억 상 크롤링 할 때 프로세스를 여러개 돌리려고, 찾았던거같은데 태그를 파라미터로 보냈던것 같다.

```ruby
namespace :crawling do
  desc 'Instagram Explores Tag Crawling'
  task :instagram, [:tag] => [:environment] do |t, args|
    InstagramCrawler.exec(args[:tag])
  end
end

```

이렇게 작성해놓고 zsh에서 rake task 실행 시 

```zsh
rake crawling:instagram[맛집]
zsh: no matches found: crawling:instagram[맛집]
```

넵 안됩니다.


```zsh
rake crawling:instagram\[맛집\]
or
rake 'crawling:instagram[맛집]'
```

이런식으로 사용.
