FROM python
COPY . /home/srv/Scripts
WORKDIR /home/srv/Scripts

RUN pip3 install requests

CMD python3 /home/srv/Scripts/aliCheck.py


