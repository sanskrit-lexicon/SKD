
'side-by-side' report for vcp and skd verbs

* vcp_skd_verb1
python vcp_skd_verb1.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1.txt

python vcp_skd_verb1.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1_deva.txt

preliminary. A summary.


* vcp_skd_verb2

python vcp_skd_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2.html vcp_skd_unmatched.html 

python vcp_skd_verb2.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_deva.html vcp_skd_unmatched_deva.html

python vcp_skd_verb2n.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch.html

python vcp_skd_verb2n.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch_deva.html 


* Further analysis of skd verbs with no matching vcp verb.
STEP 1:
python vcp_skd_verb2n.py test1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb1_test1.txt


run test1 routine in vcp_skd_verb2n.py
Use 'test1' for first parameter option
Output file is vcp_skd_verb1_test1.txt
This is just a list of the skd verbs that are NOT matched.
Sample line:
dict=skd, k1=atwaNa, L=706, mw=?


STEP 2:
python vcp_verb1.py slp1 ../../../../cologne/csl-orig/v02/vcp/vcp.txt vcp_skd_verb1_test1.txt vcp_verb1_nomatch.txt

vcp_verb1.py is variation of ../verb1.py

dump vcp.txt records using headwords (k1 values) in vcp_skd_verb1_test1.txt


STEP 3:
