FROM python:3.9.18-slim-bullseye
COPY . /home/srv/Scripts
WORKDIR /home/srv/Scripts

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install requests
RUN pip3 install schedule
RUN pip3 install redis
RUN pip3 install lxml

CMD python3 main.py


