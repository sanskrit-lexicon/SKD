
echo "vcp_skd_verb1"
python vcp_skd_verb1.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1.txt

#preliminary. A summary.


#* vcp_skd_verb2

echo "vcp_skd_verb2"
python vcp_skd_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2.html 

python vcp_skd_verb2.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_deva.html 

python vcp_skd_verb2n.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch.html

python vcp_skd_verb2n.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch_deva.html 

