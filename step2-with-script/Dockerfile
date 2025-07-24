# Use a Python base with pre-compiled packages
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pandas from pre-compiled wheels only
RUN pip install --only-binary=all pandas

# Copy your Python script and data into the container
COPY read_csv.py .
COPY sample_data.csv .

# Default command now runs your script
CMD ["python", "read_csv.py"]
