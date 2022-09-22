#! /usr/bin/env bash

NAME_OF_LABEL="$1"

if [[ $NAME_OF_LABEL == "" ]]; then
    echo "You have to provide name of new label, i.e. 'my-new-shiny-label'"
    exit 1
fi

if [[ -f "templates/$NAME_OF_LABEL-template.html" ]]; then
    echo "Label with this name already exists."
    exit 1
fi

cp templates/small-labels-default-template.html templates/$NAME_OF_LABEL-template.html
cp static/small-labels-default.css static/$NAME_OF_LABEL.css

sed -i '/LABEL_TYPE_COMMENT_TO_MATCH_FOR_SCRIPT/i \ \ \ \ \ \ \ \ <option value="'$(echo $NAME_OF_LABEL | tr "-" "_")'">'"$NAME_OF_LABEL"'</option>' templates/index.html

sed -i '/LABEL_TYPE_COMMENT_TO_MATCH_FOR_SCRIPT/i \\n\ \ \ \ \ \ \ \ elif label_type == "'$(echo $NAME_OF_LABEL | tr "-" "_")'":\n\ \ \ \ \ \ \ \ \ \ \ \ label_type_name = "'"$NAME_OF_LABEL"'"' app.py


exit 0
