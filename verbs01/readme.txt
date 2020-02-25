

* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* corrections
* 02-23-2020  skd_verb_filter.txt
python skd_verb_filter.py ../skd.txt skd_verb_filter.txt

* exceptional verbs
8480 kUpa  
31310 varRa
37770 sapa
42132 hrapa

Filter for 'iti kavikalpadrumaH' -- verb list from Vopadeva.
Most of these occur on the first line.
Some on second.
A few hyphenations 

* skd_verb_filter_map
python skd_verb_filter_map.py skd_verb_filter.txt vcp_mw_map_init.txt mwverbs1.txt skd_verb_filter_map.txt

Get correspondences between skd verb spellings and
 - vcp verb spellings
 - mw verb spellings
Use vcp_mw_map_init.txt


* 02-24-2020 verb.txt
python verb1.py slp1 ../skd.txt skd_verb_filter_map.txt skd_verb1.txt
python verb1.py deva ../skd.txt skd_verb_filter_map.txt skd_verb1_deva.txt


verb1.txt looks for patterns in VCP entries that
usually indicate that the entry is a verb. 
The patterns are:
1) presence of <div n="p">— Mit {#xx#}   xx is typically a preverb, like ud, upa,
   The upasarga form is required
 We currently exclude presence of Caus., Desid., Intens.
2) presence of <ab>Caus.</ab>   entry has a causal form
3) <ab>Desid.</ab>
4) <ab>Intens.</ab>

* format of verb1.txt records
  Three ':' separated fields per line
 1. pw headword
 2. pw Lnums corresponding to verbs. If more than 1 L, spearate using '&'
 3. pw upasargas, a comma-separated list.
     If more than 1 L, the upasarga lists for each L are separated by '~'

* Notes on verbs MW changes
MW  These changes made to
<info verb="root"/>
28830 in  mark as verb
37403 urj m a v
53560 kus m a v
67683 gozwa m a v
81421 qimb  Add alternate spelling qimb to qimp
81418 qim  m a v
81478 qval m a v
81504 QuRQ m a v
101328.1 DIr m a v ? (avaDIr)
158406 mark  m a v
178119 rimb  m a v
182948 luRq  m a v
260012 svek  m a v
264639 hOq   m a v
101328.1 DIr m a v

* VCP changes
17852 gUrha -> gUrdda   (print error?)
18633 GagDa -> GagGa (print error or typo?)
18794 GiRa -> GiRRa typo
37140 BrASaM -> BrASa  M is probably a typo, due to scan smudge.
38750 mrA -> mnA
48322 hrama -> hrasa   typo.

* Moved from VCP-Dhatus to VCP-Non-Dhatus
35190 PeRaka  is not a verb 
39830 rocI is not a verb

* 4852 avaDIra  verb  == avaDIr (MW)  

* skd_mw_map_edit.txt
 A mapping from skd spelling of roots to mw spelling.
python skd_mw_map_init.py verb1.txt skd_mw_map_init.txt

cp skd_mw_map_init.txt skd_mw_map_edit.txt

