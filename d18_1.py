from lark import Lark

parser = Lark(r"""
    ?expr: "(" expr ")" -> sub
         | expr op expr
         | NUMBER -> number
         
    op: "*" -> multi
      | "+" -> add

    %import common.NUMBER
    %import common.WS
    %ignore WS

    """, start='expr')


def eval_tree(tree, acc: int) -> int:
    if tree.data == "number":
        return int(tree.children[0])
    if tree.data == "expr":
        if tree.children[1].data == "add":
            return eval_tree(tree.children[0], acc) + eval_tree(tree.children[2], acc)
        if tree.children[1].data == "multi":
            return eval_tree(tree.children[0], acc) * eval_tree(tree.children[2], acc)
    elif tree.data == "sub":
        pass
    else:
        raise Exception('unknown op')


def parse(expr: str) -> int:
    tree = parser.parse(expr)
    print(tree.pretty())
    return eval_tree(tree, 0)


# assert parse("2") == 2
# assert parse("2 + 1") == 3
assert parse("1 + 2 * 3") == 9
# assert parse("2 * 3 + (4 * 5)") == 26
# assert parse("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
# assert parse("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert parse("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
