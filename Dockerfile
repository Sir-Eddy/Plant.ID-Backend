# 1) Use the Debian python uv base image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# 2) Set the directory
WORKDIR /app

# 3) Install only the runtime bits we need (no -dev or build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1 \
      libglib2.0-0 \
      libgomp1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 4) Create and use a UV-managed venv
RUN uv venv .venv
ENV VIRTUAL_ENV=/app/.venv

# 5) Install Python deps (including ultralytics & OpenCV headless)
RUN uv pip install \
      fastapi \
      "uvicorn[standard]" \
      numpy \
      ultralytics \
      opencv-python-headless \
      python-multipart

# 6) Copy your code
COPY . .

# 7) Ensure images dir exists
RUN mkdir -p images

# 8) Expose port and run via uv
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
