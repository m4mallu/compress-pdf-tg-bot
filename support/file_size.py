import os
from humanize import naturalsize


async def get_size(path_to_file):
    file_path = str()
    for file in os.listdir(path_to_file):
        file_path = path_to_file + str(file)
    size = naturalsize(os.path.getsize(file_path))
    return size, file_path
