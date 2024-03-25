import os
from pyascon import ascon_hash

def get_file_hashes(directory_path):
    file_hashes = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            with open(os.path.join(root, file), 'rb') as f:
                data = f.read()
                file_hashes.append(ascon_hash(data))
    return file_hashes

def build_merkle_tree(leaf_hashes):
    if not leaf_hashes:
        return None

    level_hashes = leaf_hashes[:]
    while len(level_hashes) > 1:
        new_level = []
        for i in range(0, len(level_hashes), 2):
            if i + 1 < len(level_hashes):
                combined_hash = level_hashes[i] + level_hashes[i + 1]
                new_level.append(ascon_hash(combined_hash))
            else:
                new_level.append(level_hashes[i])
        level_hashes = new_level

    return level_hashes[0]