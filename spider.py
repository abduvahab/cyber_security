import os
import argparse
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def download_images(url, path, images_l):
	try:
		response = requests.get(url)	
		response.raise_for_status()
		# os.makedirs(path, exist_ok=True)
		reponse_parse = BeautifulSoup(response.text, 'html.parser')
		img_tags = reponse_parse.find_all('img')
		for img_tag in img_tags:
			# Get the image URL
			image_url = urljoin(url, img_tag['src'])

			if image_url.endswith(valid_extensions):
				# Download the image
				if image_url.startswith('http') or image_url.startswith('https'):
					if "//wordpress." not in image_url:
						try:
							response = requests.get(image_url)
							response.raise_for_status()
							# Save the image to the specified directory
							# print(f"----{image_url}")
							if image_url not in images_l:
								images_l.add(image_url)
								filename = os.path.basename(urlparse(image_url).path)
								save_path = os.path.join(path, filename)
								with open(save_path, 'wb') as f:
									f.write(response.content)
								print("Image saved: {}".format(save_path))
						except requests.exceptions.ConnectionError as err:
							print("Download error occurred: {}".format(err))
							
	except requests.exceptions.RequestException as err:
		print(f"HTTP Error occurred: {err}")



def get_links(url, root):
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	links = set()
	for link in soup.find_all("a"):
		href = link.get("href")
		
		if href and (href.startswith(root)):
			links.add(href)
		
	my_links = list(links)
	# print(my_links)
	return my_links

def download_first_images(reponse_parse, path, images_l):
		img_tags = reponse_parse.find_all('img')
		for img_tag in img_tags:
			# Get the image URL
			image_url = img_tag['src']

			if image_url.endswith(valid_extensions):
				# Download the image
				if (image_url.startswith('http') or image_url.startswith('https')):
					if "//wordpress." not in image_url:
						try:
							response = requests.get(image_url)
							response.raise_for_status()
							# Save the image to the specified directory
							# print(f"----{image_url}")
							if image_url not in images_l:
								images_l.add(image_url)
								filename = os.path.basename(urlparse(image_url).path)
								save_path = os.path.join(path, filename)
								with open(save_path, 'wb') as f:
									f.write(response.content)
								print("Image saved: {}".format(save_path))
						except requests.exceptions.ConnectionError as err:
							print("Download error occurred: {}".format(err))


def get_local_links(reponse_parse):
	links=set()
	for link in reponse_parse.find_all("a"):
		href = link.get("href")
		if href and ("#" not in href):
			links.add(href)
	my_link = list(links)
	return my_link

def local_html(file_path, path, args):
	try:
		with open(file_path, 'r') as file:
			reponse_parse = BeautifulSoup(file, 'html.parser')
			images_l = set()
			if args.recursive == False and args.depth == None:
				download_first_images(reponse_parse, path, images_l)
			elif args.recursive == False and args.depth != None:
				print("flag '-l' must be used with flags '-r' ")
			elif args.recursive :
				if args.depth == None:
					args.depth = 5
				elif args.depth <= 0:
					print("flag '-l' must has a number biger than 0 ")
					return
				download_first_images(reponse_parse, path, images_l)
				i = 1
				url_list=list()
				while i < args.depth:
					url_list.append(get_local_links(reponse_parse))
					for link in url_list[i - 1]:
						download_images(link, path, images_l)
					i +=1
					
		
	except FileNotFoundError:
		print(f"File not found: {file_path}")
	except Exception as e:
		print(f"Error occurred: {e}")


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('url', help='Specify an url')
	parser.add_argument('-r','--recursive', action='store_true')
	parser.add_argument('-l', '--depth',type=int, help='Specify an depth of download')
	parser.add_argument('-p', '--path', default='./data/', help='Specify the address of download')
	args= parser.parse_args()
	depth = args.depth
	address = args.url
	path = args.path
	os.makedirs(path, exist_ok=True)
	s = address.split("/")
	if "http" not in s[0]:
		local_html(address, path, args)
	else:
		root = s[0]+ "//"+ s[2]
		p = [address]
		url_list=[p]
		images_l = set()
#		links_l = set(address)
#		links_l.add()
		if args.recursive == False and args.depth == None:
			download_images(address, path, images_l)
		elif args.recursive == False and args.depth != None:
			print("flag '-l' must be used with flags '-r' ")	
		elif args.recursive:
			if depth == None:
				depth = 5
			elif depth <= 0:
				print("flag '-l' must has a number biger than 0 ")
				return
			i = 0
			while i< depth:
				for link in url_list[i]:
					download_images(link, path, images_l)
					if i < depth -1:
						url_list .append(get_links(address, root))
				i +=1

main()