import subprocess
import tempfile
import time
from pathlib import Path
from typing import List


class DockerRunner:
    """
    Low-level Docker sandbox runner.
    Responsible ONLY for secure execution inside Docker.
    """

    def _run_container(
        self,
        *,
        image: str,
        entrypoint_cmd: List[str],
        source_files: dict[str, str],
        input_data: str,
        time_limit_sec: int,
    ) -> tuple[str, int]:
        """
        Generic docker runner.
        - image: docker image name
        - entrypoint_cmd: command inside container
        - source_files: {"filename": "content"}
        """

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp).resolve()  # Absolute path

            # Write all source files
            for filename, content in source_files.items():
                file_path = tmp_path / filename
                file_path.write_text(content)
                # Verify file was written
                if not file_path.exists():
                    raise RuntimeError(f"Failed to write file: {file_path}")

            start = time.perf_counter()

            try:
                # Use absolute path for Docker volume mount
                # Convert to string for Docker command
                volume_mount = f"{str(tmp_path)}:/code:ro"
                cmd = [
                    "docker",
                    "run",
                    "--rm",
                    "--network", "none",
                    "--cpus", "0.5",
                    "--memory", "256m",
                    "--pids-limit", "128",
                    "--read-only",
                    "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
                    "--ulimit", "fsize=1048576",
                    "--ulimit", "nofile=64:64",
                    "--security-opt", "no-new-privileges",
                    "-v", volume_mount,
                    image,
                    *entrypoint_cmd,
                ]

                result = subprocess.run(
                    cmd,
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=time_limit_sec,
                )

            except subprocess.TimeoutExpired:
                raise TimeoutError("Time limit exceeded")

            exec_time_ms = int((time.perf_counter() - start) * 1000)

            if result.returncode != 0:
                stderr = result.stderr.decode(errors="ignore")
                raise RuntimeError(stderr)

            stdout = result.stdout.decode(errors="ignore")
            return stdout, exec_time_ms

    # =========================
    # PYTHON
    # =========================
    def run_python(
        self,
        *,
        source_code: str,
        input_data: str,
        time_limit_sec: int = 2,
    ) -> tuple[str, int]:
        # Use stdin to pass code instead of volume mount
        # This avoids Docker-in-Docker path issues
        start = time.perf_counter()
        
        try:
            cmd = [
                "docker",
                "run",
                "--rm",
                "-i",  # Interactive mode for stdin
                "--network", "none",
                "--cpus", "0.5",
                "--memory", "256m",
                "--pids-limit", "128",
                "--read-only",
                "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
                "--ulimit", "fsize=1048576",
                "--ulimit", "nofile=64:64",
                "--security-opt", "no-new-privileges",
                "python:3.11-slim",
                "python", "-c", source_code,
            ]
            
            # Combine source code and input data
            full_input = input_data.encode()
            
            result = subprocess.run(
                cmd,
                input=full_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit_sec,
            )
            
        except subprocess.TimeoutExpired:
            raise TimeoutError("Time limit exceeded")
        
        exec_time_ms = int((time.perf_counter() - start) * 1000)
        
        if result.returncode != 0:
            stderr = result.stderr.decode(errors="ignore")
            raise RuntimeError(stderr)
        
        stdout = result.stdout.decode(errors="ignore")
        return stdout, exec_time_ms

    # =========================
    # C++
    # =========================
    def run_cpp(
        self,
        *,
        source_code: str,
        input_data: str,
        time_limit_sec: int = 2,
    ) -> tuple[str, int]:
        return self._run_container(
            image="gcc:13",
            entrypoint_cmd=[
                "bash",
                "-c",
                "g++ /code/main.cpp -O2 -std=c++17 -o /tmp/main && /tmp/main",
            ],
            source_files={"main.cpp": source_code},
            input_data=input_data,
            time_limit_sec=time_limit_sec,
        )

    # =========================
    # JAVASCRIPT
    # =========================
    def run_js(
        self,
        *,
        source_code: str,
        input_data: str,
        time_limit_sec: int = 2,
    ) -> tuple[str, int]:
        return self._run_container(
            image="node:20-slim",
            entrypoint_cmd=["node", "/code/main.js"],
            source_files={"main.js": source_code},
            input_data=input_data,
            time_limit_sec=time_limit_sec,
        )
