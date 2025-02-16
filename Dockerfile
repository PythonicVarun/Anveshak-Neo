# Use official Python image as base
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose necessary ports (if applicable)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["python", "run.py"]
