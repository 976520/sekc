# 셐시lang

## 1. 변수

**상태 변경 (Mutation)**
`set` 키워드를 사용하여 기존 변수의 값을 변경하거나 설정합니다.
```sekc
set 10 in x
set "Hello" in message
```

**바인딩 (Binding)**
`=>` 연산자를 사용하여 불변 값을 바인딩합니다.
```sekc
pi => 3.14
x => 10
```

## 2. 함수

**함수 정의 (Definitions)**
`define` 키워드를 사용합니다. Python과 유사하게 들여쓰기(Indentation)로 블록을 구분합니다.
```sekc
define add(a, b)
    return a + b
```
이렇게 단일 표현식으로 쓸 수도 있음
```sekc
define square(x) => x * x
```
**익명 함수 (Anonymous Func)**
```sekc
(x) => x * x
```

**함수 호출**
```sekc
add(10, 20)
square(5)
```

## 3. 제어문

**조건문 (Conditionals)**
```sekc
if x is 10
    print "Ten"
```
*(현재 `else`는 구현되지 않음)*

**반복문 (Loops)**
`repeat while` 구문을 사용합니다.
```sekc
repeat while count < 10
    print count
    set count + 1 in count
```

*   `break`: 루프 종료
*   `continue`: 다음 반복으로 이동
*   `return value`: 함수 반환

## 4. I/O

**출력 (Print)**
표현식을 평가하여 표준 출력에 출력합니다.
```sekc
print "Hello World"
print 10 + 20
```

**입력 (Read)**
사용자 입력을 받아 변수에 저장합니다.
```sekc
read input into name
print name
```

## 5. 연산자

*   **산술**: `+`, `-`
*   **논리**: `and`, `or`, `not`
*   **비교**: `is` (동등), `is not` (부등)
*   **파이프**: `->` (값 전달)
    ```sekc
    10 -> print  # print(10)과 동일
    ```

## 6. 자료형
*   **Number**: 실수형 (Double)
*   **String**: 큰따옴표로 감싼 문자열 (`"Text"`)
*   **Boolean**: `true`, `false`
*   **Null**: `null`

## 7. 컴포넌트 (Components & Closures)

**"모든 것은 함수이자 객체입니다."**
별도의 `class` 키워드 없이, 함수(클로저)를 통해 데이터를 캡슐화하고 객체를 생성합니다. 리액트 훅(React Hook)이나 JS의 팩토리 패턴과 유사합니다.

**객체 리터럴 (Object Literal)**
데이터 묶음을 표현합니다.
```sekc
me => { name: "Sekc", age: 1 }
print me.name
```

**상태를 가진 컴포넌트 (Stateful Component)**
함수 내부 변수(Closure)를 통해 상태를 관리합니다.
```sekc
define Counter(start)
    # 1. 상태 (State) - 클로저에 의해 캡슐화됨
    set start in count

    # 2. 메서드 (Methods)
    define up()
        set count + 1 in count
        return count

    # 3. 인터페이스 반환 (Return Interface)
    return {
        increment: up,
        current: () => count
    }

# 사용 (Usage)
c => Counter(10)
print c.increment()  # 11
print c.increment()  # 12
```

**싱글톤 (Singleton)**
함수를 실행한 결과를 바로 바인딩하면 싱글톤이 됩니다.
```sekc
GlobalConfig => (define()
    return { theme: "Dark" }
)()
```

## 9. 고급 바인딩 (Advanced Binding)

**구조 분해 (Destructuring)**
복잡한 데이터를 직관적으로 풀어서 바인딩합니다.
```sekc
[x, y] => point
print x
print y
```
