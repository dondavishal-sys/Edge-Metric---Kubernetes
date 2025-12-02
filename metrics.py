from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import threading
import time
from datetime import datetime

# Global metrics
cpu = 0
memory = 0
last_update = 0

# Function to update metrics every 2 seconds
def update_metrics():
    global cpu, memory, last_update
    while True:
        cpu = random.randint(1, 100)
        memory = random.randint(100, 1000)
        last_update = int(time.time() * 1000)  # timestamp in milliseconds
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Updated: CPU={cpu}%, Memory={memory}MB")
        time.sleep(2)

# HTTP Handler
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cpu, memory, last_update
        if self.path == "/metrics":
            # Add timestamp to make each response unique
            timestamp = int(time.time() * 1000)
            response = f"""# HELP cpu_usage CPU usage percentage
# TYPE cpu_usage gauge
cpu_usage {cpu}

# HELP memory_usage Memory usage in MB
# TYPE memory_usage gauge
memory_usage {memory}

# HELP last_update_timestamp Last update time
# TYPE last_update_timestamp gauge
last_update_timestamp {last_update}

# Current timestamp: {timestamp}
"""
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            # Add CORS headers if accessing from browser
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response.encode())
        elif self.path == "/":
            # Simple HTML page to view metrics with auto-refresh
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Edge Metrics</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #00ff00; }
        .metric { font-size: 24px; margin: 10px 0; }
        .time { color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <h1>Edge Device Metrics</h1>
    <div class="time">Last refresh: """ + datetime.now().strftime('%H:%M:%S') + """</div>
    <div class="metric">CPU Usage: """ + str(cpu) + """%</div>
    <div class="metric">Memory Usage: """ + str(memory) + """MB</div>
    <div class="time">Auto-refreshing every 2 seconds...</div>
    <p><a href="/metrics" style="color: #00aaff;">View Raw Metrics</a></p>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging or customize it
        pass

# Start metrics updater thread
threading.Thread(target=update_metrics, daemon=True).start()

print("=" * 50)
print("Edge Metrics Server Started")
print("=" * 50)
print("Endpoints:")
print("  - http://localhost:8080/        (HTML view)")
print("  - http://localhost:8080/metrics (Prometheus format)")
print("=" * 50)

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()