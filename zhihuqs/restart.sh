#!/bin/sh

#定时监测爬虫是否在运行，没有运行则启动

while true
do
	ps -fe | grep zhihuq | grep -v grep
	if [ $? -ne 0 ]
	then
		echo "start scrapy"
		kill -9 $(pgrep scrapy)
		echo "killing scrapy,start scrapy after 10s"
		sleep 10
		scrapy crawl zhihuq
	fi
	echo "scrapy is running!"
	sleep 60
done
