__author__ = 'Pontus'
from sklearn import svm
import numpy as np
import wk
import ngk
import util
import gram

docs = []
docs.append("jag ska ga bort")
docs.append("du ska ga hem nu")
docs.append("ska du ga bort")
docs.append("us supplydemand detailed usda us agriculture department made following supplydemand projections 198687 seasons mln bushels comparisons unless noted corn 198687 198586 040987 030987 040987 030987 acreage mln acres planted 767 767 834 834 harvested 692 692 752 752 yield bu 1193 1193 1180 1180 supply mln bu start stock 4040 4040 1648 1648 production 8253 8253 8877 8877 totalx 12295 12295 10536 10536 xincludes imports corn cont 198687 198586 040987 030987 040987 030987 usage feed 4500 4300 4095 4126 1180 1150 1160 1129 ttl domest 5680 5450 5255 5255 exports 1375 1250 1241 1241 total use 7055 6700 6496 6496 end stocks 5240 5595 4040 4040 farmer reser 1400 1300 564 564 ccc stocks 1700 1500 546 546 free stocks 2140 2795 2930 2930 avgprice 135165 135165 223 223 note price dlrs per bu corn season begins sept 1 wheat 198687 198586 040987 030987 040987 030987 acreage mln acres planted 720 720 756 756 harvested 607 607 647 647 yield 344 344 375 375 supply mln bu start stcks 1905 1905 1425 1425 production 2087 2087 2425 2425 total supplyx 4007 4007 3865 3865 x includes imports wheat 198687 198586 cont 040987 030987 040987 030987 usage food 700 690 678 678 seed 84 90 93 93 feed 350 325 274 274 ttl domest 1134 1105 1045 1045 exports 1025 1025 915 915 total use 2159 2130 1960 1960 end stocks 1848 1877 1905 1905 farmer reser 475 450 433 433 ccc stocks 950 950 602 602 free stocks 423 477 870 870 avg price 23040 23040 308 308 note price dlrs per bushel wheat season begins june 1 soybeans 198687 198586 040987 030987 040987 030987 acreage mln acres planted 615 615 631 611 harvested 594 594 616 616 yield bu 338 338 341 341 supply mln bu start stocks 536 536 316 316 production 2007 2007 2099 2099 total 2543 2543 2415 2415 soybeans cont 198687 198586 040987 030987 040987 030987 usage crushings 1130 1115 1053 1053 exports 700 700 740 740 seed feed residual 103 93 86 86 total use 1933 1908 1879 1879 end stocks 610 635 536 536 avg price 460480 460480 505 505 note average price dlrs per bushel soybean season begins june 1 feedgrains x 198687 198586 040987 030987 040987 030987 acreage mln acres planted 1198 1198 1281 1281 harvested 1020 1020 1118 1118 yld tonnes 248 248 245 245 supply mln tonnes start stocks 1264 1264 575 575 production 2524 2524 2744 2744 imports 06 06 09 09 total 3794 3794 3327 3327 x includes corn sorghum barley oats feedgrains x cont 198687 198586 040987 030987 040987 030987 usage feed 1406 1362 1348 1355 358 350 350 343 ttl domest 1764 1712 1698 1698 exports 439 408 366 366 total use 2203 2119 2064 2064 end stocks 1591 1675 1264 1264 farmer reser 390 365 166 166 ccc stocks 552 495 204 204 free stocks 648 815 893 893 x includes corn sorghum oats barley seasons oats barley began june 1 corn sorghum sept 1 soybean oil 198687 198586 040987 030987 040987 030987 supply mln lbs start stcks 947 947 632 632 production 12263 12103 11617 11617 imports nil nil 8 8 total 13210 13050 12257 12257 note 198586 production estimates based october year crush 1060 mln bushels soybean oil cont 198687 198586 040987 030987 040987 030987 usage mln lbs domestic 10500 10500 10053 10053 exports 1350 1350 1257 1257 total 11850 11850 11310 11310 end stcks 1360 1200 947 947 avgprice 145160 150170 1800 1800 note average price cents per lb season soybean oil begins oct 1 soybean cakemeal thousand short tons 198687 198586 040987 030987 040987 030987 start stcks 212 212 387 387 production 26558 26203 24951 24951 total 26770 26415 25338 25338 note 198586 production estimates based october year crush 1060 mln bushels soy cakemeal cont 198687 198586 040987 030987 040987 030987 usage thous short tons domestic 20000 19750 19090 19118 exports 6500 6350 6036 6008 total 26500 26100 25126 25126 end stcks 270 315 212 212 avgprice 145150 145150 15490 15490 note price dlrs per short ton season soybean cake meal begins oct 1 cotton 198687 198586 040987 030987 040987 030987 area mln acres planted 1006 1006 1068 1068 harvested 849 849 1023 1023 yield lbs 549 553 630 630 supply mln 480lb bales start stksx 935 935 410 410 production 970 979 1343 1343 ttl supplyy 1906 1914 1757 1757 x based census bureau data y includes imports cotton cont 198687 198586 040987 030987 040987 030987 usage domestic 710 701 640 640 exports 666 676 196 196 total 1376 1377 836 836 end stocks 540 549 935 935 avge price 517x 517x 5650 5650 x 198687 price weighted average first five months marketing year projection 198687 average price cents per lb cotton season begins august 1 rice 198687 198586 040987 030987 040987 030987 acreage mln acres planted 240 240 251 251 harvested 238 238 249 249 yield lbs 5648 5648 5414 5414 supply mln cwts start stcks 773 773 647 647 production 1344 1344 1349 1349 imports 22 22 22 22 total 2139 2139 2018 2018 rice cont 198687 198586 040987 030987 040987 030987 usage mln cwts domestic 670 670 658 658 exports 800 800 587 587 totaly 1470 1470 1245 1245 end stocks 669 669 773 773 ccc stocks 429 429 415 415 free stocks 240 240 358 358 avgprice 345425 345425 653 653 note average price dlrs per cwt yrough equivalent nanot available usda revising price definition due marketing loan rice season begins august 1 sorghum 198687 198586 040987 030987 040987 030987 yield bu 677 677 668 668 supply mln bu start stcks 551 551 300 300 production 942 942 1120 1120 total 1493 1493 1420 1420 usage mln bu feed 550 575 662 662 30 30 29 29 ttl domest 580 605 691 691 sorghum cont 198687 198586 040987 030987 040987 030987 exports 225 225 178 178 total use 805 830 869 869 end stocks 688 663 551 551 avge price 13050 13050 193 193 note price dlrs per bushel sorghum season begins sept 1 barley 198687 198586 040987 030987 040987 030987 yield bu 508 508 510 510 start stocks 325 325 247 247 production 610 610 591 591 imports 5 5 9 9 total 941 941 847 847 barley cont 198687 198586 040987 031587 040987 031587 usage mln bu feed 300 300 333 333 175 175 167 167 ttl domest 475 475 500 500 exports 150 150 22 22 total use 625 625 522 522 end stocks 316 316 325 325 avgprice 14565 14565 198 198 note average price dlrs per bushel barley season begins june 1 oats mln bushels 198687 198586 040987 030987 040987 030987 yield bu 560 560 637 637 start stcks 184 184 180 180 production 385 385 521 521 imports 30 30 28 28 total 598 598 729 729 oats mln bushels cont 198687 198586 040987 030987 040987 030987 usage feed 400 400 460 460 85 85 83 83 ttl domes 485 485 543 543 exports 2 2 2 2 total 487 487 545 545 end stcks 111 111 184 184 avgprice 10020 10020 123 123 note average price dlrs per bushel oats season begins june 1 long grain rice mln cwts 100 lbs 198687 198586 040987 030987 040987 030987 harvested acres mln 183 183 194 194 yield lbs 5358 5358 5168 5168 start stks 493 493 377 377 production 978 978 1004 1004 ttl supply 1486 1486 1401 1401 note starting stocks include broken kernels supply minus use equal ending stocks breakdowns total supply includes imports broken kernels long grain rice mln cwts 100 lbs cont 198687 198586 040987 030987 040987 030987 domestic use 430 430 488 488 exports 650 600 420 420 total use 1080 1030 908 908 end stocksx 406 456 493 493 avgpric 345425 345424 686 686 note average price dlrs per cwt xbroken kernels included supply minus use equal ending stocks breakdowns rice season begins august 1 medium short grain rice mln cwts 100 lbs 198687 198586 040987 030987 040987 030987 harvested acres mln 055 055 055 055 yield lbs 6651 6651 6258 6258 start stks 267 267 257 257 production 366 366 345 345 ttl supply 653 653 617 617 note starting stocks include broken kernels supply minus use equal ending stocks breakdowns total supply includes imports broken kernels medium short grain rice mln cwts 100 lbs cont 198687 198586 040987 030987 040987 030987 domestic use 240 240 170 170 exports 150 200 167 167 total use 390 440 337 337 end stocksx 245 195 267 267 avgpric 345425 345425 591 591 note average price dlrs per cwt xbroken kernels included supply minus use equal ending stocks breakdowns rice season begins august 1 notes us supplydemand tables na available totals may add due rounding figures 198687 midpoint usda range feed usage corn wheat soybean feedgrains sorghum barley oats includes residual amount residual amount included rice mediumshort grain rice domestic usage rice long grain mediumshort grain rice average price 198586 estimates 198687 projections market prices exclude cash retained marketing loan since april 1986 reuter")
docs.append("jag ska bort")
npdocs = np.array(docs)

#Doc classes
doctypes = np.array([0, 1, 0, 2, 0])

train_docs = npdocs[:4]
test_docs = npdocs[4:]

y_train = doctypes[:4]
y_test = doctypes[4:]

print ""
print "---wk---"
print ""

kernel = wk.wk(wk.get_idf(docs))

train_g = gram.gram(train_docs, train_docs, kernel)
test_g = gram.gram(train_docs, test_docs, kernel)

clf = svm.SVC(kernel = 'precomputed')
clf.fit(train_g, y_train)

print clf.predict(test_g)

print ""
print "---ngk---"
print ""
kernel = ngk.ngk(3)

train_g = gram.gram(train_docs, train_docs, kernel)
test_g = gram.gram(train_docs, test_docs, kernel)

clf = svm.SVC(kernel = 'precomputed')
clf.fit(train_g, y_train)

print clf.predict(test_g)

#---------------------------------
#
# Old test code
#
#---------------------------------
#conv = util.mapa(docs)
#k = util.kernel(test_wk, conv)
#docfloats = [[0], [1], [2], [4]]
#docfloats = np.arange(len(docs)).reshape(-1, 1)
#
#gram = np.dot(docfloats, docfloats.T)
#

#

#print clf.predict(gram)
#print test_wk(docs[0], docs[1])
#print k([1], [0])


#print test_wk(docs[1], docs[1])
#print test_wk(docs[2], docs[2])
#print test_wk(docs[3], docs[3])
#print test_wk(docs[4], docs[4])
#print test_wk(docs[0], docs[2])
#print "---"
#test_ngk = ngk.ngk(2)
#print ngk.ngk(2)(docs[4], docs[4])
#print test_ngk(docs[0], docs[2])

