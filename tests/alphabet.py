# def generate_column_names(length: int) -> list[str] | None:
#     """ Создает список названий столбцов таблиц excel """
#     alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#     extra = []
#     if 0 < length < 676:
#         if length > len(alphabet):
#             extra.extend(alphabet)
#             for letter in alphabet:
#                 extra.extend([f"{letter}{letter_next}" for letter_next in alphabet])
#                 if len(extra) >= length:
#                     break
#         return extra[:length]
#     return None

def generate_column_names(length: int) -> list[str] | None:
    """ Создает список названий столбцов таблиц excel """
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    extra = []
    if 0 < length < 676:
        if length > len(alphabet):
            extra.extend(alphabet)
            for letter in alphabet:
                for letter_next in alphabet:
                    extra.append(f"{letter}{letter_next}")
                    if len(extra) >= length:
                        break
                if len(extra) >= length:
                    break
            return extra[:length]
        return alphabet[:length]
    return None


l = generate_column_names(27)
print(len(l), l)

# #
# alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# print(len(alphabet))

# extrabet = []
# for letter in alphabet:
#     extrabet.extend([f"{letter}{letter_next}" for letter_next in alphabet])
#
# print(len(extrabet))
# print(extrabet)