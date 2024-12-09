# README for .tex to .docx conversion


## Usage

1. Copy all files in this directory into the main tex project directory.
2. Run the following command:
   - "python master_script.py <MAIN_TEX.tex> <MAIN_BIB.bib>"
   - replacing <MAIN_TEX.tex> with the main .tex file for the project, and <MAIN_BIB.bib> with the main .bib file for the project.

## Dependencies

The code has a few dependencies:
1. Pandoc 3.3 for document conversion. You can use a newer version, but I can’t promise that it won’t break things. To get citations and equation/figure/table/section reference correct, some pandoc features you need are
   - Citeproc
   - pandoc-crossref
2. Ghostscript for converting vector graphic .eps files to .png image files.
3. Python-docx for touching up the .docx files we generate.

## How it works

Pandoc is a document conversion tool that works well for a lot of scenarios, but it can fail for sufficiently complicated files. In particular, .docx is a janky format under the hood and sufficiently different from .tex that a naive conversion will often produce a messy output file. The best way I found around this was to do an intermediate conversion step to Markdown (.md), and then convert to .docx from there.

This code works as follows:

1. Convert .eps files to .png files. Word documents can't handle .eps files, so we need a different format. The code recursively searches the main project directory for .eps files and converts them to .png’s.
2. Clean up any .tex files in the directory. Keep your .tex files all in the same main directory.
3. Run pandoc to convert the main .tex file to .md. This step includes citations using the bibliography file specified.
4. Clean up the generated markdown file. This fixes equation references and some custom formatting issues. I’ve tried to remove the ones specific to my thesis, but YMMV.
5. Run pandoc to convert the .md file to .docx. This includes bibliography, equation labeling, custom format reference document, table of contents, etc.
6. Run one last processing step to fix table alignment in the .docx file. This creates an output file named “FINAL_OUTPUT.docx”.

