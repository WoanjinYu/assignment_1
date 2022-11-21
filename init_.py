
import fileSys
def filesystem():
    fs = fileSys.fileSys()
    fs.create_directory('.', "Dirctory_1")

    return fs
filesystem()