import sys, os, glob

# dependencies: Ghostscript (eps to png), pandoc (with citeproc, pandoc-crossref), docx


# this script takes in two parameters:
#   1. The main .tex file that we want to convert
#   2. The bibliography file that we're using for the paper

if __name__ == "__main__":

    # Set up input parameters for the conversion
    texname = sys.argv[1]
    bibname = sys.argv[2]

    md_intermediate_name = "out.md"
    md_out_name = "parsed_md.md"

    word_output_name = "out_partial.docx"
    final_output_name = "FINAL_OUTPUT.docx"


    # convert all .eps figures to .png images
    os.system("python eps_converter.py")

    # parse the chapter .tex files
    chapterlist = glob.glob(".\\*.tex")
    print(chapterlist)
    for chapter in chapterlist:
        n = chapter.split("\\")[-1]
        os.system(f"python process_tex_code.py {chapter} .\\{n}")

    # parse the main .tex tile
    os.system(f"python process_tex_code.py {texname} parsed_tex.tex")
    
    # .tex to .md conversion
    os.system(f"pandoc -s parsed_tex.tex -o {md_intermediate_name} --csl=spie-journals.csl --verbose --citeproc --bibliography={bibname}")

    # clean up the markdown to fix citations
    os.system(f"python processing.py {md_intermediate_name} {md_out_name}")

    # convert .md to .docx
    os.system(f"pandoc -s {md_out_name} -o {word_output_name} --csl=spie-journals.csl --verbose --filter pandoc-crossref --citeproc --bibliography={bibname} -M autoEqnLabels --reference-doc=./custom-reference.docx -N --metadata-file header.txt")

    # fix table references and alignment
    os.system(f"python fix_tables.py {word_output_name} {final_output_name}")