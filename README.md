# Codenames AI

### Summary
This repository is the simple AI implementation for the SpyMaster and Agent role of the game codenames which is a 2015 card game for 4–8 players designed by Vlaada Chvátil and published by Czech Games Edition. The program was written in codenamesAI.py program (SpyMasterAI class and AgentAI Class). Also I provided 2 examples for usage of each class in examples folder. <br/><br/>
Note: This classes were written with consideration of gensim load models. That is why if you use another Word Representation models, you can have trouble in the some methods of classes.

### Essential Libraries
>re - for regular expression operations<br/>
>nltk - for statistical natural language processing<br/>
>numpy - for mathematical operations<br/>
>itertools - for finding the best combination with using combinations

### Simple Explanation of AgentAI
The working method of AgentAI is pretty simple. It just find the distance between spymaster's word (first element of spymaster's tuple) and the all words, and choose the words which is closer to spymaster's word. The number of words Spymaster wants is the second element of spymaster's tuple.

### Simple Explanation of SpyMasterAI
The SpyMasterAI class is much more complex than AgentAI class. Basically it makes all n (self.max_comb) combinations of words of ally and choose the best suited between them. When finding the closer words, it also consider the enemy team, and also do preprocessing step to the words (stopword, lemmatizer, if english word etc). It has also update_table method which basically remove the founded words and update the table.
