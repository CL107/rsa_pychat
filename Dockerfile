### 1. Get Alpine Linux
FROM python:latest

### 2. Label
LABEL maintainer="Dockerfile created by CL107 <https://github.com/CL107> and maintained by zanda8893 <https://github.com/zanda8893>"

### 3. Get dependencies
RUN pip3 install python-dotenv

### 4. Copy server files
COPY ./server.py /rsa_pychat/server.py

### 5. Expose socket
EXPOSE 1234

### 6. Set working directory
WORKDIR /rsa_pychat

### 7. Start rsa_pychat server
CMD ["python3", "server.py"]
