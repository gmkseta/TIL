---
title: "HTTPS 와 SSL - 2"
date: "2021-12-19"
update: "2021-12-19"
tags: ["cs"]
series: "https"
---

* 이전 글에서 HTTPS와 HTTP의 차이에 대해 알아봤다.
* HTTPS에서 보안 계층은 어떻게 동작하는지에 대해 좀 더 자세히 알아보자

## SSL 인증서가 신뢰 할 수 있는 서버(사이트)임을 보장하는 방법

1. 웹 브라우저가 서버에 접속할 때 서버는 먼저 인증서를 제공한다.
2. 브라우저는 이 인증서를 발급한 CA가 자신이 갖고있는 CA의 리스트에 있는지를 확인한다.
3. 있다면 해당 CA의 공개키를 이용해서 인증서를 복호화 한다.
   * CA의 공개키로 복호화 가능 하다는 것은 해당 비공개 키로 암호화 된 것을 의미한다.
4. 복호화에 성공하면 CA에 의해 발급된 인증서라는 것이 검토됨을 의미한다.

### 그럼 사실 공개키만 있어도 복호화가 가능한거 아닌가?

* 데이터를 보호하는 목적이 아니다 
* 복호화 할 수 있다는 것은 그 데이터가 비공개키로 암호화 되었다는 것을 의미
* 따라서 공개키가 데이터를 제공한 사람의 신원을 보장해주는 것
* 이를 전자서명이라고 한다.

## SSL의 동작 방식

* 이전 글에서 간단하게 SSL은 암호화된 데이터를 전송하기 위해 공개키와 대칭키를 혼합해서 쓴다고 했다.
  * 실제 데이터는 대칭키로 암호화 - ( 리소스가 적게 들어서 빠름 )
  * 대칭키를 공개키 방식으로 암호화
* 이에 대해 좀 더 자세히 알아보자

### SSL Handshake

1. Client Hello - 먼저 클라이언트가 서버에게 요청을 보낸다. 아래의 정보를 보낸다. 

   * 클라이언트에서 생성한 **랜덤 데이터**

   * 클라이언트 사용 가능한 암호화 방식 목록 - 서로 지원하는 암호화 방식이 다를 수 있으므로 협상 해야함
     * Cipher Suite 목록

   * 세션 아이디 - 이미 SSL Handshake를 했다면 기존 세션을 사용한다. 이에 대한 식별자

2. Server Hello - 위에 대한 응답을 준다.

   * 서버에서 생성한 **랜덤 데이터**
   * 서버가 선택한 암호화 방식
     * 클라이언트의 암호화 방식 목록을 보고 서버에서도 사용할 수 있는 방식을 전달
   * 인증서

3. 클라이언트는 서버의 인증서를 확인하기위해 브라우저에 내장된 CA목록을 확인

   * 목록에 있다면 내장된 CA의 공개키로 복호화, 성공 시 인증서가 보증된 것
   * 없으면 경고
   * **Pre-master secret**를 생성한다.
   * 이후 이 **Pre-master secret**를  서버의 공개키로 암호화 해서 서버로 전송

4. 서버는 클라이언트로부터 받은 정보로 **Session key**를 유도

   *  **Pre-master secret** 복호화한다.
   * **Client 랜덤 데이터, Server 랜덤 데이터** 와 함께 **Session Key**를 유도한다.
   * 이 Session Key로 암호화된 데이터 통신을 한다.

5. 핸드쉐이크 잘 되었다고 알리고 끝

## Opinions

* pre master secret, client random, server random, session 등 많은 키가 생성되고 사용되어서 많이 헷갈린다.
* cloudflare 블로그에서 그림을 잘 그려놨다고 하던데 보러가야징







## References

- https://www.geeksforgeeks.org/secure-socket-layer-ssl/
- https://opentutorials.org/course/228/4894
- https://learningnetwork.cisco.com/s/question/0D53i00000Kt0q0/which-layer-of-the-osi-model-do-ssl-and-tls-belong-to
- https://dokydoky.tistory.com/462
