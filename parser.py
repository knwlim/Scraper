import re

italic = r"\*([A-Za-z!|\\*§%œ¢¶ .?]+)\*"
bold = r"\%([A-Za-z!|\\*§%œ¢¶ .?]+)\%"
hyperlink_wo = r"\[([A-Za-z, .:_]+)\]\(([a-zA-Z0-9.:?$|_ -]+)\)"
hyperlink_np = r"\[([A-Za-z, .:_]+)\]\((http:\/\/[a-zA-Z0-9.:?$|_ -]+)\)"
hyperlink_sp = r"\[([A-Za-z, .:_]+)\]\((https:\/\/[a-zA-Z0-9.:?$|_ -]+)\)"
imagelink = r"\<(.*)>\(w=(\d+), ?h=(\d+)\)"
quoteline = r">>(.*)"
wikipedia = r"\[wp:(.*)\]"
escape_char_b = r"(\\\%)"
escape_char_i = r"(\\\*)"

def parse_nwodkram(text):
    """
    replacing characters with escape sequence into different characters so
    user can type % and * without interference of regular expression kick in
    (now user can't type ¢ and œ but it would be extremely rare case, yet still not perfect)
    """
    text = re.sub(escape_char_b, r"œ", text)
    text = re.sub(escape_char_i, r"¢", text)

    #nwodkram to HTML
    text = re.sub(imagelink, r'<img src="\1" style="width:\2px;height:\3px";>', text)
    text = re.sub(italic, r"<i>\1</i>", text)
    text = re.sub(bold, r"<b>\1</b>", text)
    text = re.sub(hyperlink_wo, r"<a href='http://\2'>\1</a>", text)
    text = re.sub(hyperlink_np, r"<a href='\2'>\1</a>", text)
    text = re.sub(hyperlink_sp, r"<a href='\2'>\1</a>", text)
    text = re.sub(quoteline, r"<blockquote>\1</blockquote>", text)
    text = re.sub(wikipedia, r'<a href="www.wikipedia.org/wiki/\1">Search Wikipedia for \1</a>', text)

    #replacing back again to original character
    text = re.sub(r"œ",r"%" , text)
    text = re.sub(r"¢",r"*" , text)
    return text #returns the corresponding HTML

def difference_finder(str1, str2):
    """
    find the first position of difference occuered
    between two strings to spot what's wrong easily
    """

    # handle the case where one string is longer than the other
    maxlen = len(str2) if len(str1) < len(str2) else len(str1)
    result1, result2 = '', ''

    # loop through the characters
    for i in range(maxlen):
        # use a slice rather than index in case one string longer than other
        letter1 = str1[i:i + 1]
        letter2 = str2[i:i + 1]
        # create string with differences
        if letter1 != letter2:
            result1 += letter1
            result2 += letter2
    # print out result
    print("First difference character :", result1)

def verify(function, input, expected_output):
    output = function(input)
    if output == expected_output :
        print("Actual output and expected output are the same (working as expected)",end="")
    else :
        difference_finder(output, expected_output)