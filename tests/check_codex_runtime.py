"""Optional read-only Codex Skill discovery; no authentication or model turns."""

import argparse
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import tempfile
import time

from support import SKILLS, Sandbox, copy_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default=shutil.which("codex"),
                        help="Installed Codex CLI or native executable path")
    args = parser.parse_args()
    if not args.codex:
        parser.error("Install Codex separately or provide --codex; it is not a dependency")
    executable = str(Path(args.codex).resolve())
    with tempfile.TemporaryDirectory(prefix="pgsql-toolkit-runtime-") as directory:
        sandbox = Sandbox(directory)
        copy_source(Path(directory) / "package")
        consumer = sandbox.consumer("runtime-consumer", ["codex"], "../package")
        sandbox.cli(consumer, "install")
        sandbox.cli(consumer, "compile", "--single-agents")
        codex_home = Path(directory) / "codex-state"
        codex_home.mkdir()
        # CLI wrappers may require the host's installed Node; retain only PATH,
        # never its credentials/configuration. Agent state still uses temp homes.
        env = dict(sandbox.env, CODEX_HOME=str(codex_home),
                   PATH=os.environ.get("PATH", os.defpath))
        version = subprocess.run([executable, "--version"], env=env, text=True,
                                 capture_output=True, check=True, timeout=15).stdout.strip()
        with (Path(directory) / "server-stderr").open("w+") as diagnostics:
            process = subprocess.Popen([executable, "app-server"], cwd=consumer,
                                       env=env, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=diagnostics)

            def send(message):
                process.stdin.write((json.dumps(message) + "\n").encode())
                process.stdin.flush()

            def receive(identifier):
                deadline = time.monotonic() + 15
                while time.monotonic() < deadline:
                    if select.select([process.stdout], [], [], 1)[0]:
                        line = process.stdout.readline()
                        if not line:
                            diagnostics.seek(0)
                            raise RuntimeError("App server exited: " + diagnostics.read())
                        response = json.loads(line)
                        if response.get("id") == identifier:
                            if "error" in response:
                                raise RuntimeError(response["error"])
                            return response["result"]
                raise TimeoutError("No app-server response within 15 seconds")

            try:
                send({"id": 0, "method": "initialize", "params": {
                    "clientInfo": {"name": "pgsql_toolkit_validation", "version": "0.1.0"}}})
                receive(0)
                send({"method": "initialized", "params": {}})
                send({"id": 1, "method": "skills/list", "params": {
                    "cwds": [str(consumer)], "forceReload": True}})
                result = receive(1)
                enabled = {skill["name"] for group in result["data"]
                           for skill in group["skills"] if skill.get("enabled", True)}
                errors = [error for group in result["data"] for error in group.get("errors", [])]
                if not SKILLS <= enabled or errors:
                    raise RuntimeError({"missing": sorted(SKILLS - enabled), "errors": errors})
                print(json.dumps({"version": version, "recognized_skills": sorted(SKILLS),
                                  "errors": errors, "model_turns": 0}))
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                process.stdin.close()
                process.stdout.close()


if __name__ == "__main__":
    main()
