SKD/issues/issue17/readme.txt

Transcoding in preparation for Andhrabharati editing

  Local copy of /c/xampp/htdocs/cologne/csl-orig/v02/skd/skd.txt 
cp /c/xampp/htdocs/cologne/csl-orig/v02/skd/skd.txt temp_skd_orig.txt
   at commit 576e9ca1d8ba1bf3ca3caeee38054aa0b0083ece of csl-orig

***********************************************************
PRELIMINARY OBSERVATIONS
***********************************************************
Count all the xml tags
python tags.py temp_skd_orig.txt tags.txt
16 tags:
</F> 5
<C10> 24
<C11> 12
<C1> 921
<C2> 926
<C3> 824
<C4> 825
<C5> 789
<C6> 55
<C7> 46
<C8> 46
<C9> 42
<F> 5
<H> 109
<P> 1130
<Picture> 5
------------------------
In conversion to skd.xml:
<Ci> -> <C n="i"/>   (i=1,2,...,11)
<F>X</F> -> <F>X</F>  (X includes multiple lines)
<P> -> <mark n="P"/>
<H> -> <mark n="H"/>
<Picture> -> <mark n="Picture"/>

alaNkAraH  columns 1&2 should be displayed 'together' -
  but in .txt,  these are separated, since
  all lines of column 1 precedes lines of column 2.
-----------------------
***********************************************************
***********************************************************

Oct 19, 2023
transcoding of skd.txt.
code adapted from pwk code.
Refer https://github.com/sanskrit-lexicon/PWK/issues/95#issuecomment-1639204988

-----------------------------------------------
devanagari conversion
-----------------------
cp temp_skd_orig.txt temp_skd_0.txt

python skd_transcode.py slp1 deva temp_skd_0.txt temp_skd_0_deva.txt
# check invertibility
python skd_transcode.py deva slp1 temp_skd_0_deva.txt temp_skd_0_deva_slp1.txt
diff temp_skd_0.txt temp_skd_0_deva_slp1.txt | wc -l
# 0 No diff invertibility confirmed

-----------------------------------------------
iast conversion
-----------------------

python skd_transcode.py slp1 roman temp_skd_0.txt temp_skd_0_iast.txt

# confirm invertibility:
python skd_transcode.py roman slp1 temp_skd_0_iast.txt temp_skd_0_iast_slp1.txt
diff temp_skd_0.txt temp_skd_0_iast_slp1.txt | wc -l
# 0 (no difference)

