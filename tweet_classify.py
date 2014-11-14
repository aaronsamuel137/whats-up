import nltk
import csv

def hasRepeats(document):
    """Returns True is more than 3 consecutive letters are the same in document."""
    previous = ''
    two_previous = ''
    for letter in document:
        if letter == previous == two_previous:
            return True
        two_previous = previous
        previous = letter
    return False

# features for the classifier
# all features should return a boolean
all_features = {
    'hasGood': lambda document: any(word in ['good', 'awesome', 'wonderful'] for word in document.split()),
    'hasBad': lambda document: any(word in ['bad', 'terrible', 'horrible'] for word in document.split()),
    'hasHappy': lambda document: 'happ' in document,
    'hasSad': lambda document: 'sad' in document,
    'hasLove': lambda document: 'love' in document or 'loving' in document,
    'hasHate': lambda document: 'hate' in document,
    'hasSmiley': lambda document: any(word in [':)', ':D', '(:'] for word in document.split()),
    'hasWinky': lambda document: any(word in [';)', ';D'] for word in document.split()),
    'hasFrowny': lambda document: any(word in [':(', '):', 'D:', ':.('] for word in document.split()),
    'hasBest': lambda document: 'best' in document,
    'hasWorst': lambda document: 'worst' in document,
    'hasDont': lambda document: any(word in ['dont','don\'t','do not','does not','doesn\'t'] for word in document.split()),
    'hasExclamation': lambda document: '!' in document,
    'hasRepeats': lambda document: hasRepeats(document),
    'hasHeart': lambda document: any(word in ['<3', '&lt;3'] for word in document.split()),
    'hasCant': lambda document: any(word in ['cant','can\'t','can not'] for word in document.split()),
    'hasExpense': lambda document: any(word in ['expensive', 'expense'] for word in document.split()),
    'hasFavorite': lambda document: 'favorite' in document,
    'hasFantastic': lambda document: 'fantastic' in document,
    'hasFuck': lambda document: 'fuck' in document,
    'hasFriend': lambda document: any(word in ['bff', 'friend'] for word in document.split()),
    'hasLol': lambda document: 'lol' in document,
    'hasHaha': lambda document: 'haha' in document,
    'hasGreat': lambda document: 'great' in document,
    'hasNo': lambda document: 'no' in document.split(),
    'hasYes': lambda document: 'yes' in document.split(),
    'hasCold': lambda document: 'hot' in document.split(),
    'hasHot': lambda document: 'cold' in document.split(),
    'hasFree': lambda document: 'free' in document,
    'hasImprove': lambda document: 'improve' in document,
    'hasFail': lambda document: 'fail' in document,
    'hasSweet': lambda document: 'sweet' in document,
    'hasNew': lambda document: 'new' in document.split(),
    'hasCurse': lambda document: 'curse' in document,
    'hasFunny': lambda document: any(word in ['funny', 'hilarious', 'silly'] for word in document.split()),
    'hasLoss': lambda document: any(word in ['lost', 'loss'] for word in document.split()),
}

def extract_features(document):
    features = {}
    for feature, function in all_features.items():
        features[feature] = function(document.lower())
    return features

def main():
    # read in the tweet csv file with training data
    sentiment_map = {'0': 'negative', '2': 'neutral', '4': 'positive'}
    fp = open('trainingandtestdata/training.1600000.processed.noemoticon.csv', 'rb')
    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')

    data = [(row[5], sentiment_map[row[0]]) for row in reader]
    print('read ' + str(len(data)) + ' tweets for training the classifier')

    training_set = nltk.classify.apply_features(extract_features, data)
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    # read in test data
    fp = open('trainingandtestdata/testdata.manual.2009.06.14.csv', 'rb')
    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
    data = [(row[5], sentiment_map[row[0]]) for row in reader]

    print('read ' + str(len(data)) + ' tweets for testing the classifier')

    num_correct = 0
    for tweet in data:
        classification = classifier.classify(extract_features(tweet[0]))
        if classification == tweet[1]:
            num_correct +=1
        print(tweet[0] + ':\t' + classification)

    print(str(float(num_correct) / len(data)) + '% accuracy')

    classifier.show_most_informative_features(32)

main()
