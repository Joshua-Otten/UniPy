# Translates code from one language to another
#
#   1st arg - code file to translate;
#   2nd - Python key list of original language;
#   3rd - key list of target language;
#   4th - the new file extension
#
# NOTE: The language argument for a lang1 must correspond to a .txt file with
#   the same name as 'lang1Key.txt'.  Otherwise the program will not be able
#   to find the right key mapping.
#

import sys

Lang1_list = list()
Lang2_list = list()


Lang1_file = open(sys.argv[2]+'Key.txt','r')
# reading data for first language
line = Lang1_file.readline()
while line != "":
    Lang1_list.append(line.split()[0].strip()) # append without extra '\n'
    line = Lang1_file.readline()
Lang1_file.close()


Lang2_file = open(sys.argv[3]+'Key.txt','r')
# reading data for second language
line = Lang2_file.readline()
while line != "":
    Lang2_list.append(line.split()[0].strip()) # append without extra '\n'
    line = Lang2_file.readline()
Lang2_file.close()



# create new py file as the result:

# get rid of .xxpy
new_py_name = ""
for i in str(sys.argv[1]):
    if i == '.':
        break
    else:
        new_py_name += i
        
new_py_name = new_py_name + str(sys.argv[4])
new_py = open(new_py_name, 'w')
#new_py = open("test_translation.py","w")

original = open(sys.argv[1],'r')
# now go through the original py file and translate to the new
line = original.readline()
delimeter_quotes = (False,'')
fstring = False
fstring_braces = False
while line != "":
    comment = False
    i = 0
    while i < len(line): # throughout the entire line
        # finding the words
        word = ""
        # all entries in foreign dict either '_' or alphabetic characters
        #   (foregin font scripts or otherwise)
        word_flag = False
        while (line[i].isalpha()) or (line[i] == '_'):
            #print("'"+line[i]+"'")
            word_flag = True
            word += line[i]
            i += 1
        #print(word)
        if word_flag == True:
            #print('word_flag is true')
            # if there is a word, must have encountered a non-alpha or '_',
            #   so it's complete
            # search for the word in the foregin dictionary
            replace_flag = False
            if delimeter_quotes[0] == False and (not comment) or (delimeter_quotes[0] and fstring_braces and not comment):
                for j in range(0, len(Lang1_list)-1):
                    #print('compare to:',Lang1_list[j])
                    if Lang1_list[j] == word:
                        # set replace flag to True and break
                        # write the English version of the word in the new Py file
                        replace_flag = True
                        #print('found a match in the foreign list')
                        new_py.write(Lang2_list[j])
                        break
            
            if replace_flag == False:
                # there was no foreign word to replace,
                #   so just copy to the new Py file
                new_py.write(word)

        # now write the other separators/operators/etc.
        # if a separator is first in the line, the prior part of loop is skipped
        while (i < len(line) and (not line[i].isalpha()) and line[i] != '_'):
            # for not translating comments, things in quotes, etc.
            if line[i] == "#":
                comment = True
            if not comment and (line[i] == "'" or line[i] == '"'):
                if delimeter_quotes == (True,line[i]):
                    delimeter_quotes = (False,'')
                    fstring = False
                    #print('SO IT DETECTED... on line',line)
                    #print('delimiter quotes now is',False)
                elif delimeter_quotes[0] == False:
                    delimeter_quotes = (True,line[i])
                    if i > 0 and line[i-1]=="f":
                        # this is an f-string
                        fstring = True
                    #print('SO IT DETECTED... on line',line)
                    #print('delimiter quotes now is',delimeter_quotes)
            if not comment and line[i]=='{' and fstring:
                fstring_braces = True
            elif not comment and line[i]=='}' and fstring:
                fstring_braces = False
            new_py.write(line[i])
            i += 1

    line = original.readline()
    
original.close()
new_py.close()

# ADDED STUFF FOR THE WEB DEMO
# STUFF BEFORE IS JUST THE CodeTranslator.py FILE
new_py = open(new_py_name, 'r')
line = new_py.readline()
to_return = line
while line != '':
    line = new_py.readline()
    to_return += line
print(to_return)

new_py.close()
