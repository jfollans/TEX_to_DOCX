import fnmatch, re, sys


if __name__ == "__main__":

    input_fname = sys.argv[1]
    output_fname = sys.argv[2]

    print("\n\n\nParsing markdown\n\n\n")

    # read in the intermediate markdown file
    infile = open(input_fname)
    data = infile.readlines()
    infile.close()
    data_compressed = ''.join(data)


    """ I need to catch two problems.     
    
    The first is misformed equation labels,
    which are created by pandoc as follows:

    $$C = \mu / \sigma \label{eq:speckle_contrast}$$    
    
    but should be

    $$ C = \mu / \sigma $${#eq:speckle_contrast}
    
    """

    query_eqns = "\\\\label\{(.*)\}\$\$"
    eqn_search = re.finditer(query_eqns, data_compressed)
    edited_data = data_compressed
    for o in eqn_search:
        label = o.groups()[0]
        foundstring = o.string[o.start():o.end()]
        replacement = "$${#" + label + "}"
        edited_data = edited_data.replace(foundstring, replacement)

    """ The second problem is misformed equation references. Pandoc generates them as
    [\[eq:speckle_contrast\]](#eq:speckle_contrast){reference-type="ref" reference="eq:speckle_contrast"}

    when they should be

    [@eq:speckle_contrast]

    """

    query_refs = "\[.*\]\(\#(eq:.*)\)\{[ -=\":_A-Za-z|\n]*\}"
    ref_search = re.finditer(query_refs, data_compressed)
    for o in ref_search:
        foundstring = o.string[o.start():o.end()]
        replacement = "[@" + o.groups()[0].replace("eq:", "Eq:") + "]"
        edited_data = edited_data.replace(foundstring, replacement)
    

    # fix double integral sign
    query = "bigintss"
    matches = re.finditer(query, edited_data)
    for o in matches:
        foundstring = o.string[o.start():o.end()]
        replacement = "int"
        edited_data = edited_data.replace(foundstring, replacement)

    # write the output file    
    outfile = open(output_fname, 'w')
    outfile.writelines(edited_data)
    outfile.close()
    
    
    print("done")


