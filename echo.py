import glob
import os
import csv
import collections

# script to label occurances of echoes/whispers "((()))" 
# so they can be analyzed as a lexical item by programs like Antconc
os.chdir('/path/to/files')
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
      try:
            file = str(files[0])
            f = open(file, 'r', errors='ignore')
            search_text = "((("
            # this is the tag you can use to search for echoes
            replace_text = "ECHOES_((("
            data = f.read()
            data = data.replace(search_text, replace_text)
            
            f = open(file, 'w')
            f.write(data)
            print("text replaced")
            f.close()

            files.popleft()
      except FileNotFoundError:
            print("OPERATION COMPLETED")
            break
