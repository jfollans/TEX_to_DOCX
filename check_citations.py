import sys, fnmatch, re
import glob, pprint



if __name__ == "__main__":


    bibfname = "./bibliography_clean2.bib"
    bib_file = open(bibfname, 'r', errors='ignore')
    bib_data = bib_file.readlines()
    bib_file.close()

    bib_data_compressed = ''.join(bib_data)

    #print(bib_data_compressed)



    # bibtex key query
    key_query1 = "@.*{([a-zA-Z0-9_:.]*),"
    key_query2 = "@.*{(.*),"

    matches = re.finditer(key_query2, bib_data_compressed)
    print(matches)
    key_list = list()
    for o in matches:
        #print(o)
        key_list.append(o.groups()[0])
        pass

    print(key_list)
    print(len(key_list))

    unused_key_list = key_list

    filelist = glob.glob("./**/*.tex", recursive=True)
    print("\n\n")

    citationlist = list()
    citation_query = "\\\\cite{([^}]*)}"

    for filename in filelist:
        f_in = open(filename, 'r')
        f_data = ''.join(f_in.readlines())
        f_in.close()
        #print(f_data)
        citation_matches = re.finditer(citation_query, f_data)
        
        for o in citation_matches:
            citationstr = o.groups()[0]

            citation_temp = citationstr.split(",")
            #print(citation_temp)
            for s in citation_temp:
                citationlist.append(s.strip())

    #pprint.pprint(citationlist)

    for elt in citationlist:
        try:
            unused_key_list.pop(unused_key_list.index(elt))
        except ValueError:
            pass

    pprint.pprint(unused_key_list)
    print(len(unused_key_list))
    print("Done!")