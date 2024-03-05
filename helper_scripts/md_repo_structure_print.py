import os
from typing import List, Generator

global_counter = 1


class Item:
    def __init__(self, number: int, name: str, path: str):
        self.number = number
        self.name = name
        self.path = path


def should_ignore(item: str) -> bool:
    ignored_folders = [".idea", "venv", "__pycache__"]
    return item in ignored_folders or any(item.endswith(f"/{folder}") for folder in ignored_folders)


def get_items(path: str) -> Generator[str, None, None]:
    for item in os.listdir(path):
        if not should_ignore(item):
            yield item


def print_folder_structure(path: str, indent: str, items: List[Item]) -> None:
    global global_counter
    folders = [item for item in get_items(path) if os.path.isdir(os.path.abspath(os.path.join(path, item)))]
    files = [item for item in get_items(path) if not os.path.isdir(os.path.abspath(os.path.join(path, item)))]

    print_folders_in_current_path(folders, indent, items, path)

    print_files_in_current_path(files, indent, items, path)


def print_folders_in_current_path(folders, indent, items, path):
    global global_counter
    for i, folder in enumerate(folders, 1):
        folder_path = os.path.abspath(os.path.join(path, folder))
        is_last_folder = i == len(folders)
        print(f"{indent}{'└' if is_last_folder else '├'}── {folder}  ")
        global_counter += 1
        print_folder_structure(folder_path, f"{indent}{'    ' if is_last_folder else '│   '}", items)


def print_files_in_current_path(files, indent, items, path):
    global global_counter
    for i, file_item in enumerate(files, 1):
        file_path = os.path.abspath(os.path.join(path, file_item))
        is_last_file = i == len(files)
        print(f"{indent}{'└' if is_last_file else '├'}── [{global_counter} {file_item}](#{global_counter})\\\r")
        current_item = Item(global_counter, file_item, file_path)
        items.append(current_item)
        global_counter += 1


if __name__ == "__main__":
    items: List[Item] = []
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    print_folder_structure(parent_directory, "    ", items)

    print("\n\n| Item Number | Item Name | Documentation |\n|-------------|-----------|------|")
    for item in items:
        print(f"| {item.number} | [{item.name}](#{item.number}) |  |")
