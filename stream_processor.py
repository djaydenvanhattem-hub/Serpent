from tailer import follow

def process_stream(file_path, handler):
    for line in follow(file_path):
        handler(line)
