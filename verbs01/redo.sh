#echo "make mwverbs"
# In local installation, this directory is
# /c/xampp/htdocs/sanskrit-lexicon/skd/verbs01
# And csl-orig directory is
# /c/xampp/htdocs/cologne/csl-orig
# Thus csl-orig relative location relative to this directory is
CSLORIG="../../../cologne/csl-orig"
mwverbs1="../../MWS/mwverbs/mwverbs1.txt"
#python mwverb.py mw ${CSLORIG}/v02/mw/mw.txt mwverbs.txt
#echo "make mwverbs1"
#python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "make skd_verb_filter"
python skd_verb_filter.py ${CSLORIG}/v02/skd/skd.txt skd_verb_filter.txt
echo "make skd_verb_filter_map"
python skd_verb_filter_map.py skd_verb_filter.txt vcp_mw_map_init.txt ${mwverbs1} skd_verb_filter_map.txt
echo "make skd_verb1"
python verb1.py slp1 ${CSLORIG}/v02/skd/skd.txt skd_verb_filter_map.txt skd_verb1.txt
echo "make skd_verb1_deva"
python verb1.py deva ${CSLORIG}/v02/skd/skd.txt skd_verb_filter_map.txt skd_verb1_deva.txt
echo "REDO.SH done"
