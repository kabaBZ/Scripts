FROM python
COPY . /home/srv/Scripts
WORKDIR /home/srv/Scripts

RUN pip3 install requests
RUN pip3 install schedule

CMD python3 main.py


