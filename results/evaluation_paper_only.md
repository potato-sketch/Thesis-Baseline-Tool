# Evaluation of the Filipino spell checker (Tagalog: both word list, English: ud word list)

100 test sentences, n-gram threshold 0.20, paper-only pipeline.

| Metric | Test sentences | + held-out clean sentences | Paper |
|---|---|---|---|
| Recall | 87.00% | 87.00% | 81% |
| Precision | 100.00% | 64.44% | 53.64% |
| F-measure | 93.05% | 74.04% | 64.53% |
| Suggestion adequacy | 91.95% | 91.95% | 87.78% |
| Correct word ranked first | 81.61% | 81.61% | not reported |

TP = 87, FN = 13, FP = 0 in the test sentences, plus 48 false alarm(s) in 40 clean sentences (478 words).

## Results per error type (Table I categories)

| Error type | Count | Detected | Correct word suggested |
|---|---|---|---|
| insertion | 8 | 8 | 7 |
| deletion | 28 | 27 | 25 |
| substitution | 37 | 34 | 30 |
| space deletion | 9 | 4 | 4 |
| hyphen insertion | 12 | 12 | 12 |
| space insertion | 6 | 2 | 2 |

## False negatives (errors that were not flagged)

| Incorrect | Correct | Accepted by |
|---|---|---|
| maintindhan | maintindihan | stemmed-dictionary (stem: intindi) |
| asil | asul | n-gram (all trigrams of 'asil' are frequent) |
| kalabay | kalabaw | n-gram (all trigrams of 'labay' are frequent) |
| napakainot | napakainit | stemmed-dictionary (stem: not) |
| parin | pa rin | stemmed-dictionary (stem: pad) |
| kana | ka na | n-gram (all trigrams of 'kana' are frequent) |
| palang | pa lang | stemmed-dictionary (stem: pal) |
| nalang | na lang | n-gram (all trigrams of 'lang' are frequent) |
| nanaman | na naman | stemmed-dictionary (stem: ban) |
| pag bigay | pagbigay | n-gram (all trigrams of 'pag' are frequent) |
| Nag aral | Nag-aral | dictionary |
| pinag usapan | pinag-usapan | n-gram (all trigrams of 'pag' are frequent) |
| Nag lalaro | Naglalaro | dictionary |

## False positives in the test sentences

| Word | Reason | Line |
|---|---|---|

## False alarms in the held-out clean sentences

| Word | Reason | Sentence |
|---|---|---|
| hamon | n-gram: rare trigram(s) ham, mon in stem 'hamon' | 1 |
| henerasyon | n-gram: rare trigram(s) _he, hen, ene, ner, era, ras in stem 'henerasyon' | 1 |
| Nagsagawa | n-gram: rare trigram(s) sag, gaw in stem 'sagawa' | 2 |
| mananaliksik | n-gram: rare trigram(s) nal, iks, ksi in stem 'analiksik' | 2 |
| karagatan | n-gram: rare trigram(s) _ra, rag in stem 'ragat' | 2 |
| Ipinagdiriwang | n-gram: rare trigram(s) dir, iri, riw in stem 'diriwang' | 3 |
| matrikula | n-gram: rare trigram(s) _tr, tri, rik, iku in stem 'trikula' | 4 |
| alituntunin | n-gram: rare trigram(s) itu, tun, unt, ntu, tu_ in stem 'alituntu' | 5 |
| lokal | n-gram: rare trigram(s) _lo, lok, oka in stem 'lokal' | 5 |
| photosynthesis | n-gram: rare trigram(s) _ph, pho, hot, oto, tos, osy, syn, ynt, nth, the, hes, esi, sis in stem 'photosynthesis' | 6 |
| Nagtipon-tipon | n-gram: rare trigram(s) tip, ipo in stem 'tipon' | 7 |
| irigasyon | n-gram: rare trigram(s) _ri, rig, gas in stem 'rigasyon' | 7 |
| Pinuri | n-gram: rare trigram(s) pur, uri, ri_ in stem 'puri' | 8 |
| punong-guro | n-gram: rare trigram(s) pun, uno, non, ng-, g-g, -gu, gur, uro in stem 'punong-guro' | 8 |
| nagwagi | n-gram: rare trigram(s) _wa, wag, gi_ in stem 'wagi' | 8 |
| paligsahan | n-gram: rare trigram(s) igs, gsa in stem 'ligsa' | 8 |
| residente | n-gram: rare trigram(s) res, esi, sid, ide, den in stem 'residente' | 9 |
| eksperto | n-gram: rare trigram(s) _ek, eks, ksp, spe, per, ert, rto in stem 'eksperto' | 10 |
| organisasyon | n-gram: rare trigram(s) _or, org, rga, nis, sas in stem 'organisasyon' | 12 |
| Hinihikayat | n-gram: rare trigram(s) hik, yat in stem 'hikayat' | 13 |
| makilahok | n-gram: rare trigram(s) lah, hok in stem 'lahok' | 13 |
| siyentipiko | n-gram: rare trigram(s) iye, yen, tip, pik, iko in stem 'siyentipiko' | 14 |
| umuunlad | n-gram: rare trigram(s) unl, nla, lad in stem 'unlad' | 15 |
| tag-ulan | n-gram: rare trigram(s) tag, ag-, g-u, -ul in stem 'tag-ulan' | 16 |
| koponan | n-gram: rare trigram(s) kop, opo in stem 'kopo' | 18 |
| kampeonato | n-gram: rare trigram(s) mpe, peo, eon, ona, nat in stem 'kampeonato' | 18 |
| boluntaryo | n-gram: rare trigram(s) _bo, bol, olu, unt, tar, ary, ryo in stem 'boluntaryo' | 19 |
| bokabularyo | n-gram: rare trigram(s) _bo, bok, oka, kab, abu, bul, lar, ary, ryo in stem 'bokabularyo' | 21 |
| sintomas | n-gram: rare trigram(s) tom, oma, mas in stem 'sintomas' | 22 |
| dengue | n-gram: rare trigram(s) _de, den, eng, ngu, gue, ue_ in stem 'dengue' | 22 |
| helmet | n-gram: rare trigram(s) _he, hel, elm, lme, met, et_ in stem 'helmet' | 24 |
| motorsiklo | n-gram: rare trigram(s) _mo, mot, oto, tor, ors, rsi, ikl, klo in stem 'motorsiklo' | 24 |
| Nagluluksa | n-gram: rare trigram(s) luk, uks, ksa in stem 'luksa' | 26 |
| Binigyang-diin | n-gram: rare trigram(s) nig, igy, gya, ng-, g-d, -di, dii, iin in stem 'binigyang-diin' | 29 |
| negosasyon | n-gram: rare trigram(s) _ne, neg, ego, gos, osa, sas in stem 'negosasyon' | 32 |
| pumapalaot | n-gram: rare trigram(s) lao, aot in stem 'palaot' | 34 |
| eksperto | n-gram: rare trigram(s) _ek, eks, ksp, spe, per, ert, rto in stem 'eksperto' | 35 |
| ligtas | n-gram: rare trigram(s) igt, gta in stem 'ligtas' | 35 |
| bakuna | n-gram: rare trigram(s) bak, aku, kun in stem 'bakuna' | 35 |
| Jose | n-gram: rare trigram(s) _jo, jos, ose, se_ in stem 'jose' | 37 |
| Rizal | n-gram: rare trigram(s) _ri, riz, iza, zal in stem 'rizal' | 37 |
| Noli | n-gram: rare trigram(s) nol, oli in stem 'noli' | 37 |
| Tangere | n-gram: rare trigram(s) nge, ger, ere, re_ in stem 'tangere' | 37 |
| ilantad | n-gram: rare trigram(s) tad in stem 'lantad' | 37 |
| pang-aabuso | n-gram: rare trigram(s) _ab, abu, bus, uso in stem 'abuso' | 37 |
| prayle | n-gram: rare trigram(s) pra, ray, ayl, yle, le_ in stem 'prayle' | 37 |
| pag-iipon | n-gram: rare trigram(s) _ip, ipo in stem 'ipon' | 40 |
| gawi | n-gram: rare trigram(s) gaw, wi_ in stem 'gawi' | 40 |

## Detected, but the intended correction was not suggested

| Incorrect | Intended | Suggestions |
|---|---|---|
| bahaay | bahay | baha ay |
| psahero | pasahero | psa hero |
| tanwin | tanawin | tan win |
| Meron | Mayroon | Mayon, Pero |
| salanat | salamat | sala nat |
| sinogang | sinigang | sino gang |
| aklatam | aklatan | aklat am |
