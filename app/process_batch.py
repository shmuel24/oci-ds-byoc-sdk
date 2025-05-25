import os
import sys
import time
import contextlib
import traceback
import shutil

MOUNT_ROOT = "/mnt/objects"

def upload_log(local_log_path, dest_path):
    """
    Copy the local log file into the mounted bucket directory.
    """
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(local_log_path, dest_path)
        print(f"[INFO] Log copied into bucket mount: {dest_path}")
    except Exception:
        print(f"[ERROR] Failed to copy log into bucket mount: {dest_path}", file=sys.stderr)
        traceback.print_exc()

def main():
    prefix = os.getenv("PREFIX", "")
    try:
        start = int(os.getenv("START", "0"))
        limit = int(os.getenv("LIMIT", "10"))
    except ValueError:
        print(f"[ERROR] START and LIMIT must be integers. START={os.getenv('START')}, LIMIT={os.getenv('LIMIT')}", file=sys.stderr)
        sys.exit(2)

    job_run_id = os.environ.get("JOB_RUN_OCID", "unknown-run")
    timestamp = int(time.time())
    log_file_path = "/tmp/job_output.log"
    prefix_clean = prefix.rstrip('/') if prefix else ""
    target_dir = os.path.join(MOUNT_ROOT, prefix_clean)
    log_dest_path = os.path.join(target_dir, f"job_output_{job_run_id}_{timestamp}.log")

    exit_code = 0
    try:
        with open(log_file_path, "w") as log_file, \
             contextlib.redirect_stdout(log_file), \
             contextlib.redirect_stderr(log_file):

            print(f"[INFO] Job Run ID: {job_run_id}")
            print(f"[INFO] Listing files under '{target_dir}'")

            try:
                all_files = sorted(os.listdir(target_dir))
            except FileNotFoundError:
                print(f"[WARNING] Mount directory not found: {target_dir}")
                all_files = []

            if not all_files:
                print("[WARNING] No files found.")
            else:
                batch = all_files[start:start + limit]
                end_index = start + len(batch) - 1
                print(f"[INFO] Processing files {start} to {end_index}")

                for fname in batch:
                    path = os.path.join(target_dir, fname)
                    try:
                        size = os.path.getsize(path)
                        print(f"[INFO] '{fname}' size: {size} bytes")
                    except Exception as e:
                        print(f"[ERROR] Failed to stat '{fname}': {e}")

    except Exception:
        exit_code = 1
        traceback.print_exc()

    # Copy the log into the bucket mount
    upload_log(log_file_path, log_dest_path)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
