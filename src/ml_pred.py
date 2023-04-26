def predict_score(score_clf, data):
  vect = score_clf.transform(data).toarray()
  return score_clf.predict(vect)