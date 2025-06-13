import itertools

def generate_templated_numbers(template_string: str):
    """
    一个迭代器函数，根据模板字符串生成数字。
    'x' 位置可以替换为 0-9 之间的任意数字。
    数字位置必须是该数字。

    Args:
        template_string: 模板字符串，例如 "xx124xx"。

    Yields:
        符合模板规则的整数。

    Raises:
        ValueError: 如果模板字符串中包含 'x' 和数字以外的字符。
    """
    if not template_string:
        # 如果模板字符串为空，则不生成任何数字
        return

    # 存储每个位置可能的字符选择
    # 例如，对于 "xx1"，choices_per_position 会是 [['0'...'9'], ['0'...'9'], ['1']]
    choices_per_position = []
    
    # 遍历模板字符串，构建每个位置的选择列表
    for char in template_string:
        if char == 'x':
            # 'x' 可以是 0-9 任意数字
            choices_per_position.append([str(i) for i in range(10)])
        elif char.isdigit():
            # 数字位必须是该数字
            choices_per_position.append([char])
        else:
            # 模板中包含不允许的字符
            raise ValueError(f"Invalid character '{char}' in template string. Only 'x' and digits (0-9) are allowed.")

    # 使用 itertools.product 生成所有可能的组合
    # 例如，如果 choices_per_position 是 [['0', '1'], ['A', 'B']]
    # itertools.product(*choices_per_position) 会生成 ('0', 'A'), ('0', 'B'), ('1', 'A'), ('1', 'B')
    for combination_tuple in itertools.product(*choices_per_position):
        # 将组合元组中的字符连接成字符串
        number_str = "".join(combination_tuple)
        
        # 将字符串转换为整数并返回
        yield int(number_str)

# --- 使用示例 ---
if __name__ == '__main__':
    # 示例 1: "xx1"
    print("--- Generating numbers for 'xx1' ---")
    # 预期输出: 1, 11, 21, ..., 991
    for num in generate_templated_numbers("xx1"):
        print(num, end=" ")
    print("\n")

    # 示例 2: "x124x"
    print("--- Generating numbers for 'x124x' ---")
    # 预期输出: 01240, 01241, ..., 01249, 11240, ..., 91249
    # 我们可以只打印前几个和后几个来验证
    count = 0
    for num in generate_templated_numbers("x124x"):
        if count < 10 or count > 985: # 总共 10*1*1*1*10 = 100 个
            print(num, end=" ")
        elif count == 10:
            print("...", end=" ")
        count += 1
    print("\n")

    # 示例 3: "123" (没有 'x')
    print("--- Generating numbers for '123' ---")
    # 预期输出: 123
    for num in generate_templated_numbers("123"):
        print(num, end=" ")
    print("\n")

    # 示例 4: "x"
    print("--- Generating numbers for 'x' ---")
    # 预期输出: 0, 1, ..., 9
    for num in generate_templated_numbers("x"):
        print(num, end=" ")
    print("\n")

    # 示例 5: 空字符串 (不应生成任何数字)
    print("--- Generating numbers for '' ---")
    for num in generate_templated_numbers(""):
        print(num, end=" ")
    print(" (No numbers generated for empty string)")
    print("\n")

    # 示例 6: 无效字符
    print("--- Testing invalid character ---")
    try:
        for num in generate_templated_numbers("xax"):
            print(num, end=" ")
    except ValueError as e:
        print(f"Caught expected error: {e}")