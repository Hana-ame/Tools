import os
import sys
import re

# Get the path of the current directory
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

def get_module_name():
  module_file = os.path.join(os.path.dirname(TOOLS_DIR), "go.mod")

  with open(module_file, 'r') as f:
    first_line = f.readline()
    module_name = first_line.split(' ')[-1]
    return module_name.strip()

def replace_go_file(file_path, module_name):
  print("!",file_path, module_name)
  file = ''
  with open(file_path, encoding='utf8') as f:
    file = f.read()
  file = re.sub(r'"(.*?)/Tools/(.*?)"', fr'"{module_name}/Tools/\2"', file)
  with open(file_path, 'w') as f:
    f.write(file)

def replace_go_files(module_name):
  for root, _, files in os.walk(TOOLS_DIR):
    for file in files:
      if file.endswith(".go"):
        print(os.path.join(root, file))
        replace_go_file(os.path.join(root, file), module_name)

module_name = get_module_name()

print(module_name)

replace_go_files(module_name)