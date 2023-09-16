# This code translates and executes a Foreign Python script
# First command-line argument is the language the .unipy file is in
# Second arg must be the Uni-Python script file


import subprocess
import sys
import string
from googletrans import Translator



#################
# For RTL languages

def swapLineOrder(line):
    # goes through line similarly to main program, but just swaps order
    tokens = list()
    del_quotes = False
    i = 0
    while i < len(line):
        # finding the words
        word = ""
        word_flag = False
        while i<len(line) and line[i] not in non_alpha:#((line[i].isalpha()) or (line[i] == '_')):
            word_flag = True
            word += line[i]
            i += 1
        # word must be found, so add it
        if word != '':
            if del_quotes:
                #tokens.append(word)
                tokens.insert(str_start_point, word)
                str_start_point += 1
            else:
                tokens.insert(0,word)
            
        # now write the other separators/operators/etc.
        while (i < len(line) and line[i] in non_alpha):#(not line[i].isalpha()) and line[i] != '_'):
            # for not reordering comments, things in quotes, etc.
            if line[i] == "#":
                # no need to reorder anything after this
                # reorder, clean up, and return
                tokens.reverse()
                delimiterSwap(tokens)
                return "".join(tokens.append(line[i:]))
                
            elif (line[i] == "'" or line[i] == '"'):
                if del_quotes == True:
                    del_quotes = False
                    tokens.insert(str_start_point, line[i])
                elif del_quotes == False:
                    del_quotes = True
                    tokens.insert(0, line[i])
                    str_start_point = 1
            # time to add the item to the token list
            elif del_quotes == False:
                # swapping delimiters if necessary
                if line[i] == ')':#'\u202C)\u202C':
                    tokens.insert(0,'(')#'\u202C(\u202C'
                elif line[i] == '(':#'\u202C(\u202C':
                    tokens.insert(0,')')#'\u202C)\u202C'
                elif line[i] == '[':#'\u202C[\u202C':
                    tokens.insert(0,']')#'\u202C]\u202C'
                elif line[i] == ']':#'\u202C]\u202C':
                    tokens.insert(0,'[')#'\u202C[\u202C'
                elif line[i] == '{':#'\u202C{\u202C':
                    tokens.insert(0,'}')#'\u202C}\u202C'
                elif line[i] == '}':#'\u202C}\u202C':
                    tokens.insert(0,'{')#'\u202C{\u202C'
                elif line[i] == '<':#'\u202C<\u202C':
                    tokens.insert(0,'>')#'\u202C>\u202C'
                elif line[i] == '>':#'\u202C>\u202C':
                    tokens.insert(0,'<')#'\u202C<\u202C'
                else:
                    tokens.insert(0,line[i])
            else:
                #tokens.append(line[i])
                tokens.insert(str_start_point, line[i])
                str_start_point += 1
            i += 1
    # join the resulting tokens list, return the string
    result = ''.join(tokens)
    #print('result after swapping:',result)
    return result

#################



# determining whether term order needs to be switched (support for right-left languages)
RTL = ['Kurdish'] # UPDATE THIS AND StringCodeTranslator.py AS LANGUAGE LIST GROWS!!!
lang1 = sys.argv[1]
lang2 = 'English'
orderSwap = False
if (lang1 not in RTL and lang2 in RTL) or (lang1 in RTL and lang2 not in RTL):
    orderSwap = True

# set of non-alphanumeric characters used in Python
non_alpha = {' ','\t','\n'}
non_alpha = non_alpha.union(string.punctuation)
non_alpha.remove('_')

language = sys.argv[1]
file_to_translate = str(sys.argv[2])
rest_of_arguments = sys.argv[3:]
# check to make sure this is really a Uni-Python file
if file_to_translate[len(file_to_translate)-6:] != '.unipy':
    raise RuntimeError("expected file extension '.unipy'")

# these two lists will hold the key mapping
English_list = list()
Foreign_list = list()

# Get English keyword mapping into a list
English_file = open("LanguageData/EnglishKey.txt","r")
# scan English file into list
#English_list = English_file.readlines()
#print(English_list)
line = English_file.readline()
while line != "":
    English_list.append(line.strip()) # append without extra '\n'
    line = English_file.readline()
English_file.close()

# Get foreign keyword mapping
Foreign_file = open("LanguageData/"+language+"Key.txt","r")
# scan Foreign file into list
line = Foreign_file.readline()
while line != "":
    Foreign_list.append(line.strip()) # append without extra '\n'
    line = Foreign_file.readline()
Foreign_file.close()

foreign_code = open(file_to_translate,'r')
temp = open(file_to_translate[:len(file_to_translate)-6]+".py","w")


line = foreign_code.readline()
delimeter_quotes = (False,'')
fstring = False
fstring_braces = False
while line != "":

    tokenList = list()
    tokenIndex = list()
    
    ### if changing word order, must swap first to avoid complications with key orderings
    if orderSwap == True:
        line = swapLineOrder(line)

    comment = False
    i = 0
    while i < len(line): # throughout the entire line
        # finding the words
        word = ""
        # all entries in foreign dict either '_' or alphabetic characters
        #   (foregin font scripts or otherwise)
        word_flag = False
        while i<len(line) and line[i] not in non_alpha:#(line[i] == '_' or line[i] not in non_alpha):  #((line[i].isalpha()) or (line[i] == '_')):
            #print("'"+line[i]+"'")
            word_flag = True
            if line[i] != '\u202A' and line[i] != '\u202C':
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
                for j in range(0, len(Foreign_list)-1):
                    #print('compare to:',Foreign_list[j])
                    if Foreign_list[j] == word:
                        # set replace flag to True and break
                        # write the English version of the word in the new Py file
                        replace_flag = True
                        #print('found a match in the foreign list')
                        #temp.write(English_list[j])
                        # Instead of translating now, save the (index,translation) and wait until later
                        tokenList.append(word)
                        tokenIndex.append(len(tokenList)-1)
                        break
            
            if replace_flag == False:
                # there was no foreign word to replace,
                #   so just copy to the new Py file
                #temp.write(word)
                tokenList.append(word)

        # now write the other separators/operators/etc.
        # if a separator is first in the line, the prior part of loop is skipped
        while (i < len(line) and line[i] in non_alpha):#(not line[i].isalpha()) and line[i] != '_'):
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
            if line[i] != '\u202A' and line[i] != '\u202C':
                #temp.write(line[i])
                tokenList.append(line[i])
            i += 1
            
            
    for index in tokenIndex:
        word = tokenList[index]
        #print(word)
        for j in range(0, len(Foreign_list)-1):
            if Foreign_list[j] == word:
                #print('found a word:',word)
                replacement = English_list[j]
                tokenList[index] = replacement
                #tokenList.pop(index)
                #tokenList.insert(index, replacement)
                break
    
    #print(tokenList)
    if tokenList[0]=='\n':
        tokenList.pop(0)
        to_write = ''.join(tokenList) + '\n'
    else:
        to_write = ''.join(tokenList)
    #print('to write:',to_write)
    temp.write(to_write)

    line = foreign_code.readline()
foreign_code.close()
temp.close()



# Now we have a temp.py executable file!
# So first, run it.  Then we'll grab the output and print it out in this program
run = subprocess.run(["python",file_to_translate[:len(file_to_translate)-6]+".py"]+rest_of_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# not currently supporting extra command-line arguments...

output = run.stdout.decode()
errormsg = run.stderr.decode()



#############
#Convert output back now
#############

output_list = output.split("\n")
list_index = 0
line = output_list[list_index] + "\n"
Foreign_output = ""
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
        while (i<len(line) and line[i] not in non_alpha):#(line[i].isalpha()) or (line[i] == '_')):
            #print("'"+line[i]+"'")
            #print(Foreign_output)
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
                    #print('compare to:',Foreign_list[j])
                    if English_list[j] == word:
                        # set replace flag to True and break
                        # write the English version of the word in the new Py file
                        replace_flag = True
                        #print('found a match in the foreign list')
                        Foreign_output += str(Foreign_list[j])
                        break
            
            if replace_flag == False:
                # there was no foreign word to replace,
                #   so just copy to the new Py file
                Foreign_output += word

        # now write the other separators/operators/etc.
        # if a separator is first in the line, the prior part of loop is skipped
        while (i < len(line) and line[i] in non_alpha):#(not line[i].isalpha()) and line[i] != '_'):
            # for not translating things in quotes
            if line[i] == "#":
                comment = True
            if not comment and (line[i] == "'" or line[i] == '"'):
                #print('SO IT DETECTED... on line',line)
                if delimeter_quotes == (True,line[i]):
                    delimeter_quotes = (False,'')
                elif delimeter_quotes[0] == False:
                    delimeter_quotes = (True,line[i])
            Foreign_output += line[i]
            i += 1
    
    list_index += 1
    if list_index == len(output_list)-1:
        line = output_list[list_index]
    else:
        line = output_list[list_index] + "\n"

print(Foreign_output.strip())


################
# Now the same for error messages!
################

# Setting up the English and Foreign Error messages translation lists
Foreign_Error_Translation_List = list()
UniErrors = open('LanguageData/'+language+'ErrorList.txt','r')
line = UniErrors.readline()
#Foreign_Error_Translation_List = line.split(',')
while line !='':
    Foreign_Error_Translation_List.append(line.strip())
    line = UniErrors.readline()

English_Error_Translation_List = list()
EnErrors = open('LanguageData/EnglishErrorList.txt','r')
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
    err_line = Foreign_Error_Translation_List[English_Error_Translation_List.index(err_line)]
    error_list[len(error_list)-2] = err_line

# now, if the error wasn't found in the English list, we need to translate it on the fly and add it to the list
if not found:
    translator = Translator()
    # line to translate *should* be the last one of the error message
    err_line = error_list[len(error_list)-2].strip()
    
    abbrev_file = open('LanguageData/languageAbbrevs.txt','r')
    line = abbrev_file.readline()
    while line!='' and line.split(',')[0]!=language:
        line = abbrev_file.readline()
    if line.split(',')[0]!=language:
        raise RuntimeError('Language Abbreviation for error translation not found')
    abbrev_file.close()
    abbrev = line.split(',')[1].strip()
    translation = (translator.translate(err_line, dest=abbrev))
    error_list[len(error_list)-2] = str(translation.text)
    
    # now write the new error message in each file
    e = open('LanguageData/EnglishErrorList.txt','a')
    f = open('LanguageData/'+language+'ErrorList.txt','a')
    '''
    # read through both to get to the end
    line = e.readline()
    while line != '':
        line = e.readline()
        f.readline()
    '''
    e.write(err_line+'\n')
    f.write(str(translation.text)+'\n')

    # Translating the error in all other language files to keep it consistent
    # NOTE: this may result in some runtime lag, especially once we support many languages :|
    abbrev_file = open('LanguageData/languageAbbrevs.txt','r')
    line = abbrev_file.readline()
    while line != '':
        cur_lang = line.split(',')[0]
        cur_abbrev = line.split(',')[1].strip()
        # so that we don't write/translate something twice
        if cur_abbrev != abbrev and cur_abbrev != 'en':
            cur_file = open('LanguageData/'+cur_lang+'ErrorList.txt','a')
            '''
            # read through to get to the end
            cur_file.readlines()
            '''
            translation = (translator.translate(err_line, dest=cur_abbrev))
            cur_file.write(str(translation.text)+'\n')
            cur_file.close()
        line = abbrev_file.readline()
        

#print(error_list)
UniErrors.close()

EnErrors.close()

# simply translating based on keywords

# find num of spaces before '^' on its line
num_init_spaces = None
for j in error_list:
    if '^' in j.split():
        num_init_spaces = len(j)-2 # the -2 is to account for '\n' and '^'

Foreign_output = ''
word_flag = False
string = (False,'')
fstr = False
fstr_braces = False
nextLineHasCarrot = False
ln_num = 0
for line in error_list:
    if nextLineHasCarrot == True: # this line must have the carrot!
        Foreign_output += (' '*(num_init_spaces+1)) + '^\n'
        nextLineHasCarrot = False
    else:
        if ln_num < len(error_list)-1 and '^' in error_list[ln_num+1]:
            # next line has the carrot
            nextLineHasCarrot = True
        word = ''
        comment = False
        index = 0
        for i in line:
            if i not in non_alpha:#i.isalpha() or i=='_':
                # if this isn't a comment, and we're either not in a string or we are within fstring braces, then translate
                if not comment and ((not string[0]) or fstr_braces):
                    word_flag = True
                    # building word to translate
                    word += i
            else: # i must not be alphabetic, and the 'word' is complete
                if word_flag == True:
                    if word in English_list:
                        # this word needs to be translated
                        Foreign_output += Foreign_list[English_list.index(word)]
                        
                        if nextLineHasCarrot and index < num_init_spaces:
                            num_init_spaces += (len(Foreign_list[English_list.index(word)]) - len(word))
                            
                    else:
                        Foreign_output += word
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
                Foreign_output += i
            
            index += 1
            
            if index == len(line) and word_flag==True:
                Foreign_output += word
                word_flag = False
        #if index < len(error_list)-1:
        Foreign_output += '\n'
        ln_num += 1



if (Foreign_output != ""):
    print(Foreign_output.strip())

if not found:
    # if we had to translate the error on the fly, just give a note to the user
    print('(Automatically generated)')
