from operator import itemgetter
import requests
import plotly.express as px

# 执行 APi 请求
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# 处理有挂每篇文章的信息
submission_ids = r.json()
submissions_dicts = []
for submission_id in submission_ids:
	# 对于每篇文章，执行api请求
	url = (f"https://hacker-news.firebaseio.com/v0/item/"
		   f"{submission_id}.json")
	r = requests.get(url)
	print(f"id: {submission_id}\tstatus: {r.status_code}")
	response = r.json()

	# 对于每篇文章，都创建一个字典
	try:
		submission_dict = {
			'title': response['title'],
			'hn_link': f"https://news.ycombinator.com/item?id=/{submission_id}",
			'comments': response['descendants'],
		}
	except:
		continue
	else:
		submissions_dicts.append(submission_dict)

submissions_dicts = sorted(submissions_dicts, key=itemgetter('comments'),
						   reverse=True)
links, comments = [], []

for submission_dict in submissions_dicts:
	article_title = submission_dict['title']
	url = submission_dict['hn_link']
	link = f"<a href='{url}'>{article_title}</a>"
	comment = submission_dict['comments']
	links.append(link)
	comments.append(comment)

# 可视化
title = "hacker news submissions"
labels = {'x': 'Articles', 'y': 'Comments'}
fig = px.bar(x=links, y=comments, title=title, labels=labels)
fig.update_layout(title_font_size=28, xaxis_title_font_size=18,
				  yaxis_title_font_size=18)
fig.update_traces(marker_color='SkyBlue', marker_opacity=0.6)
fig.show()

