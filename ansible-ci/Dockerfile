FROM drydock/u16pytall:v7.2.4

RUN mv /usr/local/bin/virtualenv /usr/local/bin/base.virtualenv
COPY intercept.virtualenv.sh /usr/local/bin/virtualenv
RUN chmod +x /usr/local/bin/virtualenv
