# Evaluation of the Filipino spell checker (ud word list)

100 test sentences, n-gram threshold 0.20, with extensions.

| Metric | Test sentences | + held-out clean sentences | Paper |
|---|---|---|---|
| Recall | 100.00% | 100.00% | 81% |
| Precision | 34.13% | 20.16% | 53.64% |
| F-measure | 50.89% | 33.56% | 64.53% |
| Suggestion adequacy | 31.00% | 31.00% | 87.78% |
| Correct word ranked first | 30.00% | 30.00% | not reported |

TP = 100, FN = 0, FP = 193 in the test sentences, plus 203 false alarm(s) in 40 clean sentences (478 words).

## Results per error type (Table I categories)

| Error type | Count | Detected | Correct word suggested |
|---|---|---|---|
| insertion | 8 | 8 | 1 |
| deletion | 28 | 28 | 6 |
| substitution | 37 | 37 | 8 |
| space deletion | 9 | 9 | 8 |
| hyphen insertion | 12 | 12 | 2 |
| space insertion | 6 | 6 | 6 |

## False negatives (errors that were not flagged)

| Incorrect | Correct | Accepted by |
|---|---|---|

## False positives in the test sentences

| Word | Reason | Line |
|---|---|---|
| paaralan | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 9 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 10 |
| simbahan | n-gram: rare trigram(s) sim, imb, mba in stem 'simba' | 10 |
| Masayang | n-gram: rare trigram(s) say in stem 'sayang' | 11 |
| bakuran | n-gram: rare trigram(s) bak, aku, kur, ur_ in stem 'bakur' | 11 |
| Bumili | n-gram: rare trigram(s) bil, li_ in stem 'bili' | 12 |
| umaga | n-gram: rare trigram(s) _ag in stem 'aga' | 12 |
| nag-aaral | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 13 |
| medisina | n-gram: rare trigram(s) _me, med, edi, dis, isi, sin in stem 'medisina' | 13 |
| Mabilis | n-gram: rare trigram(s) bil, lis, is_ in stem 'bilis' | 14 |
| bukid | n-gram: rare trigram(s) buk, uki, kid, id_ in stem 'bukid' | 14 |
| Sinulat | n-gram: rare trigram(s) _su, sul, lat in stem 'sulat' | 15 |
| kanyang | n-gram: rare trigram(s) _ny, nya in stem 'nyang' | 15 |
| tungkol | n-gram: rare trigram(s) tun, ngk, gko, kol, ol_ in stem 'tungkol' | 15 |
| kalikasan | n-gram: rare trigram(s) lik, ika, kas in stem 'likas' | 15 |
| guro | n-gram: rare trigram(s) _gu, gur, uro, ro_ in stem 'guro' | 16 |
| matematika | n-gram: rare trigram(s) _te, tem, ema, mat, ati, tik, ika, ka_ in stem 'tematika' | 16 |
| ikatlong | n-gram: rare trigram(s) kat, atl, tlo, lon in stem 'katlong' | 16 |
| baitang | n-gram: rare trigram(s) bai, ait, ita, tan in stem 'baitang' | 16 |
| laruan | n-gram: rare trigram(s) lar, aru, ru_ in stem 'laru' | 17 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 19 |
| lola | n-gram: rare trigram(s) _lo, lol, ola in stem 'lola' | 19 |
| noong | n-gram: rare trigram(s) _no, noo, oon in stem 'noong' | 19 |
| Linggo | n-gram: rare trigram(s) lin, ngg, ggo in stem 'linggo' | 19 |
| aklat | n-gram: rare trigram(s) akl, kla, lat in stem 'aklat' | 20 |
| aklatan | n-gram: rare trigram(s) akl, kla, lat in stem 'aklat' | 20 |
| Uminom | n-gram: rare trigram(s) ino, nom, om_ in stem 'inom' | 21 |
| nauuhaw | n-gram: rare trigram(s) _uh, uha, haw in stem 'uhaw' | 21 |
| iyong | n-gram: rare trigram(s) _yo in stem 'yong' | 22 |
| kahapon | n-gram: rare trigram(s) hap, apo, pon in stem 'hapon' | 22 |
| Nagluto | n-gram: rare trigram(s) lut, uto in stem 'luto' | 23 |
| adobo | n-gram: rare trigram(s) _ad, ado, dob, obo, bo_ in stem 'adobo' | 23 |
| malinis | n-gram: rare trigram(s) lis, is_ in stem 'lis' | 24 |
| Kumain | n-gram: rare trigram(s) kai, ain in stem 'kain' | 25 |
| masarap | n-gram: rare trigram(s) sar, rap, ap_ in stem 'sarap' | 25 |
| handaan | n-gram: rare trigram(s) han, and, da_ in stem 'handa' | 25 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 26 |
| dalawang | n-gram: rare trigram(s) law, wan in stem 'dalawang' | 26 |
| palapag | n-gram: rare trigram(s) lap, pag, ag_ in stem 'lapag' | 26 |
| lola | n-gram: rare trigram(s) _lo, lol, ola in stem 'lola' | 27 |
| nagkuwento | n-gram: rare trigram(s) kuw, uwe, wen, ent, nto in stem 'kuwento' | 27 |
| tungkol | n-gram: rare trigram(s) tun, ngk, gko, kol, ol_ in stem 'tungkol' | 27 |
| buwan | n-gram: rare trigram(s) buw, uw_ in stem 'buw' | 27 |
| magsasaka | n-gram: rare trigram(s) sak, ka_ in stem 'saka' | 28 |
| nagtanim | n-gram: rare trigram(s) tan, nim, im_ in stem 'tanim' | 28 |
| gulay | n-gram: rare trigram(s) _gu, gul, lay in stem 'gulay' | 28 |
| kinabukasan | n-gram: rare trigram(s) kab, abu, buk, uka, kas in stem 'kabukas' | 29 |
| dagat | n-gram: rare trigram(s) dag, gat in stem 'dagat' | 30 |
| noong | n-gram: rare trigram(s) _no, noo, oon in stem 'noong' | 30 |
| bakasyon | n-gram: rare trigram(s) bak, kas, asy, syo in stem 'bakasyon' | 30 |
| kapatid | n-gram: rare trigram(s) ati, tid, id_ in stem 'patid' | 31 |
| aralin | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 32 |
| agham | n-gram: rare trigram(s) _ag, agh, gha, ham, am_ in stem 'agham' | 32 |
| naglalaro | n-gram: rare trigram(s) lar, aro, ro_ in stem 'laro' | 33 |
| parke | n-gram: rare trigram(s) par, ark, rke, ke_ in stem 'parke' | 33 |
| ating | n-gram: rare trigram(s) _at, ati, tin in stem 'ating' | 34 |
| mayaman | n-gram: rare trigram(s) _ya, yam, am_ in stem 'yam' | 34 |
| likas | n-gram: rare trigram(s) lik, ika, kas in stem 'likas' | 34 |
| yaman | n-gram: rare trigram(s) _ya, yam, am_ in stem 'yam' | 34 |
| ganap | n-gram: rare trigram(s) gan, nap, ap_ in stem 'ganap' | 35 |
| ikapito | n-gram: rare trigram(s) pit in stem 'pito' | 35 |
| umaga | n-gram: rare trigram(s) _ag in stem 'aga' | 35 |
| Sumulat | n-gram: rare trigram(s) _su, sul, lat in stem 'sulat' | 36 |
| dyip | n-gram: rare trigram(s) _dy, dyi, yip, ip_ in stem 'dyip' | 37 |
| puno | n-gram: rare trigram(s) pun, uno, no_ in stem 'puno' | 37 |
| Masarap | n-gram: rare trigram(s) sar, rap, ap_ in stem 'sarap' | 38 |
| mangga | n-gram: rare trigram(s) man, ngg, gga in stem 'mangga' | 38 |
| magandang | n-gram: rare trigram(s) and, dan in stem 'andang' | 39 |
| bundok | n-gram: rare trigram(s) bun, und, ndo, dok, ok_ in stem 'bundok' | 39 |
| ibon | n-gram: rare trigram(s) _bo, bon in stem 'bon' | 40 |
| himpapawid | n-gram: rare trigram(s) _hi, him, imp, mpa, pap, paw, awi, wid, id_ in stem 'himpapawid' | 40 |
| pulong | n-gram: rare trigram(s) pul, ulo, lon in stem 'pulong' | 41 |
| ulan | n-gram: rare trigram(s) _ul in stem 'ulan' | 41 |
| mahilig | n-gram: rare trigram(s) _hi in stem 'hilig' | 42 |
| nobela | n-gram: rare trigram(s) _no, nob, obe, bel, ela in stem 'nobela' | 42 |
| nating | n-gram: rare trigram(s) tin in stem 'ting' | 43 |
| ating | n-gram: rare trigram(s) _at, ati, tin in stem 'ating' | 43 |
| bisita | n-gram: rare trigram(s) bis, isi, sit, ita in stem 'bisita' | 44 |
| bagong | clitic-split: "bago ng" should be two words | 45 |
| kotse | n-gram: rare trigram(s) kot, ots, tse, se_ in stem 'kotse' | 45 |
| parke | n-gram: rare trigram(s) par, ark, rke, ke_ in stem 'parke' | 46 |
| hapunan | n-gram: rare trigram(s) hap, apu, pu_ in stem 'hapu' | 47 |
| lola | n-gram: rare trigram(s) _lo, lol, ola in stem 'lola' | 47 |
| kahapon | n-gram: rare trigram(s) hap, apo, pon in stem 'hapon' | 48 |
| malinis | n-gram: rare trigram(s) lis, is_ in stem 'lis' | 49 |
| malamig | n-gram: rare trigram(s) mig in stem 'lamig' | 49 |
| gamit | n-gram: rare trigram(s) gam, mit in stem 'gamit' | 50 |
| probinsiya | n-gram: rare trigram(s) _pr, pro, rob, obi, bin, ins, nsi, siy in stem 'probinsiya' | 51 |
| habang | n-gram: rare trigram(s) hab in stem 'habang' | 52 |
| naglalaro | n-gram: rare trigram(s) lar, aro, ro_ in stem 'laro' | 52 |
| ulan | n-gram: rare trigram(s) _ul in stem 'ulan' | 52 |
| tulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 53 |
| guro | n-gram: rare trigram(s) _gu, gur, uro, ro_ in stem 'guro' | 54 |
| nagbigay | n-gram: rare trigram(s) iga in stem 'bigay' | 54 |
| upang | n-gram: rare trigram(s) _up, upa, pan in stem 'upang' | 55 |
| bumili | n-gram: rare trigram(s) bil, li_ in stem 'bili' | 55 |
| gulay | n-gram: rare trigram(s) _gu, gul, lay in stem 'gulay' | 55 |
| kanyang | n-gram: rare trigram(s) _ny, nya in stem 'nyang' | 56 |
| mabait | n-gram: rare trigram(s) bai, ait in stem 'bait' | 56 |
| matulungin | n-gram: rare trigram(s) tul, ulu, lun in stem 'tulung' | 56 |
| langit | n-gram: rare trigram(s) ngi, git in stem 'langit' | 57 |
| hapon | n-gram: rare trigram(s) hap, apo, pon in stem 'hapon' | 57 |
| nating | n-gram: rare trigram(s) tin in stem 'ting' | 58 |
| mag-aral | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 58 |
| Nakatulog | n-gram: rare trigram(s) tul, ulo, log, og_ in stem 'tulog' | 60 |
| sanggol | n-gram: rare trigram(s) _go, gol, ol_ in stem 'gol' | 60 |
| presyo | n-gram: rare trigram(s) _pr, pre, res, esy, syo in stem 'presyo' | 61 |
| bigas | n-gram: rare trigram(s) iga, gas in stem 'bigas' | 61 |
| Naglakad | n-gram: rare trigram(s) kad, ad_ in stem 'lakad' | 62 |
| isda | n-gram: rare trigram(s) isd, sda, da_ in stem 'isda' | 63 |
| malinaw | n-gram: rare trigram(s) law in stem 'law' | 63 |
| Nagluto | n-gram: rare trigram(s) lut, uto in stem 'luto' | 64 |
| masarap | n-gram: rare trigram(s) sar, rap, ap_ in stem 'sarap' | 64 |
| kanyang | n-gram: rare trigram(s) _ny, nya in stem 'nyang' | 65 |
| laruan | n-gram: rare trigram(s) lar, aru, ru_ in stem 'laru' | 65 |
| Gusto | n-gram: rare trigram(s) _gu, gus, ust, sto in stem 'gusto' | 66 |
| kong | clitic-split: "ko ng" should be two words | 66 |
| bagong | clitic-split: "bago ng" should be two words | 66 |
| nobela | n-gram: rare trigram(s) _no, nob, obe, bel, ela in stem 'nobela' | 66 |
| magulang | n-gram: rare trigram(s) _ul in stem 'ulang' | 67 |
| igalang | n-gram: rare trigram(s) gal in stem 'galang' | 67 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 68 |
| paaralan | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 68 |
| tito | n-gram: rare trigram(s) tit in stem 'tito' | 69 |
| sundalo | n-gram: rare trigram(s) _su, sun, und, lo_ in stem 'sundalo' | 70 |
| nagbabantay | n-gram: rare trigram(s) ant, nta, tay in stem 'bantay' | 70 |
| tabing-dagat | n-gram: rare trigram(s) tab, bin, ng-, g-d, -da, dag, gat in stem 'tabing-dagat' | 71 |
| Bumili | n-gram: rare trigram(s) bil, li_ in stem 'bili' | 72 |
| bagong | clitic-split: "bago ng" should be two words | 72 |
| nagtatrabaho | n-gram: rare trigram(s) _tr, tra, rab, bah, aho, ho_ in stem 'trabaho' | 73 |
| kompanya | n-gram: rare trigram(s) kom, omp, mpa, pan, any, nya in stem 'kompanya' | 73 |
| tumutulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 74 |
| magsasaka | n-gram: rare trigram(s) sak, ka_ in stem 'saka' | 74 |
| dentista | n-gram: rare trigram(s) _de, den, ent, nti, tis, ist, sta in stem 'dentista' | 75 |
| puno | n-gram: rare trigram(s) pun, uno, no_ in stem 'puno' | 76 |
| nalalagas | n-gram: rare trigram(s) gas in stem 'lagas' | 76 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 77 |
| klase | n-gram: rare trigram(s) _kl, kla, las, ase, se_ in stem 'klase' | 77 |
| bukas | n-gram: rare trigram(s) buk, uka, kas in stem 'bukas' | 77 |
| kanyang | n-gram: rare trigram(s) _ny, nya in stem 'nyang' | 79 |
| lolo | n-gram: rare trigram(s) _lo, lol, olo, lo_ in stem 'lolo' | 79 |
| matapang | n-gram: rare trigram(s) tap, pan in stem 'tapang' | 79 |
| makatulog | n-gram: rare trigram(s) tul, ulo, log, og_ in stem 'tulog' | 80 |
| ingay | n-gram: rare trigram(s) nga in stem 'ngay' | 80 |
| panahon | n-gram: rare trigram(s) _ah, aho, hon in stem 'ahon' | 81 |
| kanya | n-gram: rare trigram(s) _ny, nya in stem 'nya' | 82 |
| sumasagot | n-gram: rare trigram(s) sag, ago, got in stem 'sagot' | 82 |
| Kumain | n-gram: rare trigram(s) kai, ain in stem 'kain' | 83 |
| tanghalian | n-gram: rare trigram(s) tan, ngh, gha, li_ in stem 'tanghali' | 83 |
| natutong | n-gram: rare trigram(s) tut, uto, ton in stem 'tutong' | 84 |
| lumangoy | n-gram: rare trigram(s) goy, oy_ in stem 'langoy' | 84 |
| Bukas | n-gram: rare trigram(s) buk, uka, kas in stem 'bukas' | 85 |
| maglaro | n-gram: rare trigram(s) lar, aro, ro_ in stem 'laro' | 85 |
| parke | n-gram: rare trigram(s) par, ark, rke, ke_ in stem 'parke' | 85 |
| Umuulan | n-gram: rare trigram(s) _ul in stem 'ulan' | 86 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 86 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 87 |
| natatanggap | n-gram: rare trigram(s) tan, ngg, gga, gap, ap_ in stem 'tanggap' | 88 |
| sulat | n-gram: rare trigram(s) _su, sul, lat in stem 'sulat' | 88 |
| kanya | n-gram: rare trigram(s) _ny, nya in stem 'nya' | 88 |
| kanina | n-gram: rare trigram(s) nin in stem 'nina' | 89 |
| Pagod | n-gram: rare trigram(s) _go, god, od_ in stem 'god' | 90 |
| dalawang | n-gram: rare trigram(s) law, wan in stem 'dalawang' | 91 |
| kasaysayan | n-gram: rare trigram(s) say, ays, ysa, say in stem 'saysay' | 91 |
| Masarap | n-gram: rare trigram(s) sar, rap, ap_ in stem 'sarap' | 92 |
| handaan | n-gram: rare trigram(s) han, and, da_ in stem 'handa' | 92 |
| kagabi | n-gram: rare trigram(s) gab, bi_ in stem 'gabi' | 92 |
| sinigang | n-gram: rare trigram(s) sig, iga, gan in stem 'sigang' | 93 |
| amin | n-gram: rare trigram(s) _am in stem 'amin' | 93 |
| Gusto | n-gram: rare trigram(s) _gu, gus, ust, sto in stem 'gusto' | 94 |
| paaralan | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 95 |
| probinsiya | n-gram: rare trigram(s) _pr, pro, rob, obi, bin, ins, nsi, siy in stem 'probinsiya' | 96 |
| Mahilig | n-gram: rare trigram(s) _hi in stem 'hilig' | 97 |
| aklat | n-gram: rare trigram(s) akl, kla, lat in stem 'aklat' | 97 |
| dagat | n-gram: rare trigram(s) dag, gat in stem 'dagat' | 98 |
| tanawin | n-gram: rare trigram(s) tan, naw in stem 'tanaw' | 99 |
| bundok | n-gram: rare trigram(s) bun, und, ndo, dok, ok_ in stem 'bundok' | 99 |
| sampung | n-gram: rare trigram(s) sam, amp, mpu, pun in stem 'sampung' | 100 |
| maaga | n-gram: rare trigram(s) _ag in stem 'aga' | 101 |
| mabuti | n-gram: rare trigram(s) but, uti, ti_ in stem 'buti' | 101 |
| kalusugan | n-gram: rare trigram(s) lus, usu, sug, ug_ in stem 'lusug' | 101 |
| maikling | n-gram: rare trigram(s) _ik, ikl, kli, lin in stem 'ikling' | 102 |
| sanaysay | n-gram: rare trigram(s) san, nay, ays, ysa, say in stem 'sanaysay' | 102 |
| tulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 103 |
| Gusto | n-gram: rare trigram(s) _gu, gus, ust, sto in stem 'gusto' | 104 |
| kong | clitic-split: "ko ng" should be two words | 104 |
| adobo | n-gram: rare trigram(s) _ad, ado, dob, obo, bo_ in stem 'adobo' | 104 |
| mamaya | n-gram: rare trigram(s) _ay in stem 'aya' | 104 |
| mabuti | n-gram: rare trigram(s) but, uti, ti_ in stem 'buti' | 105 |
| pagsusulit | n-gram: rare trigram(s) _su, sul, uli, lit in stem 'sulit' | 105 |
| proyekto | n-gram: rare trigram(s) _pr, pro, roy, oye, yek, ekt, kto in stem 'proyekto' | 106 |
| bagay | n-gram: rare trigram(s) bag in stem 'bagay' | 107 |
| bakuran | n-gram: rare trigram(s) bak, aku, kur, ur_ in stem 'bakur' | 108 |

## False alarms in the held-out clean sentences

| Word | Reason | Sentence |
|---|---|---|
| pagbabago | n-gram: rare trigram(s) bag, ago in stem 'bago' | 1 |
| klima | n-gram: rare trigram(s) _kl, kli, lim, ima in stem 'klima' | 1 |
| hamon | n-gram: rare trigram(s) ham, amo, mon in stem 'hamon' | 1 |
| kinakaharap | n-gram: rare trigram(s) kah, har, rap, ap_ in stem 'kaharap' | 1 |
| ating | n-gram: rare trigram(s) _at, ati, tin in stem 'ating' | 1 |
| henerasyon | n-gram: rare trigram(s) _he, hen, ene, ner, era, ras, asy, syo in stem 'henerasyon' | 1 |
| Nagsagawa | n-gram: rare trigram(s) sag, gaw in stem 'sagawa' | 2 |
| mananaliksik | n-gram: rare trigram(s) nal, lik, iks, ksi, sik, ik_ in stem 'analiksik' | 2 |
| malawakang | n-gram: rare trigram(s) law, wak in stem 'lawakang' | 2 |
| pag-aaral | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 2 |
| tungkol | n-gram: rare trigram(s) tun, ngk, gko, kol, ol_ in stem 'tungkol' | 2 |
| epekto | n-gram: rare trigram(s) _ep, epe, pek, ekt, kto in stem 'epekto' | 2 |
| plastik | n-gram: rare trigram(s) _pl, pla, las, ast, sti, tik, ik_ in stem 'plastik' | 2 |
| karagatan | n-gram: rare trigram(s) _ra, rag, gat in stem 'ragat' | 2 |
| Ipinagdiriwang | n-gram: rare trigram(s) dir, iri, riw, iwa, wan in stem 'diriwang' | 3 |
| Pilipino | n-gram: rare trigram(s) pil, ipi, ino, no_ in stem 'pilipino' | 3 |
| Kalayaan | n-gram: rare trigram(s) lay in stem 'laya' | 3 |
| ikalabindalawa | n-gram: rare trigram(s) lab, bin, ind, law in stem 'labindalawa' | 3 |
| Hunyo | n-gram: rare trigram(s) _hu, hun, uny in stem 'hunyo' | 3 |
| nahihirapang | n-gram: rare trigram(s) _hi, hir, rap, pan in stem 'hirapang' | 4 |
| matrikula | n-gram: rare trigram(s) _tr, tri, rik, iku, kul in stem 'trikula' | 4 |
| presyo | n-gram: rare trigram(s) _pr, pre, res, esy, syo in stem 'presyo' | 4 |
| bilihin | n-gram: rare trigram(s) bil, li_ in stem 'bili' | 4 |
| Kinakailangan | n-gram: rare trigram(s) kai, ail in stem 'kailang' | 5 |
| sumunod | n-gram: rare trigram(s) _su, sun, uno, nod, od_ in stem 'sunod' | 5 |
| alituntunin | n-gram: rare trigram(s) lit, itu, tun, unt, ntu, tu_ in stem 'alituntu' | 5 |
| pamahalaang | n-gram: rare trigram(s) _ah, laa in stem 'ahalaang' | 5 |
| lokal | n-gram: rare trigram(s) _lo, lok, oka in stem 'lokal' | 5 |
| sariling | n-gram: rare trigram(s) sar, ari, ril, lin in stem 'sariling' | 6 |
| pagkain | n-gram: rare trigram(s) kai, ain in stem 'kain' | 6 |
| pamamagitan | n-gram: rare trigram(s) _am, mag, agi, git in stem 'amagit' | 6 |
| Nagtipon-tipon | n-gram: rare trigram(s) tip, ipo, pon in stem 'tipon' | 7 |
| magsasaka | n-gram: rare trigram(s) sak, ka_ in stem 'saka' | 7 |
| upang | n-gram: rare trigram(s) _up, upa, pan in stem 'upang' | 7 |
| pag-usapan | n-gram: rare trigram(s) _us, usa, sap, ap_ in stem 'usap' | 7 |
| problema | n-gram: rare trigram(s) _pr, pro, rob, obl, ble, lem, ema in stem 'problema' | 7 |
| irigasyon | n-gram: rare trigram(s) _ri, rig, iga, gas, asy, syo in stem 'rigasyon' | 7 |
| Pinuri | n-gram: rare trigram(s) pur, uri, ri_ in stem 'puri' | 8 |
| punong-guro | n-gram: rare trigram(s) pun, uno, non, ng-, g-g, -gu, gur, uro, ro_ in stem 'punong-guro' | 8 |
| mag-aaral | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 8 |
| nagwagi | n-gram: rare trigram(s) _wa, wag, agi, gi_ in stem 'wagi' | 8 |
| paligsahan | n-gram: rare trigram(s) igs, gsa in stem 'ligsa' | 8 |
| pagsulat | n-gram: rare trigram(s) _su, sul, lat in stem 'sulat' | 8 |
| sanaysay | n-gram: rare trigram(s) san, nay, ays, ysa, say in stem 'sanaysay' | 8 |
| Lumikas | n-gram: rare trigram(s) lik, ika, kas in stem 'likas' | 9 |
| residente | n-gram: rare trigram(s) _re, res, esi, sid, ide, den, ent, nte, te_ in stem 'residente' | 9 |
| mas | n-gram: rare trigram(s) mas in stem 'mas' | 9 |
| lumakas | n-gram: rare trigram(s) kas in stem 'lakas' | 9 |
| bagyo | n-gram: rare trigram(s) bag, agy, gyo in stem 'bagyo' | 9 |
| eksperto | n-gram: rare trigram(s) _ek, eks, ksp, spe, per, ert, rto in stem 'eksperto' | 10 |
| sapat | n-gram: rare trigram(s) sap in stem 'sapat' | 10 |
| tulog | n-gram: rare trigram(s) tul, ulo, log, og_ in stem 'tulog' | 10 |
| kalusugan | n-gram: rare trigram(s) lus, usu, sug, ug_ in stem 'lusug' | 10 |
| tanghalian | n-gram: rare trigram(s) tan, ngh, gha, li_ in stem 'tanghali' | 11 |
| kanina | n-gram: rare trigram(s) nin in stem 'nina' | 11 |
| sinigang | n-gram: rare trigram(s) sig, iga, gan in stem 'sigang' | 11 |
| hipon | n-gram: rare trigram(s) _hi, hip, ipo, pon in stem 'hipon' | 11 |
| pritong | n-gram: rare trigram(s) _pr, pri, rit, ton in stem 'pritong' | 11 |
| isda | n-gram: rare trigram(s) isd, sda, da_ in stem 'isda' | 11 |
| tulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 12 |
| organisasyon | n-gram: rare trigram(s) _or, org, rga, gan, nis, isa, sas, asy, syo in stem 'organisasyon' | 12 |
| nasalanta | n-gram: rare trigram(s) sal, ant, nta in stem 'salanta' | 12 |
| lindol | n-gram: rare trigram(s) lin, ind, ndo, dol, ol_ in stem 'lindol' | 12 |
| Hinihikayat | n-gram: rare trigram(s) _hi, hik, ika, yat in stem 'hikayat' | 13 |
| paaralan | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 13 |
| magulang | n-gram: rare trigram(s) _ul in stem 'ulang' | 13 |
| makilahok | n-gram: rare trigram(s) lah, aho, hok, ok_ in stem 'lahok' | 13 |
| Natuklasan | n-gram: rare trigram(s) tuk, ukl, kla, las in stem 'tuklas' | 14 |
| siyentipiko | n-gram: rare trigram(s) siy, iye, yen, ent, nti, tip, ipi, pik, iko in stem 'siyentipiko' | 14 |
| bagong | clitic-split: "bago ng" should be two words | 14 |
| palaka | n-gram: rare trigram(s) ka_ in stem 'laka' | 14 |
| kagubatan | n-gram: rare trigram(s) _gu, gub, uba in stem 'gubat' | 14 |
| Palawan | n-gram: rare trigram(s) law in stem 'law' | 14 |
| wikang | n-gram: rare trigram(s) _wi, wik, ika in stem 'wikang' | 15 |
| Filipino | n-gram: rare trigram(s) _fi, fil, ipi, ino, no_ in stem 'filipino' | 15 |
| patuloy | n-gram: rare trigram(s) tul, ulo, loy, oy_ in stem 'tuloy' | 15 |
| umuunlad | n-gram: rare trigram(s) _un, unl, nla, lad, ad_ in stem 'unlad' | 15 |
| paghiram | n-gram: rare trigram(s) _hi, hir, ram, am_ in stem 'hiram' | 15 |
| salita | n-gram: rare trigram(s) sal, lit, ita in stem 'salita' | 15 |
| wika | n-gram: rare trigram(s) _wi, wik, ika, ka_ in stem 'wika' | 15 |
| panahon | n-gram: rare trigram(s) _ah, aho, hon in stem 'ahon' | 16 |
| tag-ulan | n-gram: rare trigram(s) tag, ag-, g-u, -ul in stem 'tag-ulan' | 16 |
| madalas | n-gram: rare trigram(s) las in stem 'dalas' | 16 |
| bumaha | n-gram: rare trigram(s) bah, ha_ in stem 'baha' | 16 |
| bahagi | n-gram: rare trigram(s) bah, hag, agi, gi_ in stem 'bahagi' | 16 |
| bagong | clitic-split: "bago ng" should be two words | 17 |
| matuto | n-gram: rare trigram(s) tut, uto in stem 'tuto' | 17 |
| wika | n-gram: rare trigram(s) _wi, wik, ika, ka_ in stem 'wika' | 17 |
| Pinaghandaan | n-gram: rare trigram(s) han, and, da_ in stem 'handa' | 18 |
| koponan | n-gram: rare trigram(s) kop, opo, po_ in stem 'kopo' | 18 |
| laban | n-gram: rare trigram(s) lab, ab_ in stem 'lab' | 18 |
| kampeonato | n-gram: rare trigram(s) amp, mpe, peo, eon, ona, nat, ato in stem 'kampeonato' | 18 |
| buwan | n-gram: rare trigram(s) buw, uw_ in stem 'buw' | 18 |
| Tumutulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 19 |
| boluntaryo | n-gram: rare trigram(s) _bo, bol, olu, lun, unt, nta, tar, ary, ryo in stem 'boluntaryo' | 19 |
| paglilinis | n-gram: rare trigram(s) lin, ini, nis, is_ in stem 'linis' | 19 |
| dalampasigan | n-gram: rare trigram(s) amp, mpa, pas, asi, sig in stem 'dalampasig' | 19 |
| Napansin | n-gram: rare trigram(s) pan, ans, ns_ in stem 'pans' | 20 |
| guro | n-gram: rare trigram(s) _gu, gur, uro, ro_ in stem 'guro' | 20 |
| nakikinig | n-gram: rare trigram(s) nig in stem 'nig' | 20 |
| habang | n-gram: rare trigram(s) hab in stem 'habang' | 20 |
| nagtuturo | n-gram: rare trigram(s) tur, uro, ro_ in stem 'turo' | 20 |
| aklat | n-gram: rare trigram(s) akl, kla, lat in stem 'aklat' | 21 |
| nakatutulong | n-gram: rare trigram(s) tul, ulo, lon in stem 'tulong' | 21 |
| pagpapalawak | n-gram: rare trigram(s) pal, law, wak in stem 'palawak' | 21 |
| bokabularyo | n-gram: rare trigram(s) _bo, bok, oka, kab, abu, lar, ary, ryo in stem 'bokabularyo' | 21 |
| Ipinaliwanag | n-gram: rare trigram(s) liw, iwa, wan, ag_ in stem 'liwanag' | 22 |
| doktor | n-gram: rare trigram(s) _do, dok, okt, kto, tor, or_ in stem 'doktor' | 22 |
| sintomas | n-gram: rare trigram(s) sin, int, nto, tom, oma, mas in stem 'sintomas' | 22 |
| dengue | n-gram: rare trigram(s) _de, den, eng, ngu, gue, ue_ in stem 'dengue' | 22 |
| paano | clitic-split: "pa ano" should be two words | 22 |
| maiiwasan | n-gram: rare trigram(s) _iw, iwa, was in stem 'iwas' | 22 |
| Nagbukas | n-gram: rare trigram(s) buk, uka, kas in stem 'bukas' | 23 |
| bagong | clitic-split: "bago ng" should be two words | 23 |
| silid-aklatan | n-gram: rare trigram(s) sil, lid, id-, d-a, -ak, akl, kla, lat, ata, tan in stem 'silid-aklatan' | 23 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 23 |
| barangay | n-gram: rare trigram(s) bar, ran, nga in stem 'barangay' | 23 |
| noong | n-gram: rare trigram(s) _no, noo, oon in stem 'noong' | 23 |
| buwan | n-gram: rare trigram(s) buw, uw_ in stem 'buw' | 23 |
| Kailangang | n-gram: rare trigram(s) nga, gan in stem 'ilangang' | 24 |
| helmet | n-gram: rare trigram(s) _he, hel, elm, lme, met, et_ in stem 'helmet' | 24 |
| nagmamaneho | n-gram: rare trigram(s) man, ane, neh, eho, ho_ in stem 'maneho' | 24 |
| motorsiklo | n-gram: rare trigram(s) _mo, mot, oto, tor, ors, rsi, sik, ikl, klo, lo_ in stem 'motorsiklo' | 24 |
| mahilig | n-gram: rare trigram(s) _hi in stem 'hilig' | 25 |
| larawan | n-gram: rare trigram(s) lar, raw in stem 'laraw' | 25 |
| social | n-gram: rare trigram(s) _so, soc, oci, cia, ial in stem 'social' | 25 |
| media | n-gram: rare trigram(s) _me, med, edi, dia, ia_ in stem 'media' | 25 |
| Nagluluksa | n-gram: rare trigram(s) luk, uks, ksa in stem 'luksa' | 26 |
| pagpanaw | n-gram: rare trigram(s) naw in stem 'naw' | 26 |
| minamahal | n-gram: rare trigram(s) mah in stem 'mahal' | 26 |
| alkalde | n-gram: rare trigram(s) alk, lka, ald, lde, de_ in stem 'alkalde' | 26 |
| Sumikat | n-gram: rare trigram(s) sik, ika, kat in stem 'sikat' | 27 |
| likod | n-gram: rare trigram(s) lik, iko, kod, od_ in stem 'likod' | 27 |
| bundok | n-gram: rare trigram(s) bun, und, ndo, dok, ok_ in stem 'bundok' | 27 |
| habang | n-gram: rare trigram(s) hab in stem 'habang' | 27 |
| naglalakad | n-gram: rare trigram(s) kad, ad_ in stem 'lakad' | 27 |
| pauwi | n-gram: rare trigram(s) _uw, uwi, wi_ in stem 'uwi' | 27 |
| Mas | n-gram: rare trigram(s) mas in stem 'mas' | 28 |
| pinipili | n-gram: rare trigram(s) pil, li_ in stem 'pili' | 28 |
| mamimili | n-gram: rare trigram(s) _im, imi, mil, li_ in stem 'imili' | 28 |
| produktong | n-gram: rare trigram(s) _pr, pro, rod, odu, duk, ukt, kto, ton in stem 'produktong' | 28 |
| sariling | n-gram: rare trigram(s) sar, ari, ril, lin in stem 'sariling' | 28 |
| Binigyang-diin | n-gram: rare trigram(s) bin, ini, nig, igy, gya, ng-, g-d, -di, dii, iin in stem 'binigyang-diin' | 29 |
| tagapagsalita | n-gram: rare trigram(s) pag, ags, gsa, sal, lit, ita in stem 'pagsalita' | 29 |
| edukasyon | n-gram: rare trigram(s) _ed, edu, duk, uka, kas, asy, syo in stem 'edukasyon' | 29 |
| pag-unlad | n-gram: rare trigram(s) _un, unl, nla, lad, ad_ in stem 'unlad' | 29 |
| darating | n-gram: rare trigram(s) dar, rat, ati, tin in stem 'darating' | 30 |
| magtanghali | n-gram: rare trigram(s) tan, ngh, gha, li_ in stem 'tanghali' | 30 |
| aming | n-gram: rare trigram(s) _am in stem 'aming' | 31 |
| lola | n-gram: rare trigram(s) _lo, lol, ola in stem 'lola' | 31 |
| mahusay | n-gram: rare trigram(s) _hu, hus, usa, say in stem 'husay' | 31 |
| magluto | n-gram: rare trigram(s) lut, uto in stem 'luto' | 31 |
| kakaning | n-gram: rare trigram(s) nin in stem 'kaning' | 31 |
| bibingka | n-gram: rare trigram(s) bin, ngk, gka, ka_ in stem 'bingka' | 31 |
| puto | n-gram: rare trigram(s) put, uto in stem 'puto' | 31 |
| Nagkasundo | n-gram: rare trigram(s) _su, sun, und, ndo, do_ in stem 'sundo' | 32 |
| dalawang | n-gram: rare trigram(s) law, wan in stem 'dalawang' | 32 |
| panig | n-gram: rare trigram(s) nig in stem 'nig' | 32 |
| ipagpatuloy | n-gram: rare trigram(s) atu, tul, ulo, loy, oy_ in stem 'patuloy' | 32 |
| negosasyon | n-gram: rare trigram(s) _ne, neg, ego, gos, osa, sas, asy, syo in stem 'negosasyon' | 32 |
| susunod | n-gram: rare trigram(s) _su, sun, uno, nod, od_ in stem 'sunod' | 32 |
| linggo | n-gram: rare trigram(s) lin, ngg, ggo in stem 'linggo' | 32 |
| saan-saan | n-gram: rare trigram(s) saa in stem 'saan' | 33 |
| basurang | n-gram: rare trigram(s) bas, asu, sur, ura, ran in stem 'basurang' | 33 |
| plastik | n-gram: rare trigram(s) _pl, pla, las, ast, sti, tik, ik_ in stem 'plastik' | 33 |
| mangingisda | n-gram: rare trigram(s) ngi, gis, isd, sda, da_ in stem 'ingisda' | 34 |
| maagang | n-gram: rare trigram(s) _ag, gan in stem 'agang' | 34 |
| pumapalaot | n-gram: rare trigram(s) pal, lao, aot in stem 'palaot' | 34 |
| upang | n-gram: rare trigram(s) _up, upa, pan in stem 'upang' | 34 |
| makahuli | n-gram: rare trigram(s) _hu, hul, uli, li_ in stem 'huli' | 34 |
| isda | n-gram: rare trigram(s) isd, sda, da_ in stem 'isda' | 34 |
| Pinag-aaralan | n-gram: rare trigram(s) _ar, ral in stem 'aral' | 35 |
| eksperto | n-gram: rare trigram(s) _ek, eks, ksp, spe, per, ert, rto in stem 'eksperto' | 35 |
| ligtas | n-gram: rare trigram(s) igt, gta, tas in stem 'ligtas' | 35 |
| bagong | clitic-split: "bago ng" should be two words | 35 |
| bakuna | n-gram: rare trigram(s) bak, aku, kun, una in stem 'bakuna' | 35 |
| bakit | n-gram: rare trigram(s) bak in stem 'bakit' | 36 |
| langit | n-gram: rare trigram(s) ngi, git in stem 'langit' | 36 |
| Isinulat | n-gram: rare trigram(s) _su, sul, lat in stem 'sulat' | 37 |
| Jose | n-gram: rare trigram(s) _jo, jos, ose, se_ in stem 'jose' | 37 |
| Rizal | n-gram: rare trigram(s) _ri, riz, iza, zal in stem 'rizal' | 37 |
| Noli | n-gram: rare trigram(s) _no, nol, oli, li_ in stem 'noli' | 37 |
| Tangere | n-gram: rare trigram(s) tan, nge, ger, ere, re_ in stem 'tangere' | 37 |
| upang | n-gram: rare trigram(s) _up, upa, pan in stem 'upang' | 37 |
| ilantad | n-gram: rare trigram(s) ant, nta, tad, ad_ in stem 'lantad' | 37 |
| pang-aabuso | n-gram: rare trigram(s) _ab, abu, bus, uso, so_ in stem 'abuso' | 37 |
| prayle | n-gram: rare trigram(s) _pr, pra, ray, ayl, yle, le_ in stem 'prayle' | 37 |
| Masayang | n-gram: rare trigram(s) say in stem 'sayang' | 38 |
| nagkuwentuhan | n-gram: rare trigram(s) kuw, uwe, wen, ent, ntu, tu_ in stem 'kuwentu' | 38 |
| magkakaibigan | n-gram: rare trigram(s) kai, aib, ibi in stem 'kaibig' | 38 |
| habang | n-gram: rare trigram(s) hab in stem 'habang' | 38 |
| umiinom | n-gram: rare trigram(s) ino, nom, om_ in stem 'inom' | 38 |
| kape | n-gram: rare trigram(s) kap, ape, pe_ in stem 'kape' | 38 |
| klase | n-gram: rare trigram(s) _kl, kla, las, ase, se_ in stem 'klase' | 39 |
| pangkat | n-gram: rare trigram(s) kat in stem 'kat' | 39 |
| proyekto | n-gram: rare trigram(s) _pr, pro, roy, oye, yek, ekt, kto in stem 'proyekto' | 39 |
| agham | n-gram: rare trigram(s) _ag, agh, gha, ham, am_ in stem 'agham' | 39 |
| pag-iipon | n-gram: rare trigram(s) _ip, ipo, pon in stem 'ipon' | 40 |
| pera | n-gram: rare trigram(s) _pe, per, era in stem 'pera' | 40 |
| mabuting | n-gram: rare trigram(s) but, uti, tin in stem 'buting' | 40 |
| gawi | n-gram: rare trigram(s) gaw, awi, wi_ in stem 'gawi' | 40 |
| simulan | n-gram: rare trigram(s) sim, imu, ul_ in stem 'simul' | 40 |
| habang | n-gram: rare trigram(s) hab in stem 'habang' | 40 |

## Detected, but the intended correction was not suggested

| Incorrect | Intended | Suggestions |
|---|---|---|
| pagka't | pagkat | (none) |
| naglalarro | naglalaro | (none) |
| isdaa | isda | isa, isla |
| kaibigaan | kaibigan | (none) |
| tumakbbo | tumakbo | (none) |
| sanaysayy | sanaysay | (none) |
| nagtuturro | nagtuturo | (none) |
| Tnago | Itinago | Bago, Tagpo, Tayo, Tungo, Tao |
| mganda | maganda | (none) |
| Pumnta | Pumunta | Punta |
| tlong | tulong | ilong, taong, tanong, mong, akong, anong, itong, talon |
| hpunan | hapunan | (none) |
| paralan | paaralan | (none) |
| pgkain | pagkain | (none) |
| alamt | alamat | alam, alamin, salamat, alaga, apat |
| bkid | bukid | bukod, akin |
| edkasyon | edukasyon | (none) |
| pamlya | pamilya | (none) |
| nagtatrbaho | nagtatrabaho | (none) |
| maintindhan | maintindihan | (none) |
| klse | klase | kasi, ale |
| lham | liham | alam, lahat |
| binli | binili | bigla, hindi |
| tanwin | tanawin | tingin, tangi |
| lumilipd | lumilipad | (none) |
| nakapnta | nakapunta | nakakita |
| kpatid | kapatid | (none) |
| kalikasn | kalikasan | (none) |
| pasalbong | pasalubong | (none) |
| Meron | Mayroon | Mayon, Pero |
| magamda | maganda | (none) |
| Kumaim | Kumain | (none) |
| Bakot | Bakit | Bawat, Ako, Abot, Bago, Bato, Bikol, Bukod, Sakit |
| aklar | aklat | alam, akyat |
| pamikya | pamilya | (none) |
| Masaua | Masaya | Kasama, Mahaba, Pasada |
| pagsusulot | pagsusulit | (none) |
| kaigigan | kaibigan | (none) |
| mabute | mabuti | (none) |
| gusako | gusali | (none) |
| duyab | duyan | (none) |
| simbahab | simbahan | (none) |
| lumalanhoy | lumalangoy | (none) |
| sinogang | sinigang | (none) |
| umiiyal | umiiyak | (none) |
| manunulag | manunulat | (none) |
| aklatam | aklatan | (none) |
| kagabu | kagabi | katabi |
| hamgganan | hangganan | (none) |
| hamgin | hangin | namin |
| inhinyeto | inhinyero | (none) |
| kalabay | kalabaw | kasakay |
| ngupin | ngipin | (none) |
| dahom | dahon | dahil, daloy |
| pagsisulit | pagsusulit | (none) |
| bayabi | bayani | bayad, katabi |
| kapitbahat | kapitbahay | (none) |
| napakainot | napakainit | (none) |
| Kayapala | Kaya pala | (none) |
| magka-ugnay | magkaugnay | (none) |
| pag-kain | pagkain | (none) |
| Nag-luto | Nagluto | (none) |
| mag-laro | maglaro | (none) |
| Nag-lakad | Naglakad | (none) |
| ka-ibigan | kaibigan | (none) |
| Napaka-ganda | Napakaganda | (none) |
| Nag-trabaho | Nagtrabaho | (none) |
| pag-tulog | pagtulog | (none) |
| Mag-sulat | Magsulat | (none) |
