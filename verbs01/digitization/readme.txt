
These notes by ejf.  Technical details.

Provide a version of skd digitization in Devanagari.

python skd_transcode.py slp1 deva /c/xampp/htdocs/cologne/csl-orig/v02/skd/skd.txt skd_deva.txt

temp_skd.txt is copy of /c/xampp/htdocs/cologne/csl-orig/v02/skd/skd.txt.

extract first 10002 lines from temp_skd.txt:

sed -n '1,10002p;10002q' temp_skd.txt > temp_skd_sample.txt

python skd_transcode.py slp1 deva temp_skd_sample.txt skd_deva_sample.txt


In csl-orig/v02/skd/:
git archive --format=zip -o temp.zip 953f24921d51cbe27cfe5bd0cd0ea8a2319da767 skd.txt
