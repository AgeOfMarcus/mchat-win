FROM stefanscherer/python-windows:3.6.1-nano
LABEL maintainer="Marcus Weinberger <marcusjw.ftw@gmail.com>"
COPY ./ ./app
WORKDIR ./app
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD [ "python3", "chatroom.py" ]
