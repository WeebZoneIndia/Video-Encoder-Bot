# Import Ubuntu
FROM ubuntu:20.04

# Make /app dir
RUN mkdir /app
RUN chmod 777 /app
WORKDIR /app

# Installation of Requirements
COPY . .
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
RUN apt update && apt install -y --no-install-recommends git wget aria2 curl busybox python3 python3-pip p7zip-full p7zip-rar unzip mkvtoolnix ffmpeg
RUN pip3 install --no-cache-dir -r requirements.txt

# For Extraction of archieved files
RUN chmod +x extract

# Start bot
CMD ["bash", "run.sh"]
