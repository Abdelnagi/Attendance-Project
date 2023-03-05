[app]
# (str) Title of your application
title = My App

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mycompany.myapp

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivy = ../../kivy
#requirements.source.mydep = ../../mydep

# (list) Garden requirements
#garden_requirements = 

# (str)
