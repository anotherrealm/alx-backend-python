# Step 1: Use an official Python base image
FROM python:3.10

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app/

# Step 6: Expose the port that Django runs on
EXPOSE 8000
# docker run -p 8000:8000 messaging_app


# Step 7: Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
