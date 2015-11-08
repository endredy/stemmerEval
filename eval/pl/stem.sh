mkdir -p hunspell stempfel morfologik

function stem(){
# typ_fakt.ann_morphosyntax.xml.txt
    ./stem.engine.sh ../../corpus/goldLemma/pl/pnc/$1.ann_morphosyntax.xml.txt.words $1.txt
}

stem typ_lit
exit
stem typ_fakt
stem typ_nd
stem typ_inf-por
stem typ_net_interakt
stem typ_konwers
stem typ_net_nieinterakt
stem typ_listy
stem typ_nklas
stem typ_publ
stem typ_lit_poezja
stem typ_qmow
stem typ_media
stem typ_urzed

./eval.sh