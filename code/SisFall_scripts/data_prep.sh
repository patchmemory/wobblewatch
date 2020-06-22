17:33:51 apatch@gollum: $ cat Readme.txt | grep '|' | grep -A100 'Subject' > Subjects.txt 
17:34:03 apatch@gollum: $ cat Readme.txt | grep '|' | grep -B100 'Subject' > Activities.txt 
