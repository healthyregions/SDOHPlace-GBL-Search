import re
import uuid

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from app.services.neural.model import model


class Query:

	def __init__(self):
		pass

	def get_query_expansion(self, query):
		q = query.split(" ") if query else []
		print(model)
		return {
			"query": q,
			"syns": Synonyms().generate_tokens(query)
		}


class Synonyms:

	def __init__(self):
		self.pos_tag_map = {
			'NN': [wn.NOUN],
			'JJ': [wn.ADJ, wn.ADJ_SAT],
			'RB': [wn.ADV],
			'VB': [wn.VERB]
		}

	def pos_tag_converter(self, nltk_pos_tag):
		root_tag = nltk_pos_tag[0:2]
		try:
			self.pos_tag_map[root_tag]
			return self.pos_tag_map[root_tag]
		except KeyError:
			return ''

	def tokenizer(self, sentence):
		return word_tokenize(sentence)

	def pos_tagger(self, tokens):
		return nltk.pos_tag(tokens)

	def stopword_treatment(self, tokens):
		stopword = stopwords.words('english')
		result = []
		for token in tokens:
			if token[0].lower() not in stopword:
				result.append(tuple([token[0].lower(), token[1]]))
		return result

	def get_synsets(self, tokens):
		synsets = []
		for token in tokens:
			wn_pos_tag = self.pos_tag_converter(token[1])
			if wn_pos_tag == '':
				continue
			else:
				synsets.append(wn.synsets(token[0], wn_pos_tag))
		return synsets

	def get_tokens_from_synsets(self, synsets):
		tokens = {}
		for synset in synsets:
			for s in synset:
				if s.name() in tokens:
					tokens[s.name().split('.')[0]] += 1
				else:
					tokens[s.name().split('.')[0]] = 1
		return tokens

	def get_hypernyms(self, synsets):
		hypernyms = []
		for synset in synsets:
			for s in synset:
				hypernyms.append(s.hypernyms())

		return hypernyms

	def get_tokens_from_hypernyms(self, synsets):
		tokens = {}
		for synset in synsets:
			for s in synsets:
				for ss in s:
					if ss.name().split('.')[0] in tokens:
						tokens[(ss.name().split('.')[0])] += 1
					else:
						tokens[(ss.name().split('.')[0])] = 1
		return tokens

	def underscore_replacer(self, tokens):
		new_tokens = {}
		for key in tokens.keys():
			mod_key = re.sub(r'_', ' ', key)
			new_tokens[mod_key] = tokens[key]
		return new_tokens

	def generate_tokens(self, sentence):
		tokens = self.tokenizer(sentence)
		tokens = self.pos_tagger(tokens)
		tokens = self.stopword_treatment(tokens)
		synsets = self.get_synsets(tokens)
		synonyms = self.get_tokens_from_synsets(synsets)
		synonyms = self.underscore_replacer(synonyms)
		hypernyms = self.get_hypernyms(synsets)
		hypernyms = self.get_tokens_from_hypernyms(hypernyms)
		hypernyms = self.underscore_replacer(hypernyms)
		tokens = {**synonyms, **hypernyms}
		return tokens
