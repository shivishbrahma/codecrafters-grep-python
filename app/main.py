import sys
import re
from enum import Enum
from typing import Union

# import pyparsing - available if you need it!
# import lark - available if you need it!


class RegexSingleton(Enum):
    ANY = "."
    DIGIT = "\\d"
    ALNUM = "\\w"

    @staticmethod
    def is_singleton(string: str):
        return string in RegexSingleton._value2member_map_


def tokenize(pattern: str):
    tokens = []
    i = 0
    while i < len(pattern):
        if pattern[i] == "\\":
            if i + 1 < len(pattern):
                tokens.append(pattern[i : i + 2])
                i += 2
            else:
                raise ValueError("Invalid escape sequence")
        elif pattern[i] == "[":
            j = i + 1
            while j < len(pattern) and pattern[j] != "]":
                j += 1
            if j < len(pattern):
                tokens.append(pattern[i : j + 1])
                i = j + 1
        else:
            tokens.append(pattern[i])
            i += 1

    return tokens


def match_token(pattern_token: Union[RegexSingleton, str], string: str):
    if pattern_token == RegexSingleton.DIGIT:
        return string.isdigit()
    elif pattern_token == RegexSingleton.ALNUM:
        return string.isalnum() or string == "_"
    if isinstance(pattern_token, RegexSingleton):
        raise RuntimeError(f"Unhandled pattern: {pattern_token}")

    if pattern_token.startswith("[^") and pattern_token.endswith("]"):
        return not all(char in pattern_token[2:-1] for char in string)
    elif pattern_token.startswith("[") and pattern_token.endswith("]"):
        return any(char in pattern_token[1:-1] for char in string)

    return pattern_token == string


def match_at_position(line, tokens, pos):
    if pos + len(tokens) > len(line):
        return False
    for i in range(len(tokens)):
        if RegexSingleton.is_singleton(tokens[i]):
            if not match_token(RegexSingleton(tokens[i]), line[pos + i]):
                # print("False", RegexSingleton(tokens[i]).value, repr(line[pos + i]))
                return False
        elif len(tokens[i]) == 1:
            if not match_token(tokens[i], line[pos + i]):
                # print("False", repr(tokens[i]), line[pos + i])
                return False
        else:
            if not match_token(tokens[i], line[pos + i :]):
                # print("False", repr(tokens[i]), line[pos + i :])
                return False

    return True


def match_pattern(input_line: str, pattern: str):
    is_start = False
    if pattern[0] == "^":
        pattern = pattern[1:]
        is_start = True

    tokens = tokenize(pattern)
    input_line = input_line.strip()
    print(tokens, input_line)
    for pos in range(len(input_line) - len(tokens) + 1):
        if match_at_position(input_line, tokens, pos):
            print("Pattern matched")
            return True
        if is_start  and pos == 0:
            return False
    return False


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
