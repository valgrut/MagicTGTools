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

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/')
def home():
    csv_file = csv.reader(open('classes-frames.md', "r"), delimiter=";")
    available_classes = []
    for row in csv_file:
        available_classes += row
    print(available_classes)

    return render_template('index.html', AVAILABLE_CLASSES=available_classes)


@app.route('/generated-labels', methods = ['GET', 'POST'])
def generate_labels():
    if request.method == 'POST':
        requested_hero_classes = []
        selected_hero_classes = request.form.getlist('hero_classes')
        for selected_class in selected_hero_classes:
            requested_hero_classes.append(selected_class)
        
        print(requested_hero_classes)
        
        label_type = request.form['label_type']
        symbol_size = "large"  #large, medium, small

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
                requested_hero_classes=requested_hero_classes, \
                label_type=label_type, \
                label_css_style=css_label_style \
                )


if __name__ == "__main__":
    # TODO In production edit these:
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
