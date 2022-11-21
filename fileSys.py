from __future__ import annotations
from typing import Any

DIR_MAX_ELEMS = 15
MAX_BUF_FILE_SIZE = 20

class fileSys():
    def __init__(self):
        self.root = Directory(self, path=[], name="~")
        self.cwd = self.root

    def path_to_string(self, path: list[Node]) -> str:
        return '/'.join(path)

    def alter_directory(self, path):
        d = self.get_node(path)
        self.cwd = d

    def create_directory(self, path: str, name: str) -> Directory:
        dest_dir = self.get_node(path)
        return dest_dir.create_directory(name)

    def create_binary_file(self, path: str, name: str, info: str) -> Binary_File:
        dest_dir = self.get_node(path)
        return dest_dir.create_binary_file(name, info)

    def create_log_file(self, path: str, name: str, info: str = None) -> Log_File:
        dest_dir = self.get_node(path)
        return dest_dir.create_log_file(name, info)

    def create_buffer(self, path: str, name: str) -> Buf:
        dest_dir = self.get_node(path)
        return dest_dir.create_buffer(name)

    def get_node(self, path) -> Node:
        return self.cwd.find_node(path)

    def print_ele(self) -> None:
        print(self.cwd.name)
        self.cwd.print_ele(lvl=0)


class Node():
    def __init__(self, path: list[Node], name: str):
        self.path = path
        self.name = name

    def delete(self):
        parent = self.path[-1]
        parent.childs.pop(parent.childs.index(self))


class Directory(Node):
    def init_(self, fs: fileSys, path: list[Node], name: str):
        if '/' in name:
            raise ValueError(f"Directory name contains {'/'}")

        super().init_(path, name)
        self.childs = []
        self.fs = fs

    def __repr__(self):
        return f"<DIR | Path: {'/'.join([d.name for d in self.path]) if self.path else ''}/[ {self.name} ]>"

    def move(self, filename: str, destination: str):
        dest_dir = self.fs.get_node(destination)

        target = None

        for c in self.childs:
            if c.name == filename:
                target = c

        if not dest_dir or not isinstance(dest_dir, Directory):
            raise ValueError("Wrong destination path")

        self.childs.remove(target)
        dest_dir.childs.append(target)

    def check_file(self, new_file_name: str) -> bool:
        if len(self.childs) == DIR_MAX_ELEMS:
            print(f"Directory can't contain more than {DIR_MAX_ELEMS} nodes")

        for child in self.childs:
            if child.name == new_file_name:
                print("File with that name already exists!")

        return True

    def create_directory(self, name: str) -> Directory:
        self.check_file(name)
        self.childs.append(Directory(self.fs, self.path + [self], name))

    def create_binary_file(self, name: str, info: str) -> Binary_File:
        self.check_file(name)

        file = Binary_File(self.path + [self], name, info)
        self.childs.append(file)

        return file


    def new_log_file(self, name: str, info: str = None) -> Log_File:
        self.check_file(name)

        file = Log_File(self.path + [self], name, info)
        self.childs.append(file)

        return file

    def new_buffer(self, name: str) -> Buf:
        self.check_file(name)

        file = Buf(self.path + [self], name)
        self.childs.append(file)

        return file

    def print_ele(self, lvl=0) -> None:
        for child in self.childs:
            print("   "*(lvl+1) + child.name)

            if isinstance(child, Directory):
                child.print_ele(lvl+1)

    def find_node(self, path):
        expect_dir_name = path.split('/')[0]
        result = None

        if expect_dir_name == '.':
            result = self
        elif expect_dir_name == '..':
            result = self.path[-1]
        elif expect_dir_name == '~':
            result = self.fs.root

        for c in self.childs:
            if c.name == expect_dir_name:
                result = c

        if '/' in path:
            return result.find_node('/'.join(path.split('/')[1:]))
        else:
            return result


class Binary_File(Node):
    def __init__(self, path: list[Node], name: str, info: str):
        super().__init__(path, name)
        self.info = info

    def read(self) -> None:
        return self.info


class Log_File(Node):
    def __init__(self, path: list[Node], name: str, info: str = ""):
            
        super().__init__(path, name)
        self.info = info

    def read(self) -> str:
        return self.info

    def append(self, info: str) -> str:
        self.info += info


class Buf(Node):
    def __init__(self, path: list[Node], name: str):
        super().__init__(path, name)
        self.items = []

    def push(self, element: Any) -> bool:
        if len(self.items) == MAX_BUF_FILE_SIZE:
            raise ValueError("BufferFile is full")

        self.items.append(element)

    def pop(self) -> bool:
        if len(self.items) == 0:
            raise ValueError("the BufferFile is empty")

        return self.items.pop()
