# How to Docker

## What is Docker?
<img src="docker-logo-png-transparent.png" alt="Docker Logo" width="120" align="right" style="margin-left: 20px; margin-bottom: 10px;"/>

Docker is a platform that uses containerization technology to package applications and their dependencies into lightweight, portable containers. Think of Docker containers as standardized shipping containers for software - they contain everything needed to run an application: code, runtime, system tools, libraries, and settings.

### Breaking Down What's Inside a Container:

**Code:** Your actual application - Python scripts, JavaScript files, Java classes, etc. <br>
**Runtime:** The execution environment needed to run your code (Python interpreter, Node.js runtime, Java Virtual Machine, etc.) <br>
**System Tools**: Basic operating system utilities like bash, curl, wget, file managers, and command-line tools your application might need <br>
**Libraries:** Pre-compiled code that your application depends on - think NumPy for Python, jQuery for JavaScript, or .jar files for Java <br>
**Settings:** Configuration files, environment variables, and system configurations that tell your application how to behave <br>

### Key Features of Docker:
- **Containerization**: Packages applications with all dependencies
- **Portability**: "Write once, run anywhere" - containers work across different environments
- **Isolation**: Each container runs in its own isolated environment
- **Efficiency**: Containers share the host OS kernel, making them lightweight
- **Scalability**: Easy to scale applications up or down
- **Version Control**: Docker images can be versioned and shared via registries

### Docker Architecture:

Understanding Docker's components is crucial for beginners. Think of it like building and running a house - you need blueprints, materials, builders, and a place to store everything.

- **Docker Engine**: The runtime that manages containers
  - This is like the construction crew that actually builds and runs your containers
  - It's the background service (daemon) running on your computer that does all the heavy lifting
  - You interact with it through commands like `docker build` and `docker run`

- **Docker Images**: Read-only templates used to create containers  
  - Think of these as blueprints or snapshots of your application
  - They contain your application code plus all the dependencies frozen in time
  - Images are built in layers (like onion layers) - each instruction in your Dockerfile creates a new layer
  - Once created, images never change - they're immutable

- **Docker Containers**: Running instances of Docker images
  - These are your actual running applications - like a house built from the blueprint
  - Multiple containers can be created from the same image (like building multiple identical houses)
  - Containers can be started, stopped, deleted, and recreated
  - Each container runs in isolation from others

- **Dockerfile**: Text file with instructions to build Docker images
  - This is your recipe or blueprint file that tells Docker how to build your image
  - Written in plain text with specific commands (FROM, RUN, COPY, etc.)
  - Must be named exactly "Dockerfile" (no file extension)
  - Lives in your project directory alongside your application code

- **Docker Registry**: Storage for Docker images (e.g., Docker Hub)
  - Think of this as a library or warehouse where Docker images are stored and shared
  - Docker Hub is the public registry (like GitHub for code, but for Docker images)
  - You can pull (download) images others have created, or push (upload) your own

# Docker Step-by-Step Tutorial: From Simple to Complex

Let's learn Docker by building progressively more complex containers, starting with a simple pandas installation and ending with a complete data analysis application.

## Step 1: Simple Docker Container with Pandas

**Goal**: Create a basic Docker container that just has pandas installed

### Files needed:
- `Dockerfile` only

### 1. Create your Dockerfile

Create a file named exactly `Dockerfile` (no extension) in an empty directory:

```dockerfile
# Use a Python base with pre-compiled packages
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pandas from pre-compiled wheels only
RUN pip install --only-binary=all pandas

CMD ["/bin/bash"]
```

**What each line does:**
- `FROM python:3.9-slim`: Start with a lightweight Python 3.9 image
- `WORKDIR /app`: Set the working directory inside the container
- `RUN apt-get update...`: Install system tools needed for compilation
- `RUN pip install --only-binary=all pandas`: Install pandas using pre-built packages (faster, no compilation)
- `CMD ["/bin/bash"]`: When container starts, open a bash shell

### 2. Build and test the container

```bash
# Build the image
docker build -t pandas-simple .

# Run the container interactively
docker run -it pandas-simple

# Inside the container, test pandas
python -c "import pandas as pd; print('Pandas version:', pd.__version__)"
```

**Project structure:**
```
step1-simple/
└── Dockerfile
```

---

## Step 2: Docker Container with Pandas + Python Script

**Goal**: Add a Python script that reads a CSV file using pandas

### Files needed:
- `Dockerfile`
- `read_csv.py` (your Python script)
- `sample_data.csv` (test data)

### 1. Create your Python script

Create `read_csv.py`:
```python
import pandas as pd
import sys
import os

def main():
    # Check if CSV file exists
    csv_file = 'sample_data.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    # Read CSV file
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Display basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nBasic statistics:")
    print(df.describe())

if __name__ == "__main__":
    main()
```

### 2. Create sample data

Create `sample_data.csv`:
```csv
name,age,city,salary
Alice,25,New York,70000
Bob,30,London,65000
Charlie,35,Tokyo,80000
Diana,28,Paris,72000
Eve,32,Berlin,68000
```

### 3. Update your Dockerfile

```dockerfile
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
```

**What's new:**
- `COPY read_csv.py .`: Copies your Python script into the container
- `COPY sample_data.csv .`: Copies your test data into the container  
- `CMD ["python", "read_csv.py"]`: When container starts, run your script instead of bash

### 4. Build and test

```bash
# Build the updated image
docker build -t pandas-with-script .

# Run the container (it will automatically run your script)
docker run pandas-with-script

# Run interactively if you want to explore
docker run -it pandas-with-script /bin/bash
```

**Project structure:**
```
step2-with-script/
├── Dockerfile
├── read_csv.py
└── sample_data.csv
```

---

## Step 3: Docker Container with External Data

**Goal**: Mount external CSV files from your computer into the container

### Files needed:
- `Dockerfile` (same as Step 2)
- `read_csv.py` (updated to handle different files)
- External CSV files on your computer

### 1. Update your Python script

Create `flexible_csv_reader.py`:
```python
import pandas as pd
import sys
import os

def main():
    # Check if a CSV file was provided as argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'sample_data.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("Available files:")
        print(os.listdir('.'))
        return
    
    # Read and analyze CSV file
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    if df.select_dtypes(include=['number']).shape[1] > 0:
        print("\nNumerical statistics:")
        print(df.describe())

if __name__ == "__main__":
    main()
```

### 2. Update Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --only-binary=all pandas

# Copy the flexible script
COPY flexible_csv_reader.py .
COPY sample_data.csv .

CMD ["python", "flexible_csv_reader.py"]
```

### 3. Build and test with external data

```bash
# Build the image
docker build -t pandas-flexible .

# Run with default data
docker run pandas-flexible

# Run with your own CSV file (mount external directory)
docker run -v /path/to/your/data:/app/data pandas-flexible python flexible_csv_reader.py data/your_file.csv

# Run interactively to explore your data
docker run -it -v $(pwd):/app/data pandas-flexible /bin/bash
```

**Project structure:**
```
step3-external-data/
├── Dockerfile
├── flexible_csv_reader.py
├── sample_data.csv
└── your-external-data/
    ├── sales_data.csv
    ├── customer_data.csv
    └── inventory.csv
```

## Key Learning Points

1. **Step 1**: Learn basic Dockerfile structure and package installation
2. **Step 2**: Learn how to add your code and data to containers  
3. **Step 3**: Learn how to work with external data using volume mounts

**Next Steps**: You could extend this to add data visualization, database connections, or web interfaces!

Each step builds on the previous one, making it easy for beginners to understand how Docker containers evolve from simple to complex applications.

## Summary

- **Docker** excels in enterprise environments, web development, and cloud deployments where you have administrative control
- **Singularity** shines in academic and research environments, particularly HPC clusters where security and user permissions matter
- Both technologies solve the "it works on my machine" problem but for different computing environments
- The choice often depends on your computing environment and organizational policies rather than technical superiority

Understanding both technologies allows you to choose the right tool for your specific use case and computing environment.

---

## What is Singularity/Apptainer?
Singularity (now called Apptainer) is a container platform designed specifically for high-performance computing (HPC) and scientific workflows. It was created to address the security and usability challenges that Docker faces in shared computing environments like academic clusters and supercomputers.

