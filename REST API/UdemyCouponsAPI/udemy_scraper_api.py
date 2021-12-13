from bs4 import BeautifulSoup
from flask import Flask, jsonify
from googlesearch import search
import json
from time import sleep
import requests

app = Flask("udemy_coupons_api")

courses_last = {"source": "geeksgod", "courses": []}

def coupon_scraper(url):
	content = requests.get(url).text
	soup = BeautifulSoup(content, 'lxml')
	coupon = soup.find('p', class_ = 'elementor-heading-title elementor-size-default').text
	return coupon

def udemy_link(title):
	query = title+' udemy course'
	for j in search(query, tld="com", num=1, stop=1, pause=1):
		return j

#home
@app.route("/")
def root():
	return jsonify({"name" : "udemy_coupons_api",
			"info"  : "scrapes udemy coupons",
			"paths" : { "/" : "home page",
				"/scrape"  : "scrapes coupons and saves in json file",
				"/coupons" : "gives the scraped coupons"
			}
		})

#scraper endpoint
@app.route("/scrape")
def scraper():
	content = requests.get('http://geeksgod.com/category/freecoupons/udemy-courses-free').text
	soup = BeautifulSoup(content, 'lxml')

	sleep(4)
	courses = soup.find_all('div', class_ = 'item-details')

	for course in courses:
		course_json = dict()

		try:
			coupon = coupon_scraper(course.a["href"])
			if coupon == None:
				continue

			title = course.h3.text
			dat = course.time.text
			udemylink = udemy_link(title)

			course_json['title'] = title
			course_json['link'] = udemylink
			course_json['date'] = dat
			course_json['coupon'] = coupon
			course_json['enroll'] = f'{udemylink}?couponCode={coupon}'

			courses_last['courses'].append(course_json)

		except:
			pass

		final = json.dumps(courses_last, indent=4)
		file = open('courses.json', 'a')
		file.write(final)
		file.close()

		return jsonify({"response" : "done", "course_count" : f"scraped 18 course coupons"})

#coupons endpoint
@app.route("/coupons")
def coupons():
	f = open("courses.json")
	data = json.load(f)
	return jsonify(data)

app.run()
