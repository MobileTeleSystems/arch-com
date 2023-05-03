FROM ubuntu

# Update and clean apt cache
RUN apt-get clean && apt-get update --fix-missing && \
    # Install utils \
    apt install -y nano ssh inetutils-ping net-tools htop telnet curl redis-tools ncdu rsync whois dnsutils git zip gosu wget python3 python3-pip;

COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY service_db_init.py      /
COPY ExportJson.json        /


ENTRYPOINT ["python3", "service_db_init.py"] 

