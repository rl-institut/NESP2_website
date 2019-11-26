import os
from shutil import copyfile, rmtree

# clone the NESP2 repository locally
branch = 'dev'
if os.path.exists('NESP2') is False:
    os.system(
        f"git clone --single-branch --branch {branch} https://github.com/rl-institut/NESP2.git")

# copy templates
template_path = os.path.join('NESP2', 'app', 'templates')

new_template_path = os.path.join('templates', 'maps')

if os.path.exists(new_template_path) is False:
    os.mkdir(new_template_path)

for fname in os.listdir(template_path):
    copyfile(os.path.join(template_path, fname), os.path.join(new_template_path, fname))

# copy static files
static_path = os.path.join('NESP2', 'app', 'static')

new_static_path = os.path.join('static')

static_types = ['data', 'images', 'css']
new_static_types = {'data': 'data', 'images': os.path.join('img', 'maps'), 'css': 'css'}

for static_type in static_types:
    new_static_type = new_static_types[static_type]

    # create the folder if it does not exists
    if os.path.exists(os.path.join(new_static_path, new_static_type)) is False:
        os.mkdir(os.path.join(new_static_path, new_static_type))

    # copy the files from NESP2 repo the folder of NESP2 template
    for fname in os.listdir(os.path.join(static_path, static_type)):
        copyfile(
            os.path.join(static_path, static_type, fname),
            os.path.join(new_static_path, new_static_type, fname)
        )


# erase the NESP2 repository
rmtree('NESP2')
