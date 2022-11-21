from __future__ import annotations
from typing import Any

DIR_MAX_ELEMS = 15
MAX_BUF_FILE_SIZE = 20

class fileSys():
    def __init__(object):
        object.root = Directory(object, path=[], name="~")
        object.cwd = object.root

    def path_to_string(object, path: list[Node]) -> str:
        return '/'.join(path)

    def alter_directory(object, path):
        d = object.get_node(path)
        object.cwd = d

    def create_directory(object, path: str, name: str) -> Directory:
        dest_dir = object.get_node(path)
        return dest_dir.create_directory(name)

    def create_binary_file(object, path: str, name: str, info: str) -> Binary_File:
        dest_dir = object.get_node(path)
        return dest_dir.create_binary_file(name, info)

    def create_log_file(object, path: str, name: str, info: str = None) -> Log_File:
        dest_dir = object.get_node(path)
        return dest_dir.create_log_file(name, info)

    def create_buffer(object, path: str, name: str) -> Buf:
        dest_dir = object.get_node(path)
        return dest_dir.create_buffer(name)

    def get_node(object, path) -> Node:
        return object.cwd.find_node(path)

    def print_ele(object) -> None:
        print(object.cwd.name)
        object.cwd.print_ele(lvl=0)


class Node():
    def __init__(object, path: list[Node], name: str):
        object.path = path
        object.name = name

    def delete(object):
        parent = object.path[-1]
        parent.childs.pop(parent.childs.index(object))


class Directory(Node):
    def init_(object, fs: fileSys, path: list[Node], name: str):
        if '/' in name:
            raise ValueError(f"Directory name contains {'/'}")

        super().init_(path, name)
        object.childs = []
        object.fs = fs

    def __repr__(object):
        return f"<DIR | Path: {'/'.join([d.name for d in object.path]) if object.path else ''}/[ {object.name} ]>"

    def move(object, filename: str, destination: str):
        dest_dir = object.fs.get_node(destination)

        target = None

        for c in object.childs:
            if c.name == filename:
                target = c

        if not dest_dir or not isinstance(dest_dir, Directory):
            raise ValueError("Wrong destination path")

        object.childs.remove(target)
        dest_dir.childs.append(target)

    def check_file(object, new_file_name: str) -> bool:
        if len(object.childs) == DIR_MAX_ELEMS:
            print(f"Directory can't contain more than {DIR_MAX_ELEMS} nodes")

        for child in object.childs:
            if child.name == new_file_name:
                print("File with that name already exists!")

        return True

    def create_directory(object, name: str) -> Directory:
        object.check_file(name)
        object.childs.append(Directory(object.fs, object.path + [object], name))

    def create_binary_file(object, name: str, info: str) -> Binary_File:
        object.check_file(name)

        file = Binary_File(object.path + [object], name, info)
        object.childs.append(file)

        return file


    def new_log_file(object, name: str, info: str = None) -> Log_File:
        object.check_file(name)

        file = Log_File(object.path + [object], name, info)
        object.childs.append(file)

        return file

    def new_buffer(object, name: str) -> Buf:
        object.check_file(name)

        file = Buf(object.path + [object], name)
        object.childs.append(file)

        return file

    def print_ele(object, lvl=0) -> None:
        for child in object.childs:
            print("   "*(lvl+1) + child.name)

            if isinstance(child, Directory):
                child.print_ele(lvl+1)

    def find_node(object, path):
        expect_dir_name = path.split('/')[0]
        result = None

        if expect_dir_name == '.':
            result = object
        elif expect_dir_name == '..':
            result = object.path[-1]
        elif expect_dir_name == '~':
            result = object.fs.root

        for c in object.childs:
            if c.name == expect_dir_name:
                result = c

        if '/' in path:
            return result.find_node('/'.join(path.split('/')[1:]))
        else:
            return result


class Binary_File(Node):
    def __init__(object, path: list[Node], name: str, info: str):
        super().__init__(path, name)
        object.info = info

    def read(object) -> None:
        return object.info


class Log_File(Node):
    def __init__(object, path: list[Node], name: str, info: str = ""):
            
        super().__init__(path, name)
        object.info = info

    def read(object) -> str:
        return object.info

    def append(object, info: str) -> str:
        object.info += info


class Buf(Node):
    def __init__(object, path: list[Node], name: str):
        super().__init__(path, name)
        object.items = []

    def push(object, element: Any) -> bool:
        if len(object.items) == MAX_BUF_FILE_SIZE:
            raise ValueError("BufferFile is full")

        object.items.append(element)

    def pop(object) -> bool:
        if len(object.items) == 0:
            raise ValueError("the BufferFile is empty")

        return object.items.pop()
