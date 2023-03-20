import hashlib
import os


def build_cache_id(filename: str, dev_mode: bool, file_hashes: dict, folder_path: str, log_hash_operations: bool):
    if not filename:
        return "ERROR_NO_FILE_PROVIDED"

    file_lw = filename.strip().lower()
    if not dev_mode and file_lw in file_hashes:
        return file_hashes[file_lw]

    if log_hash_operations:
        print("Building new hash for " + file_lw)

    fullname = os.path.abspath(os.path.join(
        folder_path, filename.lstrip('/')))

    if not os.path.exists(fullname):
        if log_hash_operations:
            print("Failed to generate hash for MISSING file " + fullname)
        return "ERROR_MISSING_FILE"
    if os.path.isdir(fullname):
        if log_hash_operations:
            print("Failed to generate hash for MISSING file " + fullname)
        return "ERROR_IS_DIRECTORY"

    file_hashes[file_lw] = get_file_hash(fullname)

    return file_hashes[file_lw]


def get_file_hash(filename):
    md5 = hashlib.md5()

    with open(filename, 'rb') as fin:
        data = fin.read()
        md5.update(data)

    return md5.hexdigest()
