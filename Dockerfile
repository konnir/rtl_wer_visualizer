# Use a lightweight Python 3.11 image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Disable virtual environments for Poetry (install dependencies globally)
RUN poetry config virtualenvs.create false

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the dependencies globally
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose port 8001
EXPOSE 8001

# Run the server
CMD ["poetry", "run", "uvicorn", "rtl_stt_server:app", "--host", "0.0.0.0", "--port", "8001"]