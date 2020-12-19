import re
from typing import List, Dict

regex_str = re.compile("\"\w+\"")


def build_regexp(lines: List[str], rule_no: int, rules_cache: Dict[int, str]) -> str:
    line = lines[rule_no]
    num_str, rule = line.split(":")
    num = int(num_str)
    if num in rules_cache.keys():
        return rules_cache[num]

    rule: str = rule.strip()

    if regex_str.match(rule):
        res = rule.strip('"')
        rules_cache[num] = res
        return res

    or_ind = rule.find("|")
    if or_ind >= 0:
        left, right = rule.split("|")
        left_part = ""
        for rule_no in left.strip().split(" "):
            left_part += build_regexp(lines, int(rule_no), rules_cache)
        right_part = ""
        for rule_no in right.strip().split(" "):
            right_part += build_regexp(lines, int(rule_no), rules_cache)
        res = f"(({left_part})|({right_part}))"
        rules_cache[num] = res
        return res
    else:
        res = ""
        for rule_no in rule.split(" "):
            res += build_regexp(lines, int(rule_no), rules_cache)
        res = "(" + res + ")"
        rules_cache[num] = res
        return res


def find_matches(lines: List[str], rule_no: int) -> int:
    try:
        ind = lines.index("")
    except ValueError:
        ind = lines.index("\n")
    rule_lines = lines[:ind]
    rule_list = [(int(line.split(":")[0]), line.strip()) for line in rule_lines]
    rule_list = sorted(rule_list, key=lambda tup: tup[0])
    sorted_rules = [tup[1] for tup in rule_list]

    rules_cache: Dict[int, str] = {}
    regexp_str = build_regexp(sorted_rules, rule_no, rules_cache)

    regex = re.compile(regexp_str)
    counter = 0
    for line in lines[ind + 1:]:
        line = line.strip()
        if regex.fullmatch(line):
            counter += 1
    return counter


test1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

res1 = find_matches(test1.splitlines(), 0)
assert res1 == 2

with open("i19.txt", "r") as f:
    lines = f.readlines()
res = find_matches(lines, 0)
print(res)
