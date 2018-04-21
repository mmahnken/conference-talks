import sys
sys.path.append("..")

from masterconf import *

project = 'Talks By Meggie'

latex_documents = [
   ('index', 'Lecture.tex', '', '', 'howto', False)
]

latex_elements['pointsize'] = '10pt'
