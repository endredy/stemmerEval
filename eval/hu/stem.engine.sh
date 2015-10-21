
WORDSPATH=../../corpus/goldLemma/hu/data
#HUMOR
~/humor/bin/stem2005Console ~/humor/bin/huau.lex ~/humor/bin/huastem.lex 1038 65001 -filter_stem -output_stem -file $WORDSPATH/domain.$1.utf.words > humor/domain.$1.txt
#-build_cache
exit
#foma
#cd ../hunmorph-foma-hunmorph-foma
#cat ../szeged/data/$1.utf.words | ../linux64/flookup -x hun0530.foma > ../szeged/foma/$1.txt
# javitott foma:
#cd ../hunmorph-foma-hunmorph-fomaIK
#cat ../szeged/data/$1.utf.words | ../linux64/flookup -x hun0923.foma > ../szeged/foma/$1.txt
#cd ../szeged


#hunspell
#cd ../hunspell
#java -cp .:hunspell.jar:jna.jar MyStemFilter dicts/hu_HU ../szeged/data/$1.utf.words > ../szeged/hunspell/$1.txt
#cd ../szeged

#snowball
#python3 snowballTest.py hungarian data/$1.utf.words > snowball/$1.txt

# ocamorph
#../hunmorph/ocamorph --compounds --bin ../hunmorph/morphdb_hu.bin --in data/$1.iso.words > ocamorph/$1.txt

# ocastem
#default:
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin > ocastem/$1.txt
# sok kapcsolo
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --lowercase no --decompounding no --stem-known all > ocastem/$1.txt
#kevesebb
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --lowercase no --decompounding no > ocastem/$1.txt
#meg kevesebb
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --decompounding no  > ocastem.decomp/$1.txt

# ujabb Attila keres
cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --decompounding no --stem-known all > ocastem/$1.txt