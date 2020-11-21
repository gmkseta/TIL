---
title: "[TypeScript] Type Alias"
date: "2021-04-11"
tags: ["ts", 'js']
cover: "./typescript.jpeg"
---

## Alias

```typescript
interface User {
  name: string;
}
interface Action {
  do(): void;
}
type UserAction = User & Action;
function createUserAction(): UserAction {
  return {
    do() {},
    name: ''
  }
}

type StringOrNumber = string | number;
type Arr<T> = T[];
type P<T> = Promise<T>;

type User2 = {
  name: string;
  login(): boolean;
}

class UserImpl implements User2 {
  login(): boolean {
    throw new Error("Method not implemented.");
  }
  name: string;
  
}

type UserState = "PENDING" | "APPROVED" | "REJECTED";

function checkUser(user: User2): UserState {
  if(user.login()){
    return "APPROVED";
  } else {
    return "REJECTED";
  }
}





```

