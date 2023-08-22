src = [1, 2, 3, 2, 1, 5, 6, 5, 5, 5]


def get_duplicates(src_data: list) -> set:
    seen = set()
    seen_add = seen.add
    seen_twice = set(x for x in src if x in seen or seen_add(x))
    return seen_twice

print(get_duplicates(src))

#
#
# seen = set()
# u = [x for x in src if x in seen or seen.add(x)]
# print(src)
# print(seen)
# print(u)
# print(set(u))
#
# src_set = set(src)
# du = [x for x in src if x in src_set]
# print(src_set)
# print(du)
