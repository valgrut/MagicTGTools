import os
from os.path import exists
from cairosvg import svg2png
from flask import Flask, redirect, url_for, render_template, request, session, flash
from markupsafe import escape
import csv
import ssl
from datetime import datetime
import requests
import re

# https://aetherhub.com/Card/Set
# https://mythicspoiler.com/sets.html
# https://gatherer.wizards.com/Handlers/Image.ashx?type=symbol&set=DTK&size=large&rarity=U

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

RARITY_COLORS = {
	"C": "#000000",  # common (black)
	"U": "#6f6f6f",  # uncommon (gray)
	"R": "#be8a2a",  # rare (gold-ish)
	"M": "#c44f27",  # mythic (orange-ish)
}

def fetch_set_svg(set_code: str) -> str:
	"""
	Get Scryfall set by the code / shortcut.
	"""
	response = requests.get(f"https://api.scryfall.com/sets/{set_code.lower()}", timeout=20)
	response.raise_for_status()
	response_json = response.json()
	return response_json["icon_svg_uri"]

def colorize_svg(svg_bytes: bytes, hex_color: str) -> bytes:
    """
    Colorize a set symbol SVG
    
    There can be multiple ways the fetched symbol is colored, so this method covers all those 
    ways, so the symbol is colored correctly every time.
    """
    txt = svg_bytes.decode("utf-8")

    # 1) replace currentColor
    txt = txt.replace("currentColor", hex_color)

    # 2) replace explicit black fills/strokes
    txt = re.sub(r'fill="(#000|#000000|black)"', f'fill="{hex_color}"', txt, flags=re.IGNORECASE)
    txt = re.sub(r"fill='(#000|#000000|black)'", f"fill='{hex_color}'", txt, flags=re.IGNORECASE)
    txt = re.sub(r'stroke="(#000|#000000|black)"', f'stroke="{hex_color}"', txt, flags=re.IGNORECASE)
    txt = re.sub(r"stroke='(#000|#000000|black)'", f"stroke='{hex_color}'", txt, flags=re.IGNORECASE)

    # 3) if there is still no fill anywhere, inject it into each path
    if "fill=" not in txt and "stroke=" not in txt and "style=" not in txt:
        txt = re.sub(r"<path\b", f'<path fill="{hex_color}"', txt)

    return txt.encode("utf-8")

def make_symbol_png(set_code: str, rarity: str, size_px: int, out_path: str):
	"""
	Fetch symbol from the source page, colorize it based on requested options and save as png.
	"""

	svg_url = fetch_set_svg(set_code)
	svg_bytes = requests.get(svg_url, timeout=20).content
	colored_svg = colorize_svg(svg_bytes, RARITY_COLORS[rarity])
	os.makedirs(os.path.dirname(out_path), exist_ok=True)
	svg2png(bytestring=colored_svg, write_to=out_path, output_width=size_px, output_height=size_px)


@app.route('/')
def home():
	# Fetch first 6 set shortcuts from csv file
	prefilled_sets = ""
	csv_file = csv.reader(open('sets-list.csv', "r"), delimiter=";")
	max_row = 5
	current_row = 0
	for row in csv_file:
		prefilled_sets += row[0]
		if current_row >= max_row:
			break
		prefilled_sets += ","
		current_row += 1
		# print(prefilled_sets)

	return render_template('index.html', PREFILLED_SETS=prefilled_sets)

def debug_svg(svg_text: str):
	for token in [
		'currentColor',
		'fill="none"',
		"fill='none'",
		'stroke=',
		'fill=',
		'style=',
		'<mask',
		'<clipPath',
		'<defs',
	]:
		print(token, token in svg_text)

@app.route('/generated-labels', methods = ['GET', 'POST'])
def generate_labels():
	if request.method != 'POST':
		print(f"Request method '{request.method}' not expected! Quitting.")
		return

	list_of_expansions = request.form['expansions_list']
	label_type = request.form['label_type']
	selected_label_rarities = request.form.getlist('label_rarity')
	label_background_colors = request.form.getlist('label_background_color')

	# Validate provided expansions shortcuts and to prevent hacking, xss, ...
	list_of_expansions = escape(list_of_expansions)

	# Remove any whitespaces from input
	list_of_expansions = list_of_expansions.replace(" ", "")
	raw_split_list_of_expansions = list_of_expansions.split(',')

	# print(raw_split_list_of_expansions)
	split_list_of_expansions = [expansion.strip() for expansion in raw_split_list_of_expansions]
	# print(split_list_of_expansions)

	set_info_list = []
	for expansion in split_list_of_expansions:
		for label_rarity in selected_label_rarities:
			expansion_info = []
			csv_file = csv.reader(open('sets-list.csv', "r"), delimiter=";")

			# Get information based on the expansion shortcut
			for row in csv_file:
				expansion = expansion.upper()
				set_shortcut = row[0]
				set_name = row[1]
				set_release_date = row[2]
				if expansion != set_shortcut:
					continue

				expansion_info.append(set_shortcut)  # Shortcut
				expansion_info.append(set_name)  # Full Edition name
				formatted_date = datetime.strptime(set_release_date, '%d.%m.%Y').strftime('%Y-%m')
				expansion_info.append(formatted_date)  # Release date
				dst_expansion_path = "static/expansion-symbols/"+set_shortcut+"-"+label_rarity+".png"
				expansion_info.append(dst_expansion_path)  # Release date

				print(f"expansion_info: {expansion_info}")

				if not exists(dst_expansion_path):
					make_symbol_png(set_shortcut, label_rarity, 128, dst_expansion_path)

					if os.stat(dst_expansion_path).st_size == 0:
						print(f"Error: Set symbol {set_shortcut} could not be fetched from the source page.")

						# Remove zero-size image
						os.remove(dst_expansion_path)

				set_info_list.append(expansion_info)

	# Selecting correct html template and css stylesheet files
	label_type_name = "small-labels-default"
	html_label_template = label_type_name+"-template.html"
	css_label_style = "static/"+label_type_name+".css"

	if label_type == "small_labels_default":
		label_type_name = "small-labels-default"

	elif label_type == "small_labels_no_date":
		label_type_name = "small-labels-no-date"

	elif label_type == "large_labels_basic":
		label_type_name = "large-labels-basic"

	elif label_type == "large_labels_basic_switched":
		label_type_name = "large-labels-basic-switched"

	elif label_type == "narrow_labels_template":
		label_type_name = "narrow-labels-template"
		# LABEL_TYPE_COMMENT_TO_MATCH_FOR_SCRIPT

	# Select correct html template and css style file
	html_label_template = label_type_name+"-template.html"
	css_label_style = "static/"+label_type_name+".css"

	return render_template(html_label_template, \
						info_about_selected_labels=set_info_list, \
						label_type=label_type, \
						label_background_colors=label_background_colors, \
						label_css_style=css_label_style \
						)


if __name__ == "__main__":
	# TODO In production edit these:
	# app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)
