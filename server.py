import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from send_sms import send_confirmation


class UpgradeHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/confirm-upgrade":
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length)) if content_length else {}

            print(f"\n--- Upgrade confirmed ---")
            print(f"Class: {body.get('upgrade_class')}")
            print(f"Seat:  {body.get('seat')}")
            print(f"Total: EUR {body.get('total')}")

            # Send RCS confirmation message
            try:
                response = send_confirmation()
                result = {"status": "ok", "message_uuid": response.message_uuid}
            except Exception as e:
                print(f"RCS send error: {e}")
                result = {"status": "ok", "note": "Confirmation displayed (RCS send failed)"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = 8080
    server = HTTPServer(("0.0.0.0", port), UpgradeHandler)
    print(f"SWISS Upgrade Server running at http://localhost:{port}")
    print(f"Open http://localhost:{port}/upgrade.html to test the flow")
    server.serve_forever()
