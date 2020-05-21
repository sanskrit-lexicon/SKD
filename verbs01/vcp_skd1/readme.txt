
'side-by-side' report for vcp and skd verbs

* preparation of equivalence classes of verbs
An equivalence class of verbs is a set of ENTRIES.
For this purpose, an 'entry' is given by a pair (k1,L) of 
entry headword k1 and Cologne ID.
An equivalence class is then a SEQUENCE of such pairs.
One usual criterion for equivalence between two entries is that the entries have
the same headword  (e.g., (k,L1) and (k,L2) with the same headword 'k').
For the purpose of verb classification and mapping, we might 
have (k1,L1) ~ (k2,L2) even though k1 != k2.  An example with skd is
 (udJa,4713) ~ (ujJa,4431).  
Such exceptions are, for skd, in file skd_ecs_manual.txt
python verb_ec.py slp1 ../../../skd/verbs01/skd_verb1.txt skd_ecs_manual.txt skd_ecs.txt
python verb_ec.py deva ../../../skd/verbs01/skd_verb1.txt skd_ecs_manual.txt skd_ecs_deva.txt

python verb_ec.py slp1 ../../../vcp/verbs01/vcp_verb1.txt vcp_ecs_manual.txt vcp_ecs.txt
python verb_ec.py deva ../../../vcp/verbs01/vcp_verb1.txt vcp_ecs_manual.txt vcp_ecs_deva.txt

* vcp_skd_ec_map
python vcp_skd_ec_map.py slp1 vcp_ecs.txt skd_ecs.txt vcp_skd_map.txt vcp_skd_ec_map.txt
python vcp_skd_ec_map.py deva vcp_ecs.txt skd_ecs.txt vcp_skd_map.txt vcp_skd_ec_map_deva.txt

* vcp_skd_ec_verb2
python vcp_skd_ec_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_ec_map.txt vcp_skd_ec_verb2.html 

python vcp_skd_ec_verb2.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_ec_map.txt vcp_skd_ec_verb2_deva.html 


* NOT USED vcp_skd_verb1
python vcp_skd_verb1.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1.txt

python vcp_skd_verb1.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1_deva.txt

preliminary. A summary.

* vcp_skd_verb2

python vcp_skd_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_ecs.txt skd_ecs.txt vcp_skd_map.txt vcp_skd_verb2.html vcp_skd_unmatched.html 

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
python dump_verb.py slp1 ../../../../cologne/csl-orig/v02/vcp/vcp.txt vcp_skd_verb1_test1.txt dump_verb_skd_nomatch.txt

dump_verb.py is variation of ../verb1.py
dump_verb_skd_nomatch.txt dumps the VCP data for the (skd) verb spellings
in vcp_skd_verb1_test1.txt

dump vcp.txt records using headwords (k1 values) in vcp_skd_verb1_test1.txt


STEP 3:

* Further analysis of vcp verbs with no matching skd verb.
STEP 1:
python vcp_skd_verb2n.py test2 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb1_test2.txt


run test2 routine in vcp_skd_verb2n.py
Use 'test2' for first parameter option
Output file is vcp_skd_verb1_test2.txt
This is just a list of the vcp verbs that are NOT matched.
Sample line:
dict=vcp, k1=aMha, L=32, mw=aMh

STEP 2:
python dump_verb.py slp1 ../../../../cologne/csl-orig/v02/skd/skd.txt vcp_skd_verb1_test2.txt dump_verb_vcp_nomatch.txt

dump_verb_vcp_nomatch.txt dumps the SKD data for the (vcp) verb spellings
in vcp_skd_verb1_test2.txt

dump_verb.py is variation of ../verb1.py

dump vcp.txt records using headwords (k1 values) in vcp_skd_verb1_test1.txt


STEP 3:
