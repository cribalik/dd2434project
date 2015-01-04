__author__ = 'Pontus'
import wk
import ngk


docs = []
docs.append("jag ska ga bort")
docs.append("du ska ga hem nu")
docs.append("ska du ga bort")
docs.append("jag ska bort")


test_wk = wk.wk(wk.get_idf(docs))
print test_wk(docs[0], docs[0])
print test_wk(docs[0], docs[2])
print "---"
test_ngk = ngk.ngk(2)
print test_ngk(docs[0], docs[0])
print test_ngk(docs[0], docs[2])