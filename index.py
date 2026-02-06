import os
import sys

PATH = sys.argv[1]

def generate_index_html(directory):
    files = os.listdir(directory)
    files.sort()  # Sort the list of files alphabetically

    html = "<html>\n<body>\n<ul>\n"
    for file in files:
        if file != "index.html":
            html += f"<li><a href='{file}'>{file}</a></li>\n"
    html += "</ul>\n</body>\n</html>"

    with open(os.path.join(directory, "index.html"), "w") as f:
        f.write(html)

# Specify the directory for which you want to generate the index.html file
directory_path = PATH # "/path/to/your/directory"
generate_index_html(directory_path)
