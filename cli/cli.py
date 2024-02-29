import os


from filemanager import file_ext_search as fes

def search(path, ext):
    """
    prj_path_from - PDS project directory path on storage (Hard Drive, Server, etc)
    """

    path = path
    elem_list = fes.file_ext_search(extension=ext, path=path)
    elem_num = 0
    
    elem_list.sort()

    print('Scanned filesets are: \n')
    for path in elem_list:
        print(f'{elem_num} {path}')
        elem_num += 1

    return elem_list


def pick_from_list(elem_list):
    """Function Picks filesets using inputted numbers"""
    print('Please type two numbers that define the range of filesets you like to copy or move')
    a_true = True
    while a_true:
        try:
            print("Please type the first number: ")
            input_03 = int(input())
        except:
            print('Input value is incorrect. Please enter correct value (it should be integer)')
            pass
        else:
            a_true = False

    b_true = True
    while b_true:
        try:
            print("Please type the second number: ")
            input_04 = int(input())
        except:
            print('Input value is incorrect. Please enter correct value (it should be integer)')
            pass
        else:
            b_true = False

    chosen_fileset_paths_from = list()

    if input_03 == input_04:
        chosen_fileset_paths_from.append(elem_list[input_03])
    elif input_04 + 1 == len(elem_list):
        chosen_fileset_paths_from = elem_list[input_03:]
    elif input_04 < input_03:
        chosen_fileset_paths_from = elem_list[input_04:input_03+1]
    else:
        chosen_fileset_paths_from = elem_list[input_03:input_04+1]

    print('Do you want to add more elements? (Y/N)')
    input_09 = str(input())
    if input_09.lower() == 'y':
        i_true = True
        while i_true:
            try:
                print('Please type two numbers that define the range of filesets you like to copy')
                a_true = True
                while a_true:
                    try:
                        print("Please type the first number: ")
                        input_03 = int(input())
                    except:
                        print('Input value is incorrect. Please enter correct value (it should be integer)')
                        pass
                    else:
                        a_true = False

                b_true = True

                while b_true:
                    try:
                        print("Please type the second number: ")
                        input_04 = int(input())
                    except:
                        print('Input value is incorrect. Please enter correct value (it should be integer)')
                        pass
                    else:
                        b_true = False

                if input_03 == input_04:
                    chosen_fileset_paths_from.append(elem_list[input_03])
                else:
                    if input_04 + 1 == len(elem_list):
                        chosen_fileset_paths_from_add = elem_list[input_03:]
                    elif input_04 < input_03:
                        chosen_fileset_paths_from_add = elem_list[input_04:input_03+1]
                    else:
                        chosen_fileset_paths_from_add = elem_list[input_03:input_04+1]
                        
                    for fileset in chosen_fileset_paths_from_add:
                        chosen_fileset_paths_from.append(fileset)

                print("Do you want to add more? (Y/N)")
                input_10 = str(input())

                if input_10.lower() == 'y':
                    raise RuntimeError('add new numbers')
                else:
                    pass
            except:
                pass
            else:
                i_true = False

    
    print('\n')
    print('Picked elements:')
    for elem in chosen_fileset_paths_from:
        print(f'{os.path.basename(elem)}')
    
    return chosen_fileset_paths_from



