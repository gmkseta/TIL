---
title: '[짧] PG:ConnectionBad - could not connect to server: Connection refused'
date: '2021-03-24'
tags: ['Rails', 'Postgresql', 'mac', 'linux', '짧', '팁']
cover: './img.jpeg'

---

레일즈 - postgres를 사용할떄 자주 본 에러이다.

```shell
PG::ConnectionBad - could not connect to server: Connection refused
```

```shell
...
Started GET "/" for 127.0.0.1 at 2020-01-06 03:12:32 +0900

PG::ConnectionBad - could not connect to server: Connection refused
Is the server running on host "localhost" (::1) and accepting
...
```

맥북 사용 시 다른 맥북 유저에 비해 맥북을 잘 꺼두는 편이였는데, 끌 때 정상적으로 종료시키지 않아서 발생하는 문제 같았다.

프로세스를 제대로 종료하지 않고 노트북이 꺼지는 바람에 pid 파일을 제대로 지우지 못한 탓이다.

이미 pid파일이 있다면 postgres은 제대로 실행되지 못한다.

### 해결 방법
1.  `/usr/local/var/postgres` 혹은 `/usr/var/postgres` 에서 `postmaster.pid` 가 존재하는지 확인 
있다면 지운다 
<br/>
`rm postmaster.pid`

2. postgresql을 재 실행 한다. 
mac : `brew services restart postgresql`
linux : `sudo service postgresql restart`

