"""
테스트용 샘플 코드
이 파일은 코드 분석기의 테스트를 위해 만들어진 샘플입니다.
"""

# 전역 변수 예시
global_var = 10

def complex_function(x, y, z):
    """복잡한 함수 예시"""
    result = 0
    if x > 0:
        if y > 0:
            if z > 0:
                result = x + y + z
            else:
                result = x + y
        else:
            result = x
    else:
        result = 0
    
    for i in range(10):
        if i % 2 == 0:
            result += i
        else:
            result -= i
    
    return result

class SampleClass:
    """샘플 클래스"""
    
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

# 메인 실행 부분
if __name__ == "__main__":
    obj = SampleClass(42)
    print(f"Value: {obj.get_value()}")
    result = complex_function(1, 2, 3)
    print(f"Result: {result}")

