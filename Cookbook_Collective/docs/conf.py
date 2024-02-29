import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../recipe_project'))
sys.path.insert(0, os.path.abspath('../recipes'))
sys.path.insert(0, os.path.abspath('../users'))
sys.path.insert(0, os.path.abspath('../ingredients'))

# Add your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'The Cookbook Collective'
copyright = '2024, Jon Cody'
author = 'Jon Cody'

autodoc_mock_imports = [
    'django',
    'django.contrib.auth',
    'django.db',
    'django.apps',
    'django.conf',
    'django.core',
    'django.urls',
    'django.forms',
    'django.views',
    'recipes.models',
    'recipe_ingredients.models',
    'recipe_project.views',
    'recipe_project.forms',
]





# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or .htaccess) here, relative to this directory.
html_extra_path = ['_extra']
