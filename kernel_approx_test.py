import kernels.kernel_approx as kernel_approx
import reuters

parser = reuters.Parser("data/reuters21578")
training_set_100 = parser.articles(only_of_type=reuters.DataType.training)[0:100]

training_set_100_bodys = [article.body for article in training_set_100 if "earn" in article.topics]

sskn = 14
sskl = 0.5

approxKern = kernel_approx.approxKernelSSKalt(S=training_set_100_bodys, n=3, x=7, sskn=sskn, sskl=sskl)

#exactKern bor bara en 8x8-matrix
exactKern = kernel_approx.exactGramSSK(S=training_set_100_bodys, sskn=sskn, sskl=sskl)

#align bor vara 0 < align < 1
align = kernel_approx.alignment(approxKern, exactKern)

#alignExact bor vara = 1
alignExact = kernel_approx.alignment(exactKern, exactKern)

print(approxKern)
print(exactKern)
print(align)
print(alignExact)