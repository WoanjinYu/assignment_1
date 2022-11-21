from fileSys import fileSys, Directory, MAX_BUF_FILE_SIZE, DIR_MAX_ELEMS
import pytest


@pytest.fixture
def fileSys() -> fileSys:
    fs = fileSys()
    fs.new_directory('.', "Dir_1")

    return fs

@pytest.fixture
def fileSys_composite() -> fileSys:
    fs = fileSys()
    fs.new_directory('.', "Dir_1")
    fs.new_directory('.', "Dir_2")
    fs.new_directory('.', "Dir_3")
    fs.new_directory('./Dir_1', "Dir_11")
    fs.new_directory('./Dir_1', "Dir_12")
    fs.new_directory('./Dir_2', "Dir_21")
    fs.new_directory('./Dir_2', "Dir_22")

    return fs


def test_fileSys_creation():
    fs = fileSys()
    
    assert fs.root.name == '~'
    assert fs.root.son == []



def test_fileSys_new_directories():
    fs = fileSys()
    fs.new_directory('.', "Dir_1")
    fs.new_directory('./Dir_1', "Nested_Dir")

    assert fs.root.son[0].son[0].name == "Nested_Dir"


def test_get_node(filesystem_composite: fileSys):
    node = filesystem_composite.get_node("./Dir_1/Dir_12")

    assert isinstance(node, Directory)
    assert node.name == "Dir_12"


def test_new_binary_file(filesystem: fileSys):
    file = filesystem.new_binary_file("./Dir_1", "file.bin", "Dummy info")

    assert filesystem.root.son[0].son[0].name == "file.bin"
    assert filesystem.root.son[0].son[0].information == "Dummy info"


def test_new_log_file(filesystem: fileSys):
    file = filesystem.new_log_file("./Dir_1", "file.log", "Log info")

    assert filesystem.root.son[0].son[0].name == "file.log"
    assert filesystem.root.son[0].son[0].information == "Log info"


def test_new_buffer(filesystem: fileSys):
    file = filesystem.new_buffer("./Dir_1", "file.buf")

    assert filesystem.root.son[0].son[0].name == "file.buf"
    assert len(filesystem.root.son[0].son[0].items) == 0


def test_delete(filesystem_composite: fileSys):
    filesystem_composite.new_buffer("./Dir_1/Dir_11", "dummy.buf")

    buffer_file = filesystem_composite.get_node("./Dir_1/Dir_11/dummy.buf")
    folder = filesystem_composite.get_node("./Dir_1/Dir_11")

    buffer_file.delete()


def test_delete_2(filesystem_composite: fileSys):
    filesystem_composite.new_buffer("./Dir_1/Dir_11", "dummy.buf")
    filesystem_composite.new_log_file("./Dir_1/Dir_11", "1.log")
    filesystem_composite.new_log_file("./Dir_1/Dir_11", "2.log")
    filesystem_composite.new_log_file("./Dir_1/Dir_11", "3.log")

    target = filesystem_composite.get_node("./Dir_1/Dir_11/2.log")
    folder = filesystem_composite.get_node("./Dir_1/Dir_11")

    target.delete()


def test_binary_file_read(fileSys: fileSys):
    fileSys.new_binary_file("./Dir_1/Dir_11", "dummy.bin", "some info")
    bin_file = fileSys.get_node("./Dir_1/Dir_11/dummy.bin")

    assert (bin_file.read() == "some info")


def test_log_file_read(fileSys: fileSys):
    fileSys.new_log_file("./Dir_1/Dir_11", "dummy.log", "some info")
    log_file = fileSys.get_node("./Dir_1/Dir_11/dummy.log")
    log_file.append("\nsome more info")

    assert (log_file.read() == "some info\nsome more info")


def test_buffer_file_push(fileSys: fileSys):
    fileSys.new_buffer("./Dir_1/Dir_11", "dummy.buf")
    buffer = fileSys.get_node("./Dir_1/Dir_11/dummy.buf")

    assert len(buffer.items) == 0

    buffer.push(1)
    buffer.push(2)
    buffer.push(3)

    assert len(buffer.items) == 3


    fileSys.new_directory(".", "Dummy")
