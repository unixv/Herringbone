import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import metrics
import joblib
import re

class NumericalFilter(BaseEstimator, TransformerMixin):
	"""
	Custom transformer to filter out numerical strings
	"""

	def fit(self, X, y=None):
		return self

	def transform(self, X):
		return [' '.join([word for word in doc.split() if not re.match(r'^\d+(\.\d+)?$', word)]) for doc in X]

class Assistant():

	def __init__(self, dataset, model_filename='log_type_classifier.pkl', is_remote=False):
		"""
		Configure the `dataset` parameter with either a local file path or a remote URL.
		If specifying a remote URL, set the `is_remote` parameter to True.
		"""

		self.df = pd.read_csv(dataset, on_bad_lines='skip')
		self.df.dropna(subset=['type', 'raw'], inplace=True)

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.df['raw'], 
																				self.df['type'], 
																				test_size=0.9, 
																				random_state=42)

		self.pipeline = Pipeline([
		('filter', NumericalFilter()),
		('vectorizer', CountVectorizer(tokenizer=self.custom_tokenizer)),
		('classifier', MultinomialNB())
		])

		"""
		Train, evaluate, and dump the model into a .pkl file
		"""
		self.pipeline.fit(self.X_train, self.y_train)
		self.y_pred = self.pipeline.predict(self.X_test)
		print(metrics.classification_report(self.y_test, self.y_pred))
		self.vectorizer = self.pipeline.named_steps['vectorizer']

		try:
			self.text_features = self.vectorizer.get_feature_names_out()
		except AttributeError:
			self.text_features = self.vectorizer.get_feature_names()
		
		self.model_filename = model_filename
		joblib.dump(self.pipeline, self.model_filename)

		print("Assistant is ready to learn with the base model!")

	def custom_tokenizer(self, text):
		"""
		Custom tokenizer to remove numbers.
		"""

		tokens = text.split()
		filtered_tokens = [token for token in tokens if not re.match(r'^\d+$', token)]
		return filtered_tokens

	def load_model(self):
		"""
		Load model from .pkl
		"""
		return joblib.load(self.model_filename)

	def predict_log_type(self, raw_log, model):
		"""
		Predict log type.
		"""
		return model.predict([raw_log])[0]

	def retrain_model(self, new_data, new_labels, model):
		"""
		Retrain the model with corrected data.
		"""

		new_df = pd.DataFrame({'raw': new_data, 'type': new_labels})

		self.X_train = pd.concat([self.X_train, new_df['raw']], ignore_index=True)
		self.y_train = pd.concat([self.y_train, new_df['type']], ignore_index=True)

		model.fit(self.X_train, self.y_train)
		joblib.dump(model, self.model_filename)
		return model
