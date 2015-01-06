import kernel_approx

a = ["pengar", "mafksl", "kalfkwjkk", "fkalslfks", "akfpwrlk", "asldfpvl", "asldfa", "lfsasl"]

n = 3
x = 7
sskn = 3
sskl = 0.5

update()

def testString(S, nn, nx, nsskn, nsskl):
	a = S
	n = nn
	x = nx
	sskn = nsskn
	sskl = nsskl
	update()

def update():
	#approxKern bor vara en 8x8-matris
	approxKern = kernel_approx.approxKernelSSK(a, n, x, sskn, sskl)

	#exactKern bor bara en 8x8-matrix
	exactKern = kernel_approx.exactGramSSK(a, sskn, sskl)

	#align bor vara 0 < align < 1
	align = kernel_approx.alignment(approxKern, exactKern)

	#alignExact bor vara = 1
	alignExact = kernel_approx.alignment(exactKern, exactKern)
