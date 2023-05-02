FROM ubuntu

# Update and clean apt cache
RUN apt-get clean && apt-get update --fix-missing && \
    # Install utils \
    apt install -y nano ssh inetutils-ping net-tools telnet ncdu rsync whois dnsutils gosu python3 python3-pip;

COPY requirements.txt /
RUN pip3 install -r requirements.txt


COPY service_presentation.py /


ENTRYPOINT ["python3", "-m", "uvicorn" , "service_presentation:app","--host","0.0.0.0","--reload", "--port", "8080"] 

