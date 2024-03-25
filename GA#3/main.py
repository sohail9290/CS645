import time
from datetime import datetime
from crypto_utils import generate_rsa_keys, sign_data
from file_utils import get_file_hashes, build_merkle_tree
from github_integration import publish_to_github
from config import CONFIG

class SnapData:
    def __init__(self, merkle_root, timestamp, signature):
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.signature = signature

class SnapMgr:
    def __init__(self):
        self.priv_key, self.pub_key = generate_rsa_keys()

    def create_snapshot(self):
        dir_path = "snapshot_data"
        file_hashes = get_file_hashes(dir_path)
        merkle_root = build_merkle_tree(file_hashes)
        if merkle_root is None:
            print("No files found in the specified directory. Skipping snapshot creation.")
            return None
        timestamp = int(time.time())
        data_to_sign = merkle_root + str(timestamp).encode()
        sig = sign_data(self.priv_key, data_to_sign)
        return SnapData(merkle_root, timestamp, sig)

    def publish_snap(self, snap, snapshot_index):
        timestamp_str = datetime.fromtimestamp(snap.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        with open("data.log", "a") as f:
            f.write(f"Published:\n")
            f.write(f"Timestamp: {timestamp_str}\n")
            f.write(f"Hash: {snap.merkle_root}\n")
            f.write(f"Signature: {snap.signature}\n\n")

        publish_to_github(timestamp_str, snap.merkle_root, snap.signature, snapshot_index)
        return timestamp_str, snap.merkle_root

    def create_and_publish_snaps(self, num_snaps, interval):
        snaps = []
        for i in range(num_snaps):
            snap = self.create_snapshot()
            if snap is None:
                continue
            snaps.append(snap)
            timestamp_str, merkle_root = self.publish_snap(snap, i + 1)
            print(f"Timestamp: {timestamp_str}, Merkle Root: {merkle_root}")
            time.sleep(interval)
        return snaps

if __name__ == "__main__":
    mgr = SnapMgr()
    snaps = mgr.create_and_publish_snaps(5, 3)

    from crypto_utils import verify_signature
    for snap in snaps:
        is_valid = verify_signature(mgr.pub_key, snap.signature, snap.merkle_root + str(snap.timestamp).encode())
        print(f"Snapshot valid: {is_valid}")