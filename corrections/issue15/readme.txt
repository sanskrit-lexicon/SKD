Corrrections discussed in issue 15:
 https://github.com/sanskrit-lexicon/SKD/issues/15
Modify pc in metalines to include column data.

-------------------------------------------------------------
temp_skd_0.txt
local copy of latest skd.txt from csl-orig repository
Using the local installation conventions of ejf:
cp /c/xampp/htdocs/cologne/csl-orig/v02/skd/skd.txt temp_skd_0.txt

-------------------------------------------------------------
SKD.pc.values.in.metalines.txt
provided by Andhrabharati
42196 lines
each line tab-delimited with 3 columns:
Sample:
<L>1	<pc>1-001	[1-001-a]
<L>2	<pc>1-001	[1-001-a]

-------------------------------------------------------------
Objective:  change the pc element of metaline according to the above.
Example for L=1
old metaline:
<L>1<pc>1-001<k1>a<k2>a
new metaline:
<L>1<pc>1-001-a<k1>a<k2>a
-------------------------------------------------------------
# make change_1.txt,
# the change transactions to apply to temp_skd_0.txt
# Note This is fairly slow, due to use of linear search in
# get_pcrec_for_entry function. On my fast pc it took about a minute.

python test_make_change_pc.py temp_skd_0.txt SKD.pc.values.in.metalines.txt change_1.txt

-------------------------------------------------------------
temp_skd_1.txt  Apply changes
python updateByLine.py temp_skd_0.txt change_1.txt temp_skd_1.txt
580774 lines read from temp_skd_0.txt
580774 records written to temp_skd_1.txt
42196 change transactions from change_1.txt
42196 of type new

-------------------------------------------------------------
temp_skd_1.txt  now ready for replacing  csl-orig/v02/skd/skd.txt
=============================================================

Next exercise: See how to replace the slow get_pcrec_for_entry
function with a much faster method
using Python dictionary.

