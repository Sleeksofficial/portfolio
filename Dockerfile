# 1. Start from a lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first to leverage Docker caching
COPY requirements.txt ./

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app's code (app.py, images, CVs)
COPY . .

# 6. The final, correct CMD line that Render needs
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
