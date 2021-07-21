import re
import nltk
import gensim
import numpy as np
from nltk.corpus import wordnet, stopwords, words
from nltk.stem import WordNetLemmatizer
from itertools import combinations

nltk.download('words')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

class SpyMasterAI:
  def __init__(self, model = None, red_words = None, blue_words = None, 
               assa_word = None, czn_words = None):
    if(model == None or red_words == None or 
       blue_words == None or assa_word == None or czn_words == None):
      raise Exception("Please enter the all parameters")
    self.red_words = red_words
    self.blue_words = blue_words
    self.assa_word = assa_word
    self.czn_words = czn_words
    self.ally_label = 'red'
    self.ally_team = None
    self.enemy_team = None
    self.model = model
    self.arr_similar = None
    self.choose_side(self.ally_label)
    self.max_comb = 4
  
  def get_closer_word(self,ally_team, enemy_team):
    self.arr_similar = self.model.most_similar(ally_team,enemy_team)
    return self.clean_arr()

  def choose_side(self,ally_label):
    if(ally_label == 'red'):
      self.ally_team = self.red_words 
      self.enemy_team = self.blue_words
    else:
      self.ally_team = self.blue_words 
      self.enemy_team = self.red_words

  def clean_arr(self):
    cleaned_arr = []
    if self.arr_similar == None:
      raise Exception('Please fist call the function \'get_closer_word\'')
    for tup in self.arr_similar:
      if self.clean_word(tup[0]) not in self.ally_team:
        cleaned_arr.append(tup)
    self.arr_similar = cleaned_arr
    return self.arr_similar

  def get_pos(self,word):
    tag = nltk.pos_tag([word])[0][1][0]
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    element = tag_dict.get(tag)
    if(element == "j" or element=="n" or element=="v" or element=="r"):
        return element
    return 'n'

  def clean_word(self, word):
    word = re.sub('[^a-zA-z]', ' ', word)
    wl = WordNetLemmatizer()
    all_stopwords = stopwords.words('english')
    return wl.lemmatize(word, pos = self.get_pos(word)) if word not in set(all_stopwords) else None 

  def all_math_combination(self):
    self.ally_comb = []
    self.enemy_comb = []
    temp_ally_comb = []
    temp_enemy_comb = []
    for i in range(1,len(self.ally_team)+1):
      if i == self.max_comb:
        break
      temp_ally_comb.append(np.array(list(combinations(self.ally_team,i)),dtype='object'))
    for i in range(1,len(self.enemy_team)+1):
      if i == self.max_comb:
        break
      temp_enemy_comb.append(np.array(list(combinations(self.enemy_team,i)),dtype='object'))
    for i in temp_ally_comb:
      for j in i:
        self.ally_comb.append(j)
    for i in temp_enemy_comb:
      for j in i:
        self.enemy_comb.append(j)
    return self.ally_comb, self.enemy_comb

  def update_table(self, deleted_words):
    updated = False
    for d in deleted_words:
      if(d == self.assa_word[0]):
        print("It was assasin word. You loosed!!")
        return
    self.red_words = np.setdiff1d(self.red_words, deleted_words)
    self.blue_words = np.setdiff1d(self.blue_words, deleted_words)
    self.czn_words = np.setdiff1d(self.czn_words, deleted_words)
    self.choose_side(self.ally_label)


  def best_combination(self):
    self.choose_side(self.ally_label)
    self.all_math_combination()
    best_tuple = ("",1)
    best_num = None
    best_ally = None
    self.index = 0
    while True:
      for ally in self.ally_comb:
        for enemy in self.enemy_comb:
          if(len(ally)!=len(enemy)):
            continue
          temp = self.get_closer_word(ally,enemy)
          if(temp[0][1] <= best_tuple[1]):
            if((self.model.distance(temp[self.index][0],self.assa_word[0]) < 0.6) or 
              (temp[self.index][0] not in words.words()) or 
              (temp[self.index][0] in ally[0]) or (ally[0] in temp[self.index][0])):
              continue
            best_tuple = temp[self.index]
            best_num = len(ally)
            best_ally = ally
      if best_num == None:
        self.index +=1
        continue
      break
    return best_tuple, best_num, best_ally


class AgentAI:
  def __init__(self,model = None,words=None,spy_tuple = None):
    if(model==None or words==None):
      raise Exception("Please enter all parameters")
    self.model = model
    self.game_words = words
    if spy_tuple != None:
      self.spy_tuple = spy_tuple
      self.spy_word, self.spy_num = self.spy_tuple
  
  def choose_word(self, spy_tuple = None):
    if spy_tuple != None:
      self.spy_word, self.spy_num = spy_tuple
    self.dict_word_distance = {}
    for word in self.game_words:
      self.dict_word_distance[word] = self.model.distance(self.spy_word,word)
    self.dict_word_distance = dict(sorted(self.dict_word_distance.items(), 
                                          key=lambda item: item[1]))
    return list(self.dict_word_distance.items())[:self.spy_num]
