import sys

while True:
    line = sys.stdin.readline()
    if not line:  # Break if EOF
        break
    try:
        line=line.strip()
        # line=line.encode()
        line=line[:20]
    except Exception as e:
        line=str(e)
    print(f"Processed: {line}", flush=True)
