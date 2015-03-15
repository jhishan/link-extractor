from flask import Flask, render_template, redirect, url_for, session
from lxml import html
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'icmdkxhascfg'

@app.route('/', methods=['GET', 'POST'])
def index():
	urls = None
	form = UrlForm()
	if form.validate_on_submit():
		session['link'] = form.link.data
		urls = parse(session.get('link'))
		return render_template('index.html', form=form, link=session.get('link'), urls=urls)
	return render_template('index.html', form=form, link=session.get('link'), urls=urls)

def parse(url_string):
	requestFile = requests.get(url_string);
	tree = html.fromstring(requestFile.text)
	urlTitles = tree.xpath('//a/text()')
	urls = tree.xpath('//a/@href')
	maxLength = len(max(urls, urlTitles))
	combinedList = []
	for index in range(0,maxLength):
		try:
			combinedList.append([urlTitles[index], urls[index]])
		except IndexError:
			try:
				combinedList.append(urls[index])
			except IndexError:
				try:
					combinedList.append(urlTitles[index])
				except IndexError:
					pass
	return combinedList

class UrlForm(Form):
		link = StringField('URL', validators=[Required()])
		submit = SubmitField('Submit')


if __name__ == '__main__':
	app.run(debug=True)
