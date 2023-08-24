from utilites import extract_data
paths = {
    "home": r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Processing\src",
    "office": r"C:\Users\kazak.ke\PycharmProjects\Quote_Processing\src",
}

source_files = {
    0: (r"template_3_68_v_2.xlsx", "name"),
    3: (r"template_3_68.xlsx", "name"),
    4: (r"template_4_68.xlsx", "name"),
    5: (r"template_5_67.xlsx", "name"),
    6: (r"res_68.xlsx", "1"),
    7: (r"new_template_3_68.xlsx", "name"),
}
place = "office"    #"home" # "office"    # "home" #

# file_queue = [(source_files[x][0], paths[place], source_files[x][1]) for x in list(source_files.keys())[1:4]]

file_number = 7
src_file_info = (source_files[file_number][0], paths[place], source_files[file_number][1])
print(src_file_info)

if __name__ == "__main__":
    extract_data(src_file_info)
