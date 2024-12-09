import glob, os

# Takes in an input glob (search for filenames expanding wildcards)
# runs ghostscript on those files to convert .eps to .png files
def conv_glob(globstr):
    flist = glob.glob(globstr)

    for input_fname in flist:

        output_fname = input_fname.replace(".eps", ".png")
        
        command_str = f"gswin64c -dSAFER -dBATCH -dNOPAUSE -dEPSCrop -sDEVICE=png16m -r600 \"-sOutputFile={output_fname}\" {input_fname}"
        
        os.system(command_str)

if __name__ == "__main__":

    conv_glob("./*.eps")
    conv_glob("./*/*.eps")
    conv_glob("./*/*/*.eps")