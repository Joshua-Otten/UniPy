# This code translates and executes a French Python script
# The command-line argument must be the French Python script file

import subprocess
import sys
from googletrans import Translator

file_to_translate = str(sys.argv[1])
rest_of_arguments = sys.argv[2:]
# check to make sure this is really a French Python file
if file_to_translate[len(file_to_translate)-5:] != '.frpy':
    print("Attendu l'extension de fichier '.frpy'")
    raise RuntimeError

# these two lists will hold the key mapping
English_list = list()
French_list = list()

# Get English keyword mapping into a list
English_file = open("EnglishKey.txt","r")
# scan English file into list
line = English_file.readline()
while line != "":
    English_list.append(line.strip()) # append without extra '\n'
    line = English_file.readline()
English_file.close()

# Get foreign keyword mapping
French_file = open("FrenchKey.txt","r")
# scan French file into list
line = French_file.readline()
while line != "":
    French_list.append(line.strip()) # append without extra '\n'
    line = French_file.readline()
French_file.close()

foreign_code = open(file_to_translate,'r')
temp = open(file_to_translate[:len(file_to_translate)-5]+".py","w")

line = foreign_code.readline()
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
                #print('down to replace for',line)
                for j in range(0, len(French_list)-1):
                    #print('compare to:',French_list[j])
                    if French_list[j] == word:
                        # set replace flag to True and break
                        # write the English version of the word in the new Py file
                        replace_flag = True
                        #print('found a match in the foreign list')
                        temp.write(English_list[j])
                        break
            
            if replace_flag == False:
                # there was no foreign word to replace,
                #   so just copy to the new Py file
                temp.write(word)

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
            temp.write(line[i])
            i += 1

    line = foreign_code.readline()
foreign_code.close()
temp.close()



# Now we have a temp.py executable file!
# So first, run it.  Then we'll grab the output and print it out in this program
run = subprocess.run(["python",file_to_translate[:len(file_to_translate)-5]+".py"]+rest_of_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# not currently supporting extra command-line arguments...

output = run.stdout.decode()
errormsg = run.stderr.decode()



#############
#Convert output back now
#############

output_list = output.split("\n")
list_index = 0
line = output_list[list_index] + "\n"
French_output = ""
delimeter_quotes = (False,'')
while list_index < len(output_list)-1:
    i = 0
    comment = False
    while i < len(line): # throughout the entire line
        # finding the words
        word = ""
        # all entries in foreign dict either '_' or alphabetic characters
        #   (foregin font scripts or otherwise)
        word_flag = False
        while (i<len(line) and (line[i].isalpha()) or (line[i] == '_')):
            #print("'"+line[i]+"'")
            #print(French_output)
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
            if delimeter_quotes == False and not comment:
                for j in range(0, len(English_list)-1):
                    #print('compare to:',French_list[j])
                    if English_list[j] == word:
                        # set replace flag to True and break
                        # write the English version of the word in the new Py file
                        replace_flag = True
                        #print('found a match in the foreign list')
                        French_output += str(French_list[j])
                        break
            
            if replace_flag == False:
                # there was no foreign word to replace,
                #   so just copy to the new Py file
                French_output += word

        # now write the other separators/operators/etc.
        # if a separator is first in the line, the prior part of loop is skipped
        while (i < len(line) and (not line[i].isalpha()) and line[i] != '_'):
            # for not translating things in quotes
            if line[i] == "#":
                comment = True
            if not comment and (line[i] == "'" or line[i] == '"'):
                #print('SO IT DETECTED... on line',line)
                if delimeter_quotes == (True,line[i]):
                    delimeter_quotes = (False,'')
                elif delimeter_quotes[0] == False:
                    delimeter_quotes = (True,line[i])
            French_output += line[i]
            i += 1
    
    list_index += 1
    if list_index == len(output_list)-1:
        line = output_list[list_index]
    else:
        line = output_list[list_index] + "\n"

print(French_output.strip())


################
# Now the same for error messages!
################

# Setting up the English and French Error messages translation lists
French_Error_Translation_List = list()
FrErrors = open('FrenchErrorList.txt','r')
line = FrErrors.readline()
#French_Error_Translation_List = line.split(',')
while line !='':
    French_Error_Translation_List.append(line.strip())
    line = FrErrors.readline()

English_Error_Translation_List = list()
EnErrors = open('EnglishErrorList.txt','r')
line = EnErrors.readline()
#English_Error_Translation_List = line.split(',')
while line != '':
    English_Error_Translation_List.append(line.strip())
    line = EnErrors.readline()


error_list = errormsg.split("\n")

# so we don't do any potentially extra work...
if error_list == ['']:
    sys.exit()

 
# first try to translate any of the more complete 'error messages', then look for any of the keywords
err_line = error_list[len(error_list)-2] # -2 here because there is an extra element '' at the end for some reason
found = False
if err_line in English_Error_Translation_List:
    found = True
    err_line = French_Error_Translation_List[English_Error_Translation_List.index(err_line)]
    error_list[len(error_list)-2] = err_line
'''
# this is for trying to translate substrings in a given line, but it may not be appropriate
index = 0
found = False
for item in error_list:
    for i in range(len(item)):
        str_to_translate = ''
        # looking at any substring of the line / moving window
        for j in range(i,len(item)):
            str_to_translate += item[j]
            if str_to_translate in English_Error_Translation_List:
                found = True
                # replace that substring with the translated version
                new_str = French_Error_Translation_List[English_Error_Translation_List.index(str_to_translate)]
                #print('OLD STRING: "'+str_to_translate+'"')
                #print('NEW STRING: "'+new_str+'"')
                error_list[index] = item[:i]+new_str+item[j:]
            # shouldn't need to worry about the carrot, since this shouldn't be the line in question
    index += 1
'''


# now, if the error wasn't found in the English list, we need to translate it on the fly and add it to the list
if not found:
    translator = Translator()
    # line to translate *should* be the last one of the error message
    err_line = error_list[len(error_list)-2].strip()
    translation = (translator.translate(err_line, dest='fr')) # will need to generalize!
    error_list[len(error_list)-2] = str(translation.text)
    
    # now write the new error message in each file
    e = open('EnglishErrorList.txt','r+')
    f = open('FrenchErrorList.txt','r+')
    
    # read through both to get to the end
    line = e.readline()
    while line != '':
        line = e.readline()
        f.readline()
    e.write(err_line+'\n')
    f.write(str(translation.text)+'\n')


#print(error_list)


EnErrors.close()
FrErrors.close()

# simply translating based on keywords

# find num of spaces before '^' on its line
num_init_spaces = None
for j in error_list:
    if '^' in j.split():
        num_init_spaces = len(j)-2 # the -2 is to account for '\n' and '^'

French_output = ''
word_flag = False
string = (False,'')
fstr = False
fstr_braces = False
nextLineHasCarrot = False
ln_num = 0
for line in error_list:
    if nextLineHasCarrot == True: # this line must have the carrot!
        French_output += (' '*(num_init_spaces+1)) + '^\n'
        nextLineHasCarrot = False
    else:
        if ln_num < len(error_list)-1 and '^' in error_list[ln_num+1]:
            # next line has the carrot
            nextLineHasCarrot = True
        word = ''
        comment = False
        index = 0
        for i in line:
            if i.isalpha() or i=='_':
                # if this isn't a comment, and we're either not in a string or we are within fstring braces, then translate
                if not comment and ((not string[0]) or fstr_braces):
                    word_flag = True
                    # building word to translate
                    word += i
            else: # i must not be alphabetic, and the 'word' is complete
                if word_flag == True:
                    if word in English_list:
                        # this word needs to be translated
                        French_output += French_list[English_list.index(word)]
                        
                        if nextLineHasCarrot and index < num_init_spaces:
                            num_init_spaces += (len(French_list[English_list.index(word)]) - len(word))
                            
                    else:
                        French_output += word
                    word_flag = False
                    word = ''
            if i == '#':
                comment = True
            # for string / delimiter stuff
            elif i=='"' or i=="'":
                if string == (True, i):
                    string = (False,'')
                    fstr = False
                elif string == (False,''):
                    string = (True,i)
                    # for fstring stuff
                    if index>0 and line[index-1]=='f':
                        fstr = True
            # fstr braces
            elif fstr and i=='{':
                fstr_braces = True
                #print('fstr_braces=true on line',line)
            elif fstr and i=='}':
                fstr_braces = False
                #print('fstr_braces=false on line',line)
            
            if word_flag == False:
                French_output += i
            
            index += 1
            
            if index == len(line) and word_flag==True:
                French_output += word
                word_flag = False
        #if index < len(error_list)-1:
        French_output += '\n'
        ln_num += 1



if (French_output != ""):
    print(French_output.strip())

if not found:
    # if we had to translate the error on the fly, just give a note to the user
    print('(Error message generated)')
