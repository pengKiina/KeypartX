
import pandas as pd 
import re ,spacy,emoji

import matplotlib.pyplot as plt
from urllib.request import urlretrieve as uru 
from PIL import Image
import numpy as np
from wordcloud import WordCloud , ImageColorGenerator
from collections import Counter




#import coreferee

def coreNLP():
  nlp = spacy.load('en_core_web_lg') #"en_core_web_sm"
  crossLC =""
  try:
    import coreferee
    nlp.add_pipe('coreferee')
    print('coreferee is Available')
    crossLC = 0
  except:
    try:
      import crosslingual_coreference
      nlp.add_pipe("xx_coref", config={"chunk_size": 2500, "chunk_overlap": 2, "device": 0})
      print('crosslingual-corefernce is Available')
      crossLC = 1
    except:
      print("No Coreference package avaiable")
  return nlp, crossLC

nlp,crossLC = coreNLP()


#1 count frequence of list and word cloud 
def countFreq(my_list,extra_name=""):
# Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    keys =[]
    values = []
    for key, value in freq.items():
        keys.append(key)
        values.append(value)
    keys_name = extra_name
    
    dlist = {keys_name:keys,(keys_name +'_freq'):values}
    df_freq = pd.DataFrame(dlist)
    df_freq = df_freq.sort_values(by= (keys_name +'_freq'), ascending=False)
    return df_freq


# count frequence dict and dataframe 
def variablename(var):
    return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())] # get the variable name 
def countFreq2(my_list,extra_name=""):
    """ list return frequency dictiaory and dataframe """
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    keys =[]
    values = []
    for key, value in freq.items():
        keys.append(key)
        values.append(value)
    keys_name = "".join(variablename(my_list)) + extra_name
    
    dlist = {keys_name:keys,(keys_name +'_freq'):values}
    df_freq = pd.DataFrame(dlist)
    df_freq = df_freq.sort_values(by= (keys_name +'_freq'), ascending=False)
    return df_freq, freq


# https://github.com/pengKiina/KeypartX/raw/main/images/ta_white.png
def wordCloud(freq_dict, background_color="turquoise",max_words=200,collocations=False,mask_img = False, save_fig = False,random_state=2,normalize_plurals = False, width=800, height=600):
  """
    freq_dict: dictionary of word and frequency 
    make_img : image address local or url 
    save_fig:  save wordcould address"""

  if mask_img:
    try:
      uru(mask_img,'ta_white.png')
      mask = np.array(Image.open('ta_white.png')) 
    except:
            mask = np.array(Image.open(mask_img)) 

    #font_path ="C:\Videos\Personal_life\R_Python\jiebaDict\SourceHanSerifTC_EL-M\SourceHanSerifTC-Regular.otf"
    #wc = WordCloud(font_path=font_path, background_color="white",collocations=False,mask=mask, random_state=3,normalize_plurals = False, width=800, height=1000, )
    wc= WordCloud(background_color=background_color,max_words=max_words,collocations=collocations,mask=mask, random_state=random_state,normalize_plurals = normalize_plurals, width=width, height=height,)
    wc.generate_from_frequencies(Counter(freq_dict))
    #create coloring from image
    image_colors = ImageColorGenerator(mask)

    plt.figure(figsize=(width/100,height/100))
    #recolor wordcloud and show
    #plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear") 
    plt.imshow(wc) 
    plt.axis("off") 
    if save_fig : 
       plt.savefig(save_fig,dpi=300)
       plt.show()
  else:
      wc= WordCloud(background_color=background_color,max_words=max_words,collocations=collocations, random_state=random_state,normalize_plurals = normalize_plurals, width=width, height=height,)
      wc.generate_from_frequencies(Counter(freq_dict))
      plt.figure(figsize=(width/100,height/100))
      #plt.figure()
      #recolor wordcloud and show
      #plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear") 
      plt.imshow(wc) 
      plt.axis("off") 
      if save_fig : 
        plt.savefig(save_fig,dpi=300)
        plt.show()








#2 coreferee
#import coreferee, spacy
#nlp = spacy.load('en_core_web_lg')
#nlp.add_pipe('coreferee')

#core_text = "Although he was very busy with his work, Peter had had enough of it. He and his wife decided they needed a holiday. They travelled to Spain because they loved the country very much."
def coref(core_text):
  if crossLC == 0:
    doc = nlp(core_text)
    #doc._.coref_chains.print()
    refs = doc._.coref_chains

    keyNs = []
    key_list =[]
    for ref in refs:
      keyN = ref[ref.most_specific_mention_index]
      if len(keyN)==1:
          key_l = [a[0] for a in list(ref)]
          keyNs.append(keyN[0])
          key_list.append(key_l)

    words_index = {}
    for i, token in enumerate(doc):
      for keyN, keyL in zip(keyNs, key_list):
        if i in keyL and token.tag_ =="PRP":
          #print(token.text)
          word = doc[keyN].text
          words_index.update({i:word})
    words2 = []
    for i, token in enumerate(doc):
      if i in list(words_index):
        word = words_index[i]
      else:
        word = token.text
      words2.append(word)
    coref_text = " ".join(words2)
  elif crossLC ==1:
    doc =   nlp(core_text)                   # add crosslingual-corefernce on 23.04.2023
    coref_text =doc._.resolved_text["resolved_text"]
  else:
    coref_text = core_text
     
  return coref_text



#3 lemmatize the words
def lemma_en(text):
    #python -m spacy download en_core_web_sm 
    # Create a Doc object
    #text = "asked I am gone you went to supermarkets to you are bought buy drinks visited and traveled by flying"
    doc = nlp(text)
    
    #lemmatized_text = " ".join([token.text for token in doc if token.text in ['him','her','them'] else token.lemma_])
    words = []
    for token in doc :
      if token.text in ['him','her','them']: # for coreference, otherwise it will be changed to he, she, they
          word = token.text
      else:
        word = token.lemma_
      words.append(word)
       
    lemmatized_text = " ".join(words)

    #print(lemmatized_text)
    return lemmatized_text

def lemma_noun(text):
    #python -m spacy download en_core_web_sm 
    # Create a Doc object
    #text = "asked I am gone you went to supermarkets to you are bought buy drinks visited and traveled by flying"
    doc = nlp(text)
    
    #lemmatized_text = " ".join([token.text for token in doc if token.text in ['him','her','them'] else token.lemma_])
    words = []
    for token in doc :
      if token.pos_ == "NOUN": # for coreference, otherwise it will be changed to he, she, they
          word = token.lemma_
      else:
        word = token.text
      words.append(word)
       
    lemmatized_text = " ".join(words)

    #print(lemmatized_text)
    return lemmatized_text


#4 nouns compund

from spacy.matcher import Matcher
# Matcher is initialized with the shared vocab
def nnncomp(text):
  # Each dict represents one token and its attributes
  matcher = Matcher(nlp.vocab)
  # Add with ID, optional callback and pattern(s)
  pattern = [{"POS": "NOUN"},{"POS": "NOUN","OP":"{1,2}"}] # only macth maxium 3 nouns 15.10.2022
  matcher.add('NA+', [pattern])
  doc = nlp(text)
  # Match by calling the matcher on a Doc object
  matches = matcher(doc)
  # Matches are (match_id, start, end) tuples
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      spans.append(span)
  nnncomp_spans  = spacy.util.filter_spans(spans) # only get the longest span
  nnncomp0 = [x.text for x in nnncomp_spans]
  nnncomp1 = ["".join(x.split()) for x in nnncomp0]
  return nnncomp0,nnncomp1

#5 negative adjective compound
def negadj(textneg,negword):
  matcher = Matcher(nlp.vocab)
  pattern = [{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"POS": "ADJ","OP":"+"}] #"OP":"+" 1 or more * 0 or more
  matcher.add('No+adj', [pattern])

  #textneg = "I do not like you never know it be not really pretty, it means no money no girl"
  doc = nlp(textneg)

  matches = matcher(doc)

  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not pretty
        spans.append(span)
  adj_doc = spacy.util.filter_spans(spans) # only get the longest span

  negadj0 =[]
  negadj1 =[]
  if len(adj_doc)>0:
    for sp in adj_doc:
      negadj0.append(sp.text)
      ss = []
      for s in sp:
        if s.text == negword: # never is adv 
          ss.append(lemma_en(s.text))  # ss.append(s.text) 02.10.2022
        elif s.pos_ == "ADV":
          pass
        else:
          ss.append(lemma_en(s.text))   # ss.append(s.text) 02.10.2022
      negadj1.append("".join(ss))
  else:
    negadj0 =[]
    negadj1 =[]
  #print(negadj0,negadj1, sep="\n")
  return negadj0,negadj1


#6 negative verb compound


def negverb(textneg,negword):
  matcher1 = Matcher(nlp.vocab)
  pattern1 = [{"POS": "AUX","OP":"*"},{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"POS": "VERB","OP":"+"}] #"OP":"+" 1 or more * 0 or more
  matcher1.add('No+verb', [pattern1])
  pattern2 = [{"POS": "AUX","OP":"*"},{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"LOWER":"like"}] #"OP":"+" 1 or more * 0 or more
  matcher1.add('No+verb2', [pattern2])

  #textneg = "I do not like you never know it be not really pretty, it means no money no girl"
  doc = nlp(textneg)
  matches = matcher1(doc)
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not like
        spans.append(span)
  verb_doc = spacy.util.filter_spans(spans) # only get the longest span
  #print('verb_doc:',verb_doc)
  negverb0 =[]
  negverb1 =[]
  if len(verb_doc)>0:
    for sp in verb_doc:
      ss = []
      ss1 = []
      for s in sp:
        if s.pos_ == "AUX":
          ss.append(s.text)
        elif s.text == negword: # never is adv 
          ss.append(s.text)
          ss1.append(lemma_en(s.text)) # ss1.append(s.text) 02.10.2022
        elif s.pos_ == 'ADV':
          ss.append(s.text)
        else:
          ss.append(s.text)
          ss1.append(lemma_en(s.text))  # ss1.append(s.text) 02.10.2022
      negverb0.append(" ".join(ss))
      negverb1.append("".join(ss1))
  else:
    negverb0 =[]
    negverb1 =[]
  #print(negverb0,negverb1, sep="\n")
  return negverb0,negverb1

#7 merg quoted words

def quote(text):
  quote0 = []
  quote1 = []
  for qt in re.findall(r'"(.*?)"', text): # double quote
    if len(qt.split())<4: # in case there's xxxxx it's 
      qt1 = re.sub(r'[^\w\s]', '', qt) # remove punct in quotes "good-good"
      qtj = "".join(qt1.split())
      quote0.append(qt)
      quote1.append(qtj)
  for qt in re.findall(r"'(.*?)'", text): # single quote
    if len(qt.split())<4:
      qt1 = re.sub(r'[^\w\s]', '', qt) # remove punct in quotes 'good-good'
      qtj = "".join(qt1.split())
      quote0.append(qt)
      quote1.append(qtj)
  #print(quote0,quote1)
  return quote0,quote1

#8 hyphenated and entity words
# hyphenated words
def hyphen(text):
  hypen0 = re.findall("((?:\w+-)+\w+)",text) 
  hypen1= []
  for hyp in hypen0:
    hypj = "".join(hyp.split('-'))
    hypen1.append(hypj)
  #print(hypen0,hypen1)
  return hypen0,hypen1

# entity words 
"""def entity(text):
  doc = nlp(text)
  entity0 =[]
  entity1 = []
  for ent in doc.ents:
      #print(ent.text, ent.start_char, ent.end_char, ent.label_)
      entt = ent.text
      entity0.append(entt)
      enttj = "".join(entt.split())
      entity1.append(enttj)
  #print(entity0,entity1)
  return entity0,entity1"""
# entity words + some proper noun e.g. paradise 
def entity(text):
  doc = nlp(text)
  entity0 =[]
  entity1 = []
  text1 = text
  for ent in doc.ents:
      #print(ent.text, ent.start_char, ent.end_char, ent.label_)
      entt = ent.text
      text1 = re.sub(r'\b' + entt + r'\b',"    ", text1)
      entity0.append(entt)
      enttj = "".join(entt.split())
      entity1.append(enttj)
  #print(entity0,entity1)
  doc2 = nlp(text1)
  propns0 = []
  propns1 = []
  
  for token in doc2:
        if token.pos_ =="PROPN":
            propn = token.text
            propns0.append(propn)
            propnj = "".join(propn.split())
            propns1.append(propnj)          
            
  return entity0 + propns0 ,entity1 +propns1




#9 n't lemmatize(ntverb)
# (ntwerb)change n't to not Apostrophe
def ntverb(text1):
  ntverb0 = []
  ntverb1 =[]
  for word in text1.split():
    if "n’t" in word:
      #print(word)
      ntverb0.append(word)
      ntverb1.append(lemma_en(word))
    elif "n't" in word:
      #print(word)
      ntverb0.append(word)
      ntverb1.append(lemma_en(word))

  #print(ntverb0,ntverb1)
  return ntverb0,ntverb1

#10 remove coma in Adj,Adj
def nonAcomaA(text1):
  #text1 = 'wonderful, beautiful and great country'
  text1 = text1 + "  "  # in case "wonderful," sentence, then there will be no poss[i+2]
  cols = ['index','word','pos']
  rows =[]
  for d in nlp(text1):
    row = d.i,d.text,d.pos_
    rows.append(row)
    #print(row)

  df = pd.DataFrame(rows, columns=cols)
  words = df.word.to_list()
  poss = df.pos.to_list()
  indexs = df.index.to_list()
  index_drop = []
  for i in range(len(df)-1):
    if words[i+1] =="," and poss[i] == poss[i+2]=="ADJ":
      #print(words[i:i+2])
      index_drop.append(indexs[i+1])

  df2 = df.drop(index_drop)
  nonAcomaA_sent = ' '.join(df2.word.to_list())
  return nonAcomaA_sent 

#11 av2n and nn edges
import itertools
def av2Nedge(adjNverbs2): # adjNverbs2 must be list
  av2Nedges =[]
  all_nouns1 = [] # nouns in adjVn edges 
  
  for anbs in adjNverbs2:
    cols = ['word','pos']
    rows=[]
    for anb in nlp(anbs):
      #print(anb.text,anb.pos_)
      if anb.text =='be':
        row = 'be','VERB'
      else:
        row = anb.text,anb.pos_
      rows.append(row)
    df_wp = pd.DataFrame(rows,columns =cols)
    nouns = df_wp[df_wp['pos'] == 'NOUN'].word.to_list()
    #all_nouns1.extend(nouns) 
    notNs = df_wp[df_wp['pos'] != 'NOUN'].word.to_list()
    for adjV in notNs:
      if adjV !='be':
        for nn in nouns:
          #print(adjV,nn)
          av2Nedges.append([adjV,nn])
          all_nouns1.append(nn)
  if len(all_nouns1)>1:
    nn_edges = list(itertools.combinations(set(all_nouns1), 2)) #noun noun edges edge
  else:
    nn_edges =[]

  return av2Nedges, nn_edges

#12 (mapnoun,mapadj,mapverb)mapping new words 
def mapnoun(new_textn,verbose = False):
  doc1 = nlp(new_textn)
  for token in doc1:
    if verbose:
      print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textn.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "NOUN",}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who"
  if verbose:
    print('---')
  doc2 = nlp(new_textn)
  for token in doc2:
    if verbose:
      print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
    print('---noun---')
def mapadj(new_textadj,verbose = False):
  doc1 = nlp(new_textadj)
  for token in doc1:
    if verbose:
       print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textadj.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "ADJ"}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who"
  if verbose:
      print('---')
  doc2 = nlp(new_textadj)
  for token in doc2:
    if verbose:
        print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
    print('---neg adj---')

def mapverb(new_textverb,verbose = False):
  doc1 = nlp(new_textverb)
  for token in doc1:
    if verbose:
        print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textverb.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "VERB",}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who
  if verbose:
    print('---')
  doc2 = nlp(new_textverb)
  for token in doc2:
    if verbose:
       print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
       print('---neg verb---')
       
#13 (adjNVmatch) match AdjN,NbeAdj,Nverb,verbN
from spacy.matcher import Matcher
def adjNVmatch(text5):
  # Matcher is initialized with the shared vocab
  #from spacy.matcher import Matcher
  # Each dict represents one token and its attributes
  matcher = Matcher(nlp.vocab)
  # Add with ID, optional callback and pattern(s)

  pattern = [{"POS": "ADJ","OP":"*"},{"POS": "NOUN","OP":"+"},{"LOWER": "be","OP":"+"}, {"POS": "ADV","OP":"*"},{"POS": "ADJ","OP":"+"}] #"OP":"+" 1 or more * 0 or more # ugly and expensive ugly is adj, ugly expensive ugly is adv
  matcher.add('(A)N+A', [pattern])
  #pattern2 =[{"LIKE_EMAIL":True}]
  pattern2 = [{"POS": "ADJ","OP":"+"},{"POS": "NOUN","OP":"+"}]
  matcher.add('A+N', [pattern2])
  
  pattern3 = [{"POS": "VERB","OP":"+"},{"POS": "ADJ","OP":"*"},{"POS": "NOUN","OP":"+"}]   # 11.11.2022 modified 
  matcher.add('V(A)+N', [pattern3]) # like beautiful girl - like girl, beautiful girl 

  pattern4 = [{"POS": "ADJ","OP":"*"},{"POS": "NOUN","OP":"+"},{"LOWER": "be","OP":"+"},{"POS": "VERB"}]  # 11.11.2022 modified 
  matcher.add('(A)N+V', [pattern4]) # delicious food is recommened 

  # pattern3 = [{"POS": "VERB","OP":"+"},{"POS": "NOUN","OP":"+"}]   # 09.10.2022 {"POS": "VERB"}
  # matcher.add('V+N', [pattern3])

  # pattern4 = [{"POS": "NOUN","OP":"+"},{"LOWER": "be","OP":"+"},{"POS": "VERB"}]
  # matcher.add('N+V', [pattern4])

  #doc = nlp("restaurantfood be nice expensive food like nice expensive , company be recommend,address , the price-quality ration is not quite right, soon cafe be hot cool massage place, beautiful destination, I like hotel")
  doc = nlp(text5)
  matches = matcher(doc)
  # Matches are (match_id, start, end) tuples
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      spans.append(span)
  adjNverbs1 = spacy.util.filter_spans(spans) # only get the longest span
  adjNverbs2 = [x.text for x in adjNverbs1]
  return adjNverbs2 


#text = "We 😊 recommend 😊and book your next stay at the Arctic Light 😊Hotel😊"

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)   # this patter is not full, use emoji module instead 

def emo(text, emojiINtext = False):
    """
    :smiling_face_with_smiling_eyes: : will be replaced by , but _ stay 
    """
    #text = 'I love food 😊, ok👍👍 bad😱😱 or 🙂great🙂 🙂 💀 😂? '
    #text = 'how good food ❤️ strong❤️😊 recommendation.'
    emojis = []   
    for emoD in emoji.emoji_list(text):
        emo = emoD['emoji']
        emojis.append(emo)

    if len(emojis)>0:
        new_text = text
        for e in emojis:
            new_text = new_text.replace(e,' , ')
    else:
        new_text = text 
        
    text2 = text
    for emo in emojis:
        emo_text = emoji.demojize(emo)
        #emo_text = emo_text.split('_')
        #emo_text ="".join(emo_text)
        emo_text = re.sub(r'[^\w\s]', '', emo_text)
        mapnoun(emo_text)
        text2 = text2.replace(emo," , " + emo_text +" , ")

    if emojiINtext:
        return text2,emojis
    else:
        return new_text, emojis 


  
def vaderAV():
  vader_text = pd.read_csv("https://raw.githubusercontent.com/pengKiina/KeypartX/main/vader_lexicon.csv")
  #vader_text
  words= vader_text.token.to_list()
  vader_adjs =[]
  vader_verbs = []
  for word in words:
    doc = nlp(word)
    if doc[0].pos_ == "ADJ" and len(doc[0].lemma_)>2 :
      ns = doc[0].lemma_
      if "sse" == ns[-3:] or "ness" == ns[-4:] :
        #print('adj',ns)
        pass
      else:
        vader_adjs.append(ns)
    elif doc[0].pos_ == "VERB" and len(doc[0].lemma_)>2:
      ns = doc[0].lemma_
      if "sse" == ns[-3:] or "ness" == ns[-4:] :
        #print('verb', ns)
        pass
      else:
        vader_verbs.append(ns)
  adjs_set = set(vader_adjs)
  #print(len(vader_adjs))
  #print(len(adjs_set))
  verbs_set = set(vader_verbs)
  verbs_set = (set([verbs_set]) - set(['lovelie']))
  #print(len(vader_verbs))
  #print(len(verbs_set))
  
  vader_df = pd.DataFrame.from_dict({'vader_adjs':adjs_set,'vader_verbs':verbs_set},orient = 'index')
  vader_df = vader_df.transpose()
  return vader_df, adjs_set, verbs_set 


# new for back and again

def abverb_old(abtext,myBA = False):
    """
    again, back # visit, come, go, travel, be and others verbs 
    myBA:  my own abverbs ['visit', 'come','go', 'travel', 'be']
    """
    #abtext = "We notlove2vvv it again to Finland, I came back to Finland"
    #abtext ="I come to Finland again"
    matcher1 = Matcher(nlp.vocab)
    pattern1 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'back'}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
    matcher1.add('verb + back', [pattern1])
    pattern2 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'again'}]#"OP":"+" 1 or more * 0 or more
    matcher1.add('verb + again', [pattern2])

    #textneg = "I do not like you never know it be not really pretty, it means no money no girl"
    doc = nlp(abtext)

    matches = matcher1(doc)
    spans =[]
    for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not like
        spans.append(span)

    ab_doc = spacy.util.filter_spans(spans) # only get the longest span

    if len(ab_doc)>0:
        ab_verbs = []
        for abd in ab_doc:

            abV =""
            abV2=""
            ab =""
            for token in abd:
                #print(token)
                if token.pos_ == "VERB":
                    abv = token.text
                    abv2 = token.lemma_
                    abV = abv.replace('2vvv','')
                    abV2= abv2.replace('2vvv','')
                   # print('abV',abV)
                else:
                    if token.text == "back":
                        ab1 = token.text
                        ab = ab1
                    elif token.text == "again":
                        ab1 =  token.text
                        ab = ab1
            #print(abV, abV2,ab)
            if myBA:  # my own abverbs 
                if len(abV)>1 and any([x in abV2 for x in myBA ]): # changed len(abV)>1 and abV2 in myBA: 09.10.2022
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print(abd1)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print(abd2)
                    abtext = abtext.replace(abd.text,abd2)
                    ab_verbs.append(ab_verb)
                    
            else:
                if len(abV)>1:
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print(abd1)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print(abd2)
                    abtext = abtext.replace(abd.text,abd2)
                    ab_verbs.append(ab_verb)                  
            
        return abtext, ab_verbs 
    else:
        return abtext, []
      
      
def abverb_old2(abtext,myBA = False,myBAverb = False):
    """
    myBA: ['back','again']
    myBAverb:  my own abverbs ['visit', 'come','go', 'travel', 'be']
    """
    matcher1 = Matcher(nlp.vocab)
    if myBA:
        for myba in myBA:
            #abtext = "We notlove2vvv it again to Finland, I came back to Finland"
            #abtext ="I come to Finland again"
            pattern1 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": myba}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
            matcher1.add('verb + back', [pattern1])
            pattern2 = [{"LEMMA": {"IN": ["are", "am","been","is","was",'be','were']}}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": myba}]#"OP":"+" 1 or more * 0 or more
            matcher1.add('be + again', [pattern2])
    else:
        pattern1 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'back'}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
        matcher1.add('verb + back', [pattern1])
        pattern2 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'again'}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
        matcher1.add('verb + back', [pattern2])
        pattern3 = [{"LEMMA": {"IN": ["are", "am","been","is","was",'be','were']}}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'back'}]#"OP":"+" 1 or more * 0 or more
        matcher1.add('be + again', [pattern3])


    doc = nlp(abtext)
    
    matches = matcher1(doc)
    spans =[]
    for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not like
        spans.append(span)

    ab_doc = spacy.util.filter_spans(spans) # only get the longest span
    #print('ab_doc' , ab_doc)
    if len(ab_doc)>0:
        ab_verbs = []
        for abd in ab_doc:

            abV =""
            abV2=""
            ab =""
            for token in abd:
                #print(token)
                if token.pos_ == "VERB" or token.lemma_ =="be":
                    abv = token.text
                    abv2 = token.lemma_
                    abV = abv.replace('2vvv','')
                    abV2= abv2.replace('2vvv','')
                   # print('abV',abV)
                else:
                    if token.text == "back":
                        ab1 = token.text
                        ab = ab1
                    elif token.text == "again":
                        ab1 =  token.text
                        ab = ab1
            #print(abV, abV2,ab)
            if myBAverb:  # my own abverbs 
                #print('yes')
                if len(abV)>1 and any([x in abV2 for x in myBAverb]): # changed len(abV)>1 and abV2 in myBA: 09.10.2022
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print(abd1)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print(abd2)
                    abtext = abtext.replace(abd.text,abd2)
                    ab_verbs.append(ab_verb)
                    
            else:
                if len(abV)>1:
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print(abd1)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print(abd2)
                    abtext = abtext.replace(abd.text,abd2)
                    ab_verbs.append(ab_verb)                  
            
        return abtext, ab_verbs 
    else:
        return abtext, []
      
      
def abverb(abtext,myBA = False,myBAverb = False):
    """
    myBA: ['back','again']
    myBAverb:  my own abverbs ['visit', 'come','go', 'travel', 'be']
    """
    matcher1 = Matcher(nlp.vocab)
    if myBA:
        for myba in myBA:
            #abtext = "We notlove2vvv it again to Finland, I came back to Finland"
            #abtext ="I come to Finland again"
            pattern1 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": myba}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
            matcher1.add('verb + back', [pattern1])
            pattern2 = [{"LEMMA": {"IN": ["are", "am","been","is","was",'be','were']}}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": myba}]#"OP":"+" 1 or more * 0 or more
            matcher1.add('be + again', [pattern2])
    else:
        pattern1 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'back'}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
        matcher1.add('verb + back', [pattern1])
        pattern2 = [{"POS": 'VERB'}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'again'}] #"OP":"+" 1 or more * 0 or more  # ADP: 'from' ,'to'
        matcher1.add('verb + back', [pattern2])
        pattern3 = [{"LEMMA": {"IN": ["are", "am","been","is","was",'be','were']}}, {'IS_ASCII': True, 'OP': '{0,3}'},{"LOWER": 'back'}]#"OP":"+" 1 or more * 0 or more
        matcher1.add('be + again', [pattern3])


    doc = nlp(abtext)
    
    matches = matcher1(doc)
    spans =[]
    for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not like
        spans.append(span)

    ab_doc = spacy.util.filter_spans(spans) # only get the longest span
    #print('ab_doc' , ab_doc)
    if len(ab_doc)>0:
        ab_verbs = []
        for abd in ab_doc:

            abV =""
            abV2=""
            ab =""
            for token in abd:
                #print(token)
                if token.pos_ == "VERB" or token.lemma_ =="be":
                    abv = token.text
                    abv2 = token.lemma_
                    abV = abv.replace('2vvv','')
                    abV2= abv2.replace('2vvv','')
                   # print('abV',abV)
                else:
                    try:
                        if token.text == "back" or token.text in myBA:
                            ab1 = token.text
                            ab = ab1
                        elif token.text == "again" or token.text in myBA:
                            ab1 =  token.text
                            ab = ab1
                    except:
                        if token.text == "back":
                            ab1 = token.text
                            ab = ab1
                        elif token.text == "again":
                            ab1 =  token.text
                            ab = ab1
            #print(abV, abV2,ab)  # visited, visit, back 
            if myBAverb:  # my own abverbs 
                #print('yes')
                if len(abV)>1 and any([x in abV2 for x in myBAverb]): # changed len(abV)>1 and abV2 in myBA: 09.10.2022
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print(abd1)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print(abd2)
                    abd2 = re.sub(r'\b' +ab + r'\b',"", abd2) 
                    abtext = abtext.replace(abd.text,abd2)
                    ab_verbs.append(ab_verb)
                    
            else:
                if len(abV)>1:
                    #print(abd)
                    abd1 = abd.text.replace('2vvv',"")
                    #print('abd' , abd)
                    ab_verb = abV2 +ab +'2vvv'
                    mapverb(ab_verb)  
                    abd2 =  re.sub(r'\b' +abV + r'\b',ab_verb, abd1)  # replace whole word 
                    #print('abd2', abd2)
                    abd2 = re.sub(r'\b' +ab + r'\b',"", abd2) 
                    abtext = abtext.replace(abd.text,abd2)
                    #print('abtext1',abtext)
                    ab_verbs.append(ab_verb)                  
            
        return abtext, ab_verbs 
    else:
        return abtext, []
      
if __name__ == "__main__":
  print('ok')