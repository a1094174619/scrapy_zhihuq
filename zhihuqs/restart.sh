#!/bin/sh

#定时监测爬虫是否在运行，没有运行则启动
kill -9 $(pgrep scrapy)
while true
do
	ps -fe | grep "scrapy crawl zhihuq" | grep -v grep
	if [ $? -ne 0 ]
	then
		echo "start scrapy"
		kill -9 $(pgrep scrapy)
		echo "killing scrapy,start scrapy after 10s"
		scrapy crawl zhihuq
		echo "restart scrapy"
		sleep 10
	else
		echo "scrapy is running!"
	fi
done
