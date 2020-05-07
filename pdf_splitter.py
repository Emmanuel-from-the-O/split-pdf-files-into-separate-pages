import os
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_file_names():
    """Gets the names of all the PDF files in the current working directory and returns
    a list of all the file names"""

    list_of_files = []

    # get current working directory
    directory = os.getcwd()

    # create a list containing all the pdf files in the current working directory
    try:
        print("Files: --------------------")
        for entry in os.scandir(directory):
            if entry.path.endswith(".pdf") and entry.is_file():
                list_of_files.append(entry.name)
                print(entry.name)  # for debugging
        print("--------------------------------------------------")
        print(list_of_files)  # for debugging
    except:  # I know, I know - PEP8 but idk what the error would be here
        print("exception")

    return list_of_files


def check_if_folder_exists(folder_name):
    """Checks if the folder 'folder_name' exists; if it exists, an integer is added to the 'folder_name'
    it tries again

    Note: this function adds '\\PDF Split Done' to the cwd path
    and thus all new folders are created inside 'PDF Split Done'"""

    cwd = os.getcwd()
    path_name = cwd + "\\" + folder_name
    add_on = 1

    # check if the folder to be created is  "PDF Split Done"
    # if it already exists return its name and path (we do not want something like "PDF Split Done(1)" to be made)
    if folder_name == "PDF Split Done" and os.path.isdir(path_name):
        return [path_name, folder_name]

    # This is for all the other new files to be created inside the file 'Split PDFs'
    else:
        cwd = os.getcwd()
        new_cwd = cwd + "\\" + "PDF Split Done"
        path_name = new_cwd + "\\" + folder_name
        new_folder_name = folder_name

        while os.path.isdir(path_name):
            new_folder_name = folder_name + f" ({str(add_on)})"
            path_name = new_cwd + "\\" + new_folder_name
            add_on += 1

        folder_name = new_folder_name

    path_name_folder_name_list = make_new_folder(path_name, folder_name)

    return path_name_folder_name_list


def make_new_folder(path_name, folder_name):
    """Creates a new folder inside of the folder with name 'folder_name' and path 'path_name'
    returns a list containing the folder path and folder name
    Note: the returned values are exactly the same as the function inputs"""

    try:
        # make the folder 'folder_name'
        os.makedirs(path_name)
        print("File created")
    except FileExistsError:
        print(f"file name:[{folder_name}] exists")

    list_with_names = [path_name, folder_name]

    return list_with_names


def split_pdfs(file_names, folder_to_save_in):
    """Separates the pages of the pdf files and saves them in a folder named after the pdf doc"""

    cwd = os.getcwd() + "\\" + folder_to_save_in

    list_of_new_files = []

    for each_name in file_names:

        name_with_extension_removed = each_name[:-4]
        list_with_path_name_and_folder_name = check_if_folder_exists(name_with_extension_removed)

        full_path = list_with_path_name_and_folder_name[0]
        folder_name = list_with_path_name_and_folder_name[1]

        print("_____________________________________________")
        inputpdf = PdfFileReader(open(f"{each_name}", "rb"))
        # inputpdf = PdfFileReader()

        num_pages = inputpdf.numPages

        print("------------------------------------------")
        print(f"Number of pages: {num_pages}")  # for debugging

        for i in range(0, num_pages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))

            name_of_file = f"{each_name}_page{i + 1}.pdf"
            save_path = full_path + "\\" + name_of_file
            # list_of_new_files.append(name_of_file)

            with open(save_path, 'wb') as outputStream:
                output.write(outputStream)

            index_of_current_file = file_names.index(each_name) + 1

            print(f"Working on page {i + 1} of {num_pages} in pdf {index_of_current_file} of {len(file_names)}")

    print("___________________________________________________")
    print("fin")  # for debugging


if __name__ == '__main__':
    new_dir = "PDF Split Done"
    save_list = check_if_folder_exists(new_dir)

    file_list = get_file_names()
    split_pdfs(file_list, save_list[1])

