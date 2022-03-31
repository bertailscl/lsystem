# TP10
# #By Clément Bertails
Containing tp10

## Using the Program
Use "make" to compile and execute ./tp10_hangMan {path of word's file}

## Notes
"make run" won't work because it need an argument.

## Compilation
Go to the decompressed folder via a terminal. Execute "make".

## Generate Doxygen
If you want to generate the Doxygen, run "make docs". !! You will have to install the graphviz package to avoid errors when generating the doxygen !!

## Read doxygen
Open the doc/html/index.html page generated at the time of "make docs". The Doxyfile is also created with the above command.

## Delete unnecessary files
Run "make clean" : delete the bin folder containing the object files (*.o), the save folder containing a backup of the src folder, the doc folder containing the Doxygen, the last archive created by "make give", the src.old folder created by "make restore" and the executable.

## Create save
Run "make save": create the save folder if it doesn't exist and copy the src folder into it.

## Revert to last save
Run "make restore": restore the backup from the save folder.

## Archive the program
Run "make give": a ready-to-give archive is created.
