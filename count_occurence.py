from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(input='content')
corpus = [
     'This is the first document.',
     'This is the second second document.',
     'And the third one.',
     'Is this the first document?',
 ]
 
X = vectorizer.fit_transform(corpus)
print(X)
analyze = vectorizer.build_analyzer()
analyze("This is a text document to analyze.") == (
    ['this', 'is', 'text', 'document', 'to', 'analyze'])
    
vectorizer.get_feature_names() == (
     ['and', 'document', 'first', 'is', 'one',
     'second', 'the', 'third', 'this'])
     
print(X.toarray())
