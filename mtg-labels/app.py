from flask import Flask, redirect, url_for, render_template, request, session, flash, escape
from os.path import exists
import wget
import csv
import sys
import ssl
import urllib
import urllib.request
import datetime
import os

# https://aetherhub.com/Card/Set
# https://mythicspoiler.com/sets.html   !!!!
# https://gatherer.wizards.com/Handlers/Image.ashx?type=symbol&set=DTK&size=large&rarity=U

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/')
def home():
    # fetch first 6 sets shortcuts from csv file
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


@app.route('/generated-labels', methods = ['GET', 'POST'])
def generate_labels():
    if request.method == 'POST':
        list_of_expansions = request.form['expansions_list']
        label_type = request.form['label_type']
        selected_label_rarities = request.form.getlist('label_rarity')
        label_background_colors = request.form.getlist('label_background_color')
        symbol_size = "large"  #large, medium, small

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
                    if expansion == row[0]:
                        set_shortcut = row[0]
                        expansion_info.append(row[0])  # Shortcut
                        expansion_info.append(row[1])  # Full Edition name
                        formatted_date = datetime.datetime.strptime(row[2], '%d.%m.%Y').strftime('%Y-%m')
                        expansion_info.append(formatted_date)  # Release date
                        expansion_info.append("static/expansion-symbols/"+row[0]+"-"+label_rarity+".png")  # Release date
                        if not exists("static/expansion-symbols/"+set_shortcut+"-"+label_rarity+".png"):
                            src_expansion_link = "https://gatherer.wizards.com/Handlers/Image.ashx?type=symbol&set="+set_shortcut+"&size="+symbol_size+"&rarity="+label_rarity
                            dst_expansion_path = "static/expansion-symbols/"+set_shortcut+"-"+label_rarity+".png"
                            response = wget.download(src_expansion_link, dst_expansion_path)

                            if os.stat(dst_expansion_path).st_size == 0:
                                print(f"Error: Set symbol image for {set_shortcut} does not exist on source page.")
                                # Remove zero-size image
                                os.remove(dst_expansion_path)
                                
                                # TODO: Try to fetch image from other source?

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
