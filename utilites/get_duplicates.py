def get_duplicates(src_data: list) -> set:
    seen = set()
    seen_add = seen.add
    seen_twice = set(x for x in src_data if x in seen or seen_add(x))
    return seen_twice
