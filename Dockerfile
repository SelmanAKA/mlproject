# Use an official Python runtime as a parent image
FROM python:3.9.12

# Set the working directory to /app
WORKDIR /home/selman/Documents/Projects/mlproject

# Copy the current directory contents into the container at /app
COPY . /home/selman/Documents/Projects/mlproject

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME New_World

# Run app.py when the container launches
CMD ["python", "app.py", "--port", "5000", "--host", "0.0.0.0"]


#sudo docker run -p 5000:5000 myapp:latest
#http://localhost:5000/predictdata

