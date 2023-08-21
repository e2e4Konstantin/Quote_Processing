from utilites import parse_file_with_quotes
paths = {
    "home": r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\1_targets\tasck_2\sources",
    "office": r"*",
}

source_files = {
    0: (r"template_3_68_v_2.xlsx", "name"),
    3: (r"template_3_68.xlsx", "name"),
    4: (r"template_4_68.xlsx", "name"),
    5: (r"template_5_67.xlsx", "name"),
    6: (r"res_68.xlsx", "1")
}
place = "home" # "office"

# file_queue = [(source_files[x][0], paths[place], source_files[x][1]) for x in list(source_files.keys())[1:4]]

file_number = 3
src_file_info = (source_files[file_number][0], paths[place], source_files[file_number][1])
print(src_file_info)

if __name__ == "__main__":
    parse_file_with_quotes(src_file_info)
