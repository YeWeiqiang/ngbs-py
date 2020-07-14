FROM selenium/node-chrome:3.5.3-boron
LABEL authors=SeleniumHQ

USER seluser

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY entry_point.sh /opt/bin/entry_point.sh

MAINTAINER rory <yeweiqiang1024@foxmail.com>

ENV SERVICE_NAME ngbs-py
ENV VERSION 1.0.0

EXPOSE 9999







