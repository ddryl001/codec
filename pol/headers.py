import glob
import os
import csv
import collections

os.chdir(r'directory_containing_files')
my_files = glob.glob('*.txt')
print(my_files)

dir_file = open("dir.txt", "w")
writer = csv.writer(dir_file, delimiter='\n')
writer.writerow(my_files)
dir_file.close()

my_file = open("dir.txt", "r")
data = my_file.read()
data_into_list = data.split("\n")
files = collections.deque(data_into_list)
my_file.close()

while True:
      file = str(files[0])
      try:
            f = open(file, 'r')
            first_line = f.readline()
            print(first_line)

            f = open(file, 'r')
            subject = first_line
            search_text = subject
            replace_text = "<h> TEXT </h>" + "\t" + "<h> ID </h>" + "\t" + "<h> USERNAME </h>" + "\t" + "<h> TIME </h>" + "\t" + "<h> POSTNUM </h>" + "\t" + "<h> THREAD </h>" + "\t" + "<h> REPLY </h>" + "\t" + "<h> FLAG </h>" + "\t" + "<h> SUBJECT </h>" + "\n"
            data = f.read()
            data = data.replace(search_text, replace_text)
      
            f = open(file, 'w')
            f.write(data)
            print("subject replaced")

            search_text = "</m>\n"
            replace_text = str("</m>" + "\t" + "<m> NO FLAG </m>" + "\t" + subject + "\n")

            f = open(file, 'r')
            data = f.read()
            data = data.replace(search_text, replace_text)

            f = open(file, 'w')
            f.write(data)
            print("Text replaced")
            f.close()

            files.popleft()
            
      except FileNotFoundError:
            print("Complete")
            break
