#!/usr/bin/env python
# Created by Simon Goldin on github.com/goldins/image-replace-64


import base64
import sys, getopt
import re, os
import imghdr

old_dir = os.path.abspath(os.curdir)
print 'pwd: ' + old_dir

def main(argv):
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv,'hf:',['file='])
  except getopt.GetoptError:
    print 'encode64.py -f <file>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'encode64.py -f <file>'
      sys.exit()
    elif opt in ('-f', '--file'):
      inputfile = arg

  file_dir = os.path.dirname(os.path.abspath(inputfile))

  os.chdir(file_dir)
  print 'In dir ' + os.path.abspath(os.curdir)

  #print 'Input file is', inputfile
  input_file_name = os.path.basename(inputfile)
  print 'reading ' + input_file_name

  f = open(input_file_name,'r')
  filedata = f.read()
  f.close()

  p = re.compile('src="([^"]+)"')
  matches = p.findall(filedata)

  for img_src in matches:
    if not os.path.isfile(img_src):
      print 'ERROR: "' + img_src + '" not found. Continuing to next file if exists'
      continue
    with open(img_src, "r+") as image_file:
      ext = imghdr.what(image_file)
      encoded_string = base64.b64encode(image_file.read())

      print 'Changing src "' + img_src + '" to ' + encoded_string[0:15] + '...'
      new_src = 'data:image/' + ext + ';base64,' + encoded_string
      newdata = filedata.replace(img_src, new_src)

      f = open('output.html','w')
      f.write(newdata)
      f.close()

  os.chdir(old_dir)

if __name__ == "__main__":
  main(sys.argv[1:])


