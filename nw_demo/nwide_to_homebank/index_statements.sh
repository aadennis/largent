#!/usr/bin/env bash

# This script renames the PDF files in the current directory 
# by prepending the month number to the filename.


declare -A mon=(
    [Jan]=01 [Feb]=02 [Mar]=03 [Apr]=04
    [May]=05 [Jun]=06 [Jul]=07 [Aug]=08
    [Sep]=09 [Oct]=10 [Nov]=11 [Dec]=12
)

# cd into the directory containing the PDF files
dir="x"
cd $dir || exit 1

for f in *.pdf
do
    month=${f%% *}
    echo mv "$f" "${mon[$month]} $f"
done

