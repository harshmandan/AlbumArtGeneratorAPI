from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import random


def draw_rectangle(draw, coordinates, color, width=1):
	for i in range(width):
		rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
		rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
		draw.rectangle((rect_start, rect_end), outline = color)	

def add_text(text, draw, font, fontsize, artistname, trackname):
	c=0
	x=100
	y=120
	marker = ImageFont.truetype(font, fontsize)
	#w, h = marker.getsize(text)
	words = text.split(" ")
	#avgword = w/len(words)
	
	for word in words:
		if(x>480):
			x=100
			y=y+70
		draw.text((x, y), word+" ", font=ImageFont.truetype(font, fontsize))
		wid, hei = marker.getsize(word+" ")
		x=x+wid

	draw.text((50,505), trackname, font=ImageFont.truetype("geoo.ttf", 20))
	draw.text((50,530), artistname, font=ImageFont.truetype("geo.ttf", 20))

def prepare_image(somelist):
	count=0
	finalitem = ""
	for item in somelist:
		if((count+len(item))>85):
			break
		else:
			finalitem = finalitem + item + " "
			count = count + len(item)
	return finalitem


# example usage


def generate_img(img, finalitem, artist, track):
	#img = Image.open(photo)
	im = img.point(lambda p: p * 0.6)
	fonts = [ 'glitter', 'learning','learningdashed','south', 'wild']

	drawing = ImageDraw.Draw(im)
	top_left = (40, 40)
	bottom_right = (560, 560)

	outline_width = 10
	outline_color = "white"

	draw_rectangle(drawing, (top_left, bottom_right), color=outline_color, width=outline_width)
	add_text(finalitem, drawing, random.choice(fonts)+".ttf", 50, artist, track)
	im.save("out.jpg", "JPEG")
	return ("out.jpg")

