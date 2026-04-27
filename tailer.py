import time

def follow(file_path):
    with open(file_path, "r", errors="ignore") as f:
        f.seek(0, 2)  # go to end of file

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line
