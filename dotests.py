from reuter import DataType
from data import Topics, Dataset


def getRecallPrecision(found, true):
	tp = fp = tn = fn = 0
	for i,c in enumerate(classifications):
		if c:
			if true_classifications[i]:
				tp = tp + 1
			else
				fp = fp + 1
		else:
			if not true_classifications[i]:
				tn = tn + 1
			else
				fn = fn + 1
	return tp/(tp+fp), tp/(fn+tp)


for topic_to_test in Topics:
	
	dataset = Dataset()

	training_articles = [dataset.getData(topic=topic, data_type=DataType.training) for topic in Topics]#[articlesWithTopic("earn"), restOfTheArticles]
	
	true_classifications = [(topic_to_test.value in article.topics) for article in training_articles];


	n = 5
	plambda = 0.5

	SVMSSK.train(training_articles, true_classifications n, plambda);

	classifications = SVMSSK.test(testing_articles, n, plambda);

	true_classifications = [(topic_to_test in article.topics) for article in testing_articles]

	recall, precision = getRecallPrecision(found=classifications, true=true_classifications)

	print("precision and recall for topic %s: %f %f", topic_to_test, precision, recall)
