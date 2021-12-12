다음 글에서 SSL Handshake와 SSL Protocol Stack에 대해 더 자세히 다뤄보겠다.

## SSL HandShake

* SSL 인증서를 주고 받는 과정
  * 이미 앞에서 간랸하게 설명한 내용이지만 이 과정에 대해서 다시 설명해본다.

1. 클라이언트가 서버에 요청을 보낸다.
   * 

## SSL ( Secure Socket Layer ) 동작 원리

#### SSL Protocol Stack

![](/Users/seongjunkim/Repository/Gmkseta/blog-content/posts/https-and-ssl/2021-12-12-23-07-00.png)

1. SSL Record Protocol
   * 기밀성 ( Confidentiality )과 무결성( Message Integrity )을 제공한다
   * 데이터는 보내기 좋게 나누고, 그 조각들을 압축한다.
   * 그 후 SHA 및 MD5 같은 알고리즘에 의해 생성된 MAC이 추가된다.
   * 데이터를 암호화한 후 마지막으로 SSL 헤더가 데이터에 추가된다.
   * 이후 TCP로 전달