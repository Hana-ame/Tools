import sys


def nginx_parser(line: str):
    r = {
        "'": "'",
        '"': '"',
        "[": "]",
        "]": "[",
    }
    stack = []
    words = []
    word = []
    for letter in line:
        if letter == " " and len(stack) == 0:
            if len(word) != 0:
                words.append("".join(word))
                word = []
            else:
                pass
        elif letter in ['"', "'", "[", "]"]:
            if len(stack) > 0 and stack[-1] == r[letter]:
                stack.pop()
                if len(stack) == 0:
                    words.append("".join(word))
                    word = []
            else:
                stack.append(letter)
        else:
            # print(f"append letter {letter}")
            word.append(letter)
    return words


if __name__ == "__main__":
    freq_dict = {}

    def handler(line: str):
        words = nginx_parser(line)
        freq_dict[words[0]] = freq_dict.get(words[0], 0) + 1

    while True:
        line = sys.stdin.readline()
        if not line:  # Break if EOF
            break
        try:
            handler(line)
        except Exception as e:
            line = str(e)

    # 将字典按值（频数）降序排序
    sorted_dict = dict(
        sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    )
    for k in sorted_dict:
        print(k,sorted_dict[k])
