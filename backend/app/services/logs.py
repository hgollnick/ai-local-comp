import os
import time
from fastapi.responses import StreamingResponse

def tail_lines(filename, n=100):
    """Read the last n lines from a file efficiently."""
    try:
        with open(filename, 'rb') as f:
            f.seek(0, os.SEEK_END)
            end = f.tell()
            lines = []
            size = 0
            block = 1024
            while end > 0 and len(lines) <= n:
                delta = min(block, end)
                f.seek(end - delta, os.SEEK_SET)
                buf = f.read(delta)
                lines = buf.split(b'\n') + lines
                end -= delta
            return [l.decode(errors='replace') + '\n' for l in lines[-n:] if l]
    except Exception as e:
        return [f"Error reading log file: {e}\n"]

def stream_logs_service():
    """
    Service to stream the last 100 lines from backend.log and follow new lines in real time.
    """
    def event_stream():
        logfile = "backend.log"
        if not os.path.exists(logfile):
            yield f"data: Log file not found.\n\n"
            return
        # Yield last 100 lines first
        for line in tail_lines(logfile, 100):
            yield f"data: {line.rstrip()}\n\n"
        try:
            with open(logfile, "r") as f:
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        yield f"data: {line.rstrip()}\n\n"
                    else:
                        time.sleep(0.5)
        except Exception as e:
            yield f"data: Error reading log file: {e}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
