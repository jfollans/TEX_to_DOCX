import sys, re


if __name__ == "__main__":
    
    instr = sys.argv[1]
    outstr = sys.argv[2]

    # read in the raw tex file
    infile = open(instr, encoding="utf-8")
    data = infile.readlines()
    infile.close()
    data_compressed = ''.join(data)

    # replace any instances of sidewaystable in the latex
    edited_data = data_compressed
    edited_data = edited_data.replace("sidewaystable", "table")
    
    # Replace \includegraphics{*.eps} with \includegraphics{*.png}
    query = "\\\\includegraphics.*\{(.*\.eps)\}"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]  
        replacement = foundstring.replace(".eps", ".png")
        edited_data = edited_data.replace(foundstring, replacement)
            
    # Replace \textnormal{*} with \textrm{*}
    query = "\\\\textnormal\{.*}"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()] 
        replacement = foundstring.replace("textnormal", "textrm")
        edited_data = edited_data.replace(foundstring, replacement)

    # Replace \begin{split} or \end{split} with nothing
    query = "\\\\begin\{split\}|\\\\end\{split\}"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]            
        replacement = ""
        edited_data = edited_data.replace(foundstring, replacement)

    # replace the &= syntax for the split equation environment with a default =
    query = "\&="
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = "="
        edited_data = edited_data.replace(foundstring, replacement)

    # replace Equation \ref{eq:*} with \ref{eq:*}
    query = "[Ee]quation (\\\\ref\{eq:.*\})"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = o.groups()[0]
        edited_data = edited_data.replace(foundstring, replacement)

    # replace \bigintss calls with \int
    query = "\\\\bigintss"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = foundstring.replace("bigintss", "int")
        edited_data = edited_data.replace(foundstring, replacement)

    # fix chapter references
    query = "\\\\include\{(chapters/.*)\}"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = foundstring.replace("chapters", "edited_chapters")
        edited_data = edited_data.replace(foundstring, replacement)

    # fix indent in equations
    query = "\\\\indent"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = "    "
        edited_data = edited_data.replace(foundstring, replacement)


    # write out the updated tex file
    outfile = open(outstr, 'w')
    outfile.writelines(edited_data)
    outfile.close()

    
    #print("done")


