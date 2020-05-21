
echo "skd_ecs reports"
python verb_ec.py slp1 ../../../skd/verbs01/skd_verb1.txt skd_ecs_manual.txt skd_ecs.txt
python verb_ec.py deva ../../../skd/verbs01/skd_verb1.txt skd_ecs_manual.txt skd_ecs_deva.txt

echo "vcp_ecs reports"
python verb_ec.py slp1 ../../../vcp/verbs01/vcp_verb1.txt vcp_ecs_manual.txt vcp_ecs.txt
python verb_ec.py deva ../../../vcp/verbs01/vcp_verb1.txt vcp_ecs_manual.txt vcp_ecs_deva.txt

echo "vcp_skd_ec_map reports"
python vcp_skd_ec_map.py slp1 vcp_ecs.txt skd_ecs.txt vcp_skd_map.txt vcp_skd_ec_map.txt
python vcp_skd_ec_map.py deva vcp_ecs.txt skd_ecs.txt vcp_skd_map.txt vcp_skd_ec_map_deva.txt

echo "vcp_skd_ec_verb2 reports"
python vcp_skd_ec_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_ec_map.txt vcp_skd_ec_verb2.html 

python vcp_skd_ec_verb2.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_ec_map.txt vcp_skd_ec_verb2_deva.html 

exit 0
# rest kept temporarily
python vcp_skd_verb1.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_verb1.txt

#preliminary. A summary.


#* vcp_skd_verb2

echo "vcp_skd_verb2"
python vcp_skd_verb2.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2.html 

python vcp_skd_verb2.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_deva.html 

python vcp_skd_verb2n.py slp1 ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch.html

python vcp_skd_verb2n.py deva ../../../vcp/verbs01/vcp_verb1.txt  ../../../skd/verbs01/skd_verb1.txt vcp_skd_map.txt vcp_skd_verb2_nomatch_deva.html 

