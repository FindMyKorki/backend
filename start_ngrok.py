import time
import requests
import subprocess

ENV_FILE = "/app/.env"

def wait_for_ngrok():
    print("[⏳] Waiting for ngrok tunnel...")
    for i in range(30):
        try:
            r = requests.get("http://ngrok:4040/api/tunnels").json()
            tunnels = r.get("tunnels", [])
            if tunnels:
                for tunnel in tunnels:
                    if tunnel["proto"] == "https":
                        return tunnel["public_url"]
                return tunnels[0]["public_url"]
        except Exception:
            pass
        time.sleep(1)
        print(f"  ... still waiting ({i+1}s)")
    raise RuntimeError("Ngrok tunnel did not start in time.")

def update_env(ngrok_url):
    print(f"[⚙️] Updating {ENV_FILE} with BACKEND_URL={ngrok_url}")
    updated = False
    lines = []
    with open(ENV_FILE, "r") as f:
        for line in f:
            if line.startswith("BACKEND_URL="):
                lines.append(f"BACKEND_URL={ngrok_url}\n")
                updated = True
            else:
                lines.append(line)

    if not updated:
        lines.append(f"BACKEND_URL={ngrok_url}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(lines)

def restart_backend():
    print("♻️ Restarting backend container...")

    # Find container name that includes '_backend_'
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True
    )
    container_names = result.stdout.splitlines()

    backend_container = next((name for name in container_names if "backend" in name), None)

    if not backend_container:
        raise RuntimeError("❌ Could not find backend container to restart.")

    subprocess.run(["docker", "restart", backend_container], check=True)

if __name__ == "__main__":
    ngrok_url = wait_for_ngrok()
    update_env(ngrok_url)
    restart_backend()
