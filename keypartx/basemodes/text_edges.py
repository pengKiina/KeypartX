
import pandas as pd
import re 
#import coreferee, spacy
#from spacy import displacy

from autocorrect import Speller
import re
from keypartx.basemodes.avn_base import *
from collections import defaultdict

import matplotlib.pylab as plt
import networkx as nx
#from matplotlib.pyplot import figure, text


## negative, conative verbs, non opinion adjective, arcticle, ordinal words


opi_verbs = ['enjoy','love','like','adore','avoid','revisit','desire','dislike','hate','wish','hope','appreciate','value','recommend','unrecommend','astonish','impress','please','satisfy','unsatisfy','surprise','mean','mind','overjoy', 'despair', 'disgust', 'attract', 'encourage', 'favour','favor', 'forget', 'remember','disappoint', 'discourage','fascinate',
            'dissatisfy', 'disinterest', 'interest', 'complain', 'compliment', 'suffer' , 'trust', 'distrust', 'praise','content','miss']

neg_words = ['hardly', 'scarcely','barely','no','not','none','neither','nor','never']
#keep_words2 = keep_words +opi_verbs + neg_words
#textneg = "I do not like you never know it be not really pretty, it means no money no girl, I hardly learn in the never nice school"
#text =""" I don't like this High-quality hotel, /the\ restaraunt food is so ugly and expensive, United states of America next time we will go to New York, "good-good"  the place called "long islands",but I never hate it, it was not pretty,so I don't recommend it."""

nounDEL = ['thing', 'things','issue', 'issues', 'part', 'parts','lot','lots', 'year', 'years', 'week', 'weeks', 'month','months', 'hour','hours', 'date', 'minute',  'minutes', 'one','ones','bit','bits','addition','variety']
adjDEL =["same","similar","different","another","other","half", "some", "several", "much", "all", "many", "whole","enough", "little", "sufficient", "most","least","few", "own","very","this", "that", "these", "those","each", "every","any","less","more","only",'next','previous','least','first','second','third','able','last','such','main','really','late','early','possible','due',] # number are deleted separtely 
#timedate = timedate0 + non_opi_adjs
#timedate.remove('pengy')
art_ordinal = ["a","an","the",'first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','elventh','twelvth','e','o']
# pengy repalce the num adj and detleted later , for example it is beautiful country and I have three kids if drop three with empty space, then [beautiful country kids]
"""       "quantitative": ["half", "some", "several", "much", "all", "many", "whole", "no", "enough", "little", "any", "sufficient", "none", "most", "few"],
        "demonstrative": ["this", "that", "these", "those"],
        "possessive": ["my", "his", "their", "your", "our", "mine", "his", "hers", "theirs", "yours", "ours"],
        "interrogative": ["which", "what", "whose"],
        "distributive": ["each", "every", "either", "neither", "any"],
        "article": ["a", "an", "the"],"""

def negADJ(neg_words,adjDEL):
  aa = neg_words
  bb = adjDEL + ['pengy','ok']
  #print(len(bb))
  non_opi_adjs1 = []
  for a in aa:
    for b in bb:
      ab= a+b
      non_opi_adjs1.append(ab)
  #print(len(non_opi_adjs1))
  non_opi_adjs = adjDEL +non_opi_adjs1 +['pengy','ok'] # pengy is a temperal adjective 
  #print(len(non_opi_adjs))
  return non_opi_adjs





def text2edges(text,verbose = False, verbose_text= False,include_otherEdge = False, only_otherNouns = False,only_opiAV = True, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,nncompound = False,facility = False,faciNN = False, emojis = True,emojiINtext = False, check_spell = True,back_again = True,myBA = False,myBAverb = False):
  """
  include_otherEdge: greedy edges of the unmatched adj, verb, noun 
  only_otherNouns: does not have adjverb in other2N_edges other than av2n, the other2N_edeges are greedy to mach the rest adj, verb, noun instead of considering match pattern
  nounDEL : nouns to be removed 
  adjDEL : adjective to be removed 
  facility: additional noun for the missing in the include_otherEdge class, e.g. I recommend! So pretty! 
  faciNN: if True add facility noun to all NN edges, otherwise facility only add to AV2N in the otherEdges other than facilty-N in the matched AV2N to form greedy NN 
  myBA: my own abverbs ['visit', 'come','go', 'travel', 'be'] + 'back', 'again' 
  """
  non_opi_adjs = negADJ(neg_words,adjDEL)
  
  
  # 1. check spelling 

  #from autocorrect import Speller
  # text2 = re.sub(r'\b' + token.text + r'\b'," ", text2)
  #line1 = re.sub(' +', ' ', line1).strip() #remove extra space whitespace 
  if emojis:
    text, emojis1 = emo(text, emojiINtext = emojiINtext)
  else:
    text, _= emo(text)
    emojis1 =[]
  
  if text.isupper():
    text = text.lower()
  
  ## --- check spelling ---##
  if check_spell:
    spell = Speller('en')
    text = spell(text) # restaraunt - restaurant
  else:
    text = text
    
  text = text.replace(r"/"," ")
  text1 = text.replace("\\"," ")
  text1 = re.sub(' +', ' ', text1).strip() #remove extra space whitespace 
  text1 = text1.replace("."," . ") # in case: it is great.the food become a word of great.the
  text1 = text1.replace("´","'") 
  #timedate = ['year','week','month','thing','things','years','weeks','months','date','hour','minute']
  for art in art_ordinal:
    text1 = re.sub(r'\b' + art + r'\b'," ", text1)
    text1 = re.sub(r'\b' + art.capitalize() + r'\b'," ", text1)
  for token in nlp(text1):
    if token.pos_ == "NUM":
      text1 = re.sub(r'\b' + token.text + r'\b',"    ", text1)  # space in case make new compund 
  for td in nounDEL:
    text1 =  re.sub(r'\b' + td + r'\b',"  ,  ", text1) 
    text1 =  re.sub(r'\b' + td.capitalize() + r'\b'," ,  ", text1) 
  if verbose_text:
    print('text1 clean:', text1)

  if facility:
    facility1 = facility +'2nnn' 
    print('facility1:',facility1)
    mapnoun(facility1)


  # 2. quote,hyphen, entity, n't

  # quote 
  quote0 ,quote1 = quote(text1)
  quote1 = [x+'2nnn' for x in quote1]
  # hyphen 
  hyphen0,hyphen1 = hyphen(text1)
  hyphen1 = [x+'2nnn' for x in hyphen1]
  # entity 
  entity0,entity1 = entity(text1)
  entity1 = [x +'2nnn' for x in entity1]
  # n't verb lemma
  ntverb0,ntverb1 = ntverb(text1)
  if verbose:
    print('nt verb:',ntverb0,ntverb1)
    print('quote:',quote0 ,quote1)
    print('hyphen:',hyphen0,hyphen1)
    print('entity:',entity0,entity1)
  # mapping new pos to noun
  mapnouns1 = quote1 + hyphen1 +entity1
  mapnouns1 = " ".join(mapnouns1)
  #print('mapnouns1',mapnouns1)
  mapnoun(mapnouns1)

  for old , new in zip(quote0+hyphen0+entity0 +ntverb0 ,quote1+hyphen1+entity1 + ntverb1):
    text1 = re.sub(r'\b' + old + r'\b',new,text1)
  if verbose_text:
    print('text1(update quote,hypen,entity): ', text1)


  #3. compound Noun, Coreference  

  text2a =  re.sub(r'"'," ", text1) #quoation double  
  #text2b =  re.sub(r"'"," ", text2a) #single double  
  """for ntv0,ntv1 in zip(ntverb0,ntverb1):
    text2b = re.sub(r'\b' + ntv0 + r'\b',ntv1,text2b)"""
  text2b = text2a.lower()
  text2b = lemma_noun(text2b)

  text2b = text2b.replace("'ve","have")  ## I've can not be lemmatized as I have 
  text2b = text2b.replace("'"," ")


  # noun compund
  if nncompound:
    ncomp0,ncomp1 = nnncomp(text2b)
    ncomp1 = [x+'2nnn' for x in ncomp1]  #'thai1nfood2n'
    if verbose == True:
        print('nn compound:',ncomp0,ncomp1) 
    text2c = re.sub(' +', ' ', text2b).strip() #remove extra space whitespace
    for old, new in zip(ncomp0,ncomp1):
      #print(old,new)
      text2c = re.sub(r'\b' + old + r'\b',new,text2c)
    mapnoun(" ".join(ncomp1))

    # coreference no lemmatize text 
    try:
      text2 = coref(text2c)
      if verbose_text:
        print('text2 correference: ', text2)
    except:
      text2 = text2c
      if verbose_text:
        print('text2 NO_correference: ', text2)
    #text2 = lemma_en(text2)


  else: 
    ncomp0,ncomp1 = [],[]  
    # coreference no lemmatize text 
    try:
      text2 = coref(text2b)
      if verbose_text:
        print('text2 correference: ', text2)
    except:
      text2 = text2b
      if verbose_text:
        print('text2: ', text2)
    #text2 = lemma_en(text2)



  #4. --- negverb, negadj --- 

  # neg adj compound
  negadj0 = []
  negadj1 = []
  for negword in neg_words:
    na0,na1 = negadj(text2,negword)
    #print(na0,na1)
    negadj0.extend(na0)
    negadj1.extend(na1)
  negadj1 = [x +'2aaa' for x in negadj1]

  # neg verb compound
  negverb0 = []
  negverb1 = []
  for negword in neg_words:
    na0,na1 = negverb(text2,negword)
    #print(na0,na1)
    negverb0.extend(na0)
    negverb1.extend(na1)
  negverb1 = [x+'2vvv' for x in negverb1]
  if verbose:
      print('neg-adj compound:',negadj0,negadj1)
      print('neg-verb compound:',negverb0,negverb1)

  ## --- mapping negadj negverb --- ##

  mapadj(" ".join(negadj1 +['ok','pengy']))# ok INTJ , 
  mapverb(" ".join(negverb1))
  
  

  text3 = text2
  for old, new in zip(negadj0+negverb0,negadj1+negverb1):
    text3 = re.sub(r'\b' + old + r'\b',new,text3)
  #quote1 + hyphen1 +entity1 + ncomp1 +negadj1 +negverb1
  if verbose_text:
    print('text3(update negadj,negaverb): ', text3)

  ## ---- back , again verb ---
  if back_again:
    text3,ba_verbs = abverb(text3,myBA = myBA,myBAverb = myBAverb)
    bavbs = [] 
    for vb in ba_verbs:
      vb1 = vb.replace('2vvv','')
      bavbs.append(vb1)
    opi_verbs = opi_verbs +bavbs  


  #5. except compounds, other normal words into ADJ, VERB, NOUN 

  all_new_comps = quote1 + hyphen1 +entity1 + ncomp1 +negadj1 +negverb1
  #print('all_new_comps:',all_new_comps)

  text3 = re.sub(' +', ' ', text3).strip() #remove extra space whitespace
  new_adjs = []
  new_nouns = []
  new_verbs = []
  old_adjs = []
  old_nouns = []
  old_verbs = []
  text4a= [x.text for x in nlp(text3)] # make the text split equal to nlp token, since if love. in split love. but in nlp will be love . 
  #print(len(text4a))
  text4 = " ".join(text4a)
  #print(len(text4.split()))
  text4 = text4.replace('-','') # -bedroom in case - still there


  all_new_comps1 = [x.lower() for x in all_new_comps]  # Tripadvisor entity will become tripadvisornnn after text2 lemma_en 
  all_new_comps1 = all_new_comps1 + all_new_comps +['be'] +ba_verbs
  for token in nlp(text4):
    if token.text not in all_new_comps1:

      if token.pos_ =="ADJ":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.lemma_ +'2aaa'
        text4 = " ".join(text4_list)
        mapadj(token.lemma_ +'2aaa'), 
        new_adjs.append(token.lemma_ +'2aaa')
        old_adjs.append(token.lemma_)
      elif token.pos_ == "NOUN":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.text +'2nnn'
        text4 = " ".join(text4_list)

        mapnoun(token.text +'2nnn'), 
        new_nouns.append(token.text +'2nnn')
        old_nouns.append(token.text)
      elif token.pos_ == "VERB":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.lemma_ +'2vvv'
        text4 = " ".join(text4_list)
        mapverb(token.lemma_ +'2vvv'), 
        new_verbs.append(token.lemma_ +'2vvv') 
        old_verbs.append(token.lemma_)          
  if verbose_text:
    print('text4(update other than conpound noun,adj,verb): ', text4)   


  #6.  only keep adj, verb, noun, punct and be 

  #only_opiAV = True

  text5 = lemma_en(text4)
  for token in nlp(text5):
    #print(token.text,token.pos_)
    if  token.text != "be" and len(token.text)<7 :
      text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

    elif lemma_en(token.text) =="have": # have looked to have look, have becomes adj otherwise havevvv will be kept
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)
    elif token.text != "be" and token.pos_ not in ['ADJ','NOUN','VERB','PUNCT']:
      try:
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
      except:
        text5 = text5.replace(token.text," ")
  for token in nlp(text5):
    if 'vvv' in token.text or 'aaa' in token.text or 'nnn' in token.text or 'be' in token.text or token.pos_ =="PUNCT":
      pass
    else:
      #print("pos changed token",token.text) # such as pretty will change from adv to adj
      text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
  text5 = re.sub(' +', ' ', text5).strip() #remove extra space whitespace 
  if verbose_text:
    print('text5:',text5)


  #  if keep only opi adj and verb
  cop_verbs=['be','get2vvv','taste2vvv','smell2vvv','sound2vvv','seem2vvv','feel2vvv','look2vvv','appear2vvv','remain2vvv' ]
  # passive voice(get,be) and copular linking verb (taste, smell, sound, seem ,feel,look,appear, get , remian)
  if only_opiAV:

    for token in nlp(text5):
      if token.text in cop_verbs:
        text5 = re.sub(r'\b' + token.text + r'\b',"be", text5)
      elif token.pos_ =='ADJ':
        for adj in non_opi_adjs:
          if adj == token.text.replace("2aaa",""):
            text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
      elif token.pos_ == 'VERB':
          if any(x in token.text for x in opi_verbs):
            pass
          else:
              text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

      elif 'pengy' in token.text:
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")  


  else:
    for token in nlp(text5):
      if 'pengy' in token.text:
        #print(token.text)
        text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

  if only_opiAV:
    print('text5(only_opiAV): ',text5)
  else:
    print('text5(aaa,vvv, nnn): ',text5)

  #7. match AdjN,NbeAdj,Nverb,verbN

  #include_otherEdge = False
  ## --- match AdjN,NbeAdj,Nverb,verbN ---#

  text5 = nonAcomaA(text5)

  adjNverbs2 = adjNVmatch(text5)
  #adjNverbs2 

  ## --- 1 adj verb noun edges ---
  adjV2N_edges, nn_edges = av2Nedge(adjNverbs2)
  print('adjV2N_edges', adjV2N_edges)

  nodes = []
  for edges in adjV2N_edges:
    for node in edges:
      nodes.append(node)


  ## --- 2 other words than the match aNv ---
  text6 = text5 
  #print(text6)

  noadjNV= ""
  if len(nodes)>0:
    for x in nodes:
      #text6 = text6.replace(x,"")
      text6 = re.sub(r'\b' + x + r'\b'," ", text6)
      noadjNV = text6
      #print('noadjNV',noadjNV)
  else:
    noadjNV = text6



  print('noadjNV',noadjNV)
  
  
  noadjV = []
  noN =[]
  for token in nlp(noadjNV):
    if token.pos_ in ['ADJ','VERB'] and len(token.text)>5: # and len(token.text)>5 added on 02-10.2022 , in case some emoji or short words 2vvv 
        noadjV.append(token.text)
    elif token.pos_ == 'NOUN' and len(token.text)>5:
        noN.append(token.text)
  noadjNV2 = noadjV + noN 
  noadjNV3 = " ".join(noadjNV2)
  if verbose:
    print('noadjNV3:' ,noadjNV3)
  
  if facility: 
    other2N_edges = []
    otherNN_edges = []
    for av in noadjV: # av other than av in av2n 
      if av != 'be':
        other2n_edge = [av,facility1]
        other2N_edges.append(other2n_edge)
    for n in noN: # n other than n in av2n 
      if n != 'be':
        otherNN_edge = (n,facility1)
        otherNN_edges.append(otherNN_edge) 
  else:
     other2N_edges, otherNN_edges = av2Nedge([noadjNV3])

  ## --- 3 all noun to noun set ---
  allnouns = []
  if faciNN and facility:
    text5 = text5 +" " + facility1
    print('faciNN', text5)
  else:
    text5 = text5
    
  for token in nlp(text5):
    if token.pos_ == 'NOUN' and token.text != 'be':  # in case be changed as noun
      #print(token.text)
      allnouns.append(token.text)
  allNN_edges0 = list(itertools.combinations(set(allnouns), 2))


  ##  --- all edges --- ## 
  if include_otherEdge:
    if only_otherNouns: # does not have other2N_edges but nn edges. does not have adjverb in other2N_edges other than av2n, the other2N_edeges are greedy to mach the rest adj, verb, noun instead of considering match pattern
      all_adjV2N_edges = adjV2N_edges
      allNNedges = allNN_edges0
    else:
      all_adjV2N_edges = adjV2N_edges+other2N_edges
      allNNedges = allNN_edges0 
  
  else:
    all_adjV2N_edges = adjV2N_edges
    allNNedges = nn_edges
  
  ## --- All Nodes old new, adj,noun,verb --- ##
  allnodes = []
  old_node_adjs = []
  old_node_nouns = []
  old_node_verbs = []
  new_node_adjs = []
  new_node_nouns = []
  new_node_verbs = []

  for edges in all_adjV2N_edges:
    for node in edges:
      allnodes.append(node)
      if 'aaa' in node:
        old_node_adj = node.replace('2aaa','')
        new_node_adj = node
        old_node_adjs.append(old_node_adj)
        new_node_adjs.append(new_node_adj)
      elif 'nnn' in node:
        old_node_noun = node.replace('2nnn','')
        old_node_noun = old_node_noun.replace('1nnn','')
        new_node_noun = node
        old_node_nouns.append(old_node_noun)
        new_node_nouns.append(new_node_noun)
      elif 'vvv' in node:
        old_node_verb = node.replace('2vvv','')
        new_node_verb = node
        old_node_verbs.append(old_node_verb)
        new_node_verbs.append(new_node_verb)
  all_old_nodes = old_node_adjs+old_node_nouns+old_node_verbs
  all_new_nodes = new_node_adjs+new_node_nouns+new_node_verbs
  return all_adjV2N_edges, allNNedges, all_new_nodes, all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs,emojis1





## --target_edges for target_plot


def targList(mylist):
  D = defaultdict(list)
  for i,item in enumerate(mylist):
      D[item].append(i)
  D = {k:v for k,v in D.items() if len(v)>1}
  for key in D.keys():
    for i in range(1,len(D[key])):
      node_index = D[key][i]
      mylist[node_index] = mylist[node_index] +str(i)
  return mylist


#from autocorrect import Speller
#from collections import defaultdict
def target2edges(text,verbose = False, verbose_text= False,include_otherEdge = False, only_otherNouns = False,opi_verbs = opi_verbs ,neg_words =neg_words,adjDEL = adjDEL,nounDEL = nounDEL,only_opiAV = True,nncompound = True, emojis = True,emojiINtext = False,  check_spell = True,back_again = True, myBA =False,myBAverb = False):
  non_opi_adjs = negADJ(neg_words,adjDEL)
  # 1. check spelling 

  #from autocorrect import Speller
  # text2 = re.sub(r'\b' + token.text + r'\b'," ", text2)
  #line1 = re.sub(' +', ' ', line1).strip() #remove extra space whitespace 
  if emojis:
    text, emojis2 = emo(text,emojiINtext = emojiINtext)
  else:
    text, emojis1 = emo(text)
    emojis2 =[]

  if text.isupper():
    text = text.lower()
  ## --- check spelling ---##
  
    ## --- check spelling ---##
  if check_spell:
    spell = Speller('en')
    text = spell(text) # restaraunt - restaurant
  else:
    text = text
  
  
  text = text.replace(r"/"," ")
  text1 = text.replace("\\"," ")
  text1 = re.sub(' +', ' ', text1).strip() #remove extra space whitespace 
  text1 = text1.replace("."," . ") # in case: it is great.the food become a word of great.the
  text1 = text1.replace("´","'") 
  #timedate = ['year','week','month','thing','things','years','weeks','months','date','hour','minute']
  for art in art_ordinal:
    text1 = re.sub(r'\b' + art + r'\b'," ", text1)
    text1 = re.sub(r'\b' + art.capitalize() + r'\b'," ", text1)
  for token in nlp(text1):
    if token.pos_ == "NUM":
      text1 = re.sub(r'\b' + token.text + r'\b',"   ", text1)  # space in case make new compund 
  for td in nounDEL:
    text1 =  re.sub(r'\b' + td + r'\b',"  ,  ", text1) 
    text1 =  re.sub(r'\b' + td.capitalize() + r'\b'," ,  ", text1) 
  if verbose_text:
    print('text1 clean:', text1)

  # 2. quote,hyphen, entity, n't

  # quote 
  quote0 ,quote1 = quote(text1)
  quote1 = [x+'2nnn' for x in quote1]
  # hyphen 
  hyphen0,hyphen1 = hyphen(text1)
  hyphen1 = [x+'2nnn' for x in hyphen1]
  # entity 
  entity0,entity1 = entity(text1)
  entity1 = [x +'2nnn' for x in entity1]
  # n't verb lemma
  ntverb0,ntverb1 = ntverb(text1)
  if verbose:
    print('nt verb:',ntverb0,ntverb1)
    print('quote:',quote0 ,quote1)
    print('hyphen:',hyphen0,hyphen1)
    print('entity:',entity0,entity1)
  # mapping new pos to noun
  mapnouns1 = quote1 + hyphen1 +entity1
  mapnouns1 = " ".join(mapnouns1)
  #print('mapnouns1',mapnouns1)
  mapnoun(mapnouns1)

  for old , new in zip(quote0+hyphen0+entity0 +ntverb0 ,quote1+hyphen1+entity1 + ntverb1):
    text1 = re.sub(r'\b' + old + r'\b',new,text1)
  if verbose_text:
    print('text1(update quote,hypen,entity): ', text1)


  #3. compound Noun, Coreference  

  text2a =  re.sub(r'"'," ", text1) #quoation double  
  #text2b =  re.sub(r"'"," ", text2a) #single double  
  """for ntv0,ntv1 in zip(ntverb0,ntverb1):
    text2b = re.sub(r'\b' + ntv0 + r'\b',ntv1,text2b)"""
  text2b = text2a.lower()
  text2b = lemma_noun(text2b)

  text2b = text2b.replace("'ve","have")  ## I've can not be lemmatized as I have 
  text2b = text2b.replace("'"," ")


  # noun compund
  if nncompound:
    ncomp0,ncomp1 = nnncomp(text2b)
    ncomp1 = [x+'2nnn' for x in ncomp1]  #'thai1nfood2n'
    if verbose == True:
        print('nn compound:',ncomp0,ncomp1) 
    text2c = re.sub(' +', ' ', text2b).strip() #remove extra space whitespace
    for old, new in zip(ncomp0,ncomp1):
      #print(old,new)
      text2c = re.sub(r'\b' + old + r'\b',new,text2c)
    mapnoun(" ".join(ncomp1))

    # coreference no lemmatize text 
    try:
      text2 = coref(text2c)
      if verbose_text:
        print('text2 correference: ', text2)
    except:
      text2 = text2c
      if verbose_text:
        print('text2: ', text2)
    #text2 = lemma_en(text2)

  else: 
    ncomp0,ncomp1 = [],[]  
    # coreference no lemmatize text 
    try:
      text2 = coref(text2b)
      if verbose_text:
        print('text2 correference: ', text2)
    except:
      text2 = text2b
      if verbose_text:
        print('text2: ', text2)
    #text2 = lemma_en(text2)


  #4. --- negverb, negadj --- 

  # neg adj compound
  negadj0 = []
  negadj1 = []
  for negword in neg_words:
    na0,na1 = negadj(text2,negword)
    #print(na0,na1)
    negadj0.extend(na0)
    negadj1.extend(na1)
  negadj1 = [x +'2aaa' for x in negadj1]

  # neg verb compound
  negverb0 = []
  negverb1 = []
  for negword in neg_words:
    na0,na1 = negverb(text2,negword)
    #print(na0,na1)
    negverb0.extend(na0)
    negverb1.extend(na1)
  negverb1 = [x+'2vvv' for x in negverb1]
  if verbose:
      print('neg-adj compound:',negadj0,negadj1)
      print('neg-verb compound:',negverb0,negverb1)

  ## --- mapping negadj negverb --- ##

  mapadj(" ".join(negadj1 +['ok','pengy']))# ok INTJ , 
  mapverb(" ".join(negverb1))

  text3 = text2
  for old, new in zip(negadj0+negverb0,negadj1+negverb1):
    text3 = re.sub(r'\b' + old + r'\b',new,text3)
  #quote1 + hyphen1 +entity1 + ncomp1 +negadj1 +negverb1
  if verbose_text:
    print('text3(update negadj,negaverb): ', text3)

 
  ## ---- back , again verb ---
  if back_again:
    text3,ba_verbs = abverb(text3,myBA = myBA,myBAverb = myBAverb)
    bavbs = [] 
    for vb in ba_verbs:
      vb1 = vb.replace('2vvv','')
      bavbs.append(vb1)
    opi_verbs = opi_verbs +bavbs  



  #5. ecept compounds, other normal words into ADJ, VERB, NOUN 

  all_new_comps = quote1 + hyphen1 +entity1 + ncomp1 +negadj1 +negverb1
  #print('all_new_comps:',all_new_comps)

  text3 = re.sub(' +', ' ', text3).strip() #remove extra space whitespace
  new_adjs = []
  new_nouns = []
  new_verbs = []
  old_adjs = []
  old_nouns = []
  old_verbs = []
  text4a= [x.text for x in nlp(text3)] # make the text split equal to nlp token, since if love. in split love. but in nlp will be love . 
  #print(len(text4a))
  text4 = " ".join(text4a)
  #print(len(text4.split()))
  text4 = text4.replace('-','') # -bedroom in case - still there


  all_new_comps1 = [x.lower() for x in all_new_comps]  # Tripadvisor entity will become tripadvisornnn after text2 lemma_en 
  all_new_comps1 = all_new_comps1 + all_new_comps +['be'] +ba_verbs
  for token in nlp(text4):
    if token.text not in all_new_comps1:

      if token.pos_ =="ADJ":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.lemma_ +'2aaa'
        text4 = " ".join(text4_list)
        mapadj(token.lemma_ +'2aaa'), 
        new_adjs.append(token.lemma_ +'2aaa')
        old_adjs.append(token.lemma_)
      elif token.pos_ == "NOUN":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.text +'2nnn'
        text4 = " ".join(text4_list)

        mapnoun(token.text +'2nnn'), 
        new_nouns.append(token.text +'2nnn')
        old_nouns.append(token.text)
      elif token.pos_ == "VERB":
        #print(token.i)
        text4_list = text4.split()
        text4_list[token.i] = token.lemma_ +'2vvv'
        text4 = " ".join(text4_list)
        mapverb(token.lemma_ +'2vvv'), 
        new_verbs.append(token.lemma_ +'2vvv') 
        old_verbs.append(token.lemma_)          
  if verbose_text:
    print('text4(update other than conpound noun,adj,verb): ', text4)   

  mylist = text4.split()
  targlist = targList(mylist)
  for newword in targlist:
    if 'aaa' in newword:
      mapadj(newword)
    elif 'vvv' in newword:
      mapverb(newword)
    elif 'nnn' in newword:
      mapnoun(newword)
  text4b = " ".join(targlist)

  #6.  only keep adj, verb, noun, punct and be 

  #only_opiAV = True

  text5 = lemma_en(text4b)
  for token in nlp(text5):
    #print(token.text,token.pos_)
    if  token.text != "be" and len(token.text)<7 :
      text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

    elif lemma_en(token.text) =="have": # have looked to have look, have becomes adj otherwise havevvv will be kept
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)
    elif token.text != "be" and token.pos_ not in ['ADJ','NOUN','VERB','PUNCT']:
      try:
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
      except:
        text5 = text5.replace(token.text," ")
  for token in nlp(text5):
    if 'vvv' in token.text or 'aaa' in token.text or 'nnn' in token.text or 'be' in token.text or token.pos_ =="PUNCT":
      pass
    else:
      #print("pos changed token",token.text) # such as pretty will change from adv to adj
      text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
  text5 = re.sub(' +', ' ', text5).strip() #remove extra space whitespace 
  if verbose_text:
    print('text5:',text5)


  #  if keep only opi adj and verb
  cop_verbs=['be','get2vvv','taste2vvv','smell2vvv','sound2vvv','seem2vvv','feel2vvv','look2vvv','appear2vvv','remain2vvv' ]
  # passive voice(get,be) and copular linking verb (taste, smell, sound, seem ,feel,look,appear, get , remian)
  if only_opiAV:

    for token in nlp(text5):
      if token.text in cop_verbs:
        text5 = re.sub(r'\b' + token.text + r'\b',"be", text5)
      elif token.pos_ =='ADJ':
        for adj in non_opi_adjs:
          if adj == token.text.replace("2aaa",""):
            text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")
      elif token.pos_ == 'VERB':
          if any(x in token.text for x in opi_verbs):
            pass
          else:
              text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

      elif 'pengy' in token.text:
        text5 = re.sub(r'\b' + token.text + r'\b'," ", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")  


  else:
    for token in nlp(text5):
      if 'pengy' in token.text:
        #print(token.text)
        text5 = re.sub(r'\b' + token.text + r'\b',"", text5)    #re.sub(r'\b' + "?" + r'\b'," ", "beach???room is ok")

  """  if only_opiAV:
      print('text5(only_opiAV): ',text5)
    else:
      print('text5(aaa,vvv, nnn): ',text5)
  """
  #7. match AdjN,NbeAdj,Nverb,verbN

  #include_otherEdge = False
  ## --- match AdjN,NbeAdj,Nverb,verbN ---#

  text5 = nonAcomaA(text5)

  adjNverbs2 = adjNVmatch(text5)
  adjNverbs2 

  ## --- 1 adj verb noun edges ---
  adjV2N_edges, nn_edges = av2Nedge(adjNverbs2)
  #print('adjV2N_edges', adjV2N_edges)

  nodes = []
  for edges in adjV2N_edges:
    for node in edges:
      nodes.append(node)


  ## --- 2 other words than the match aNv ---
  text6 = text5 
  #print(text6)

  noadjNV= ""
  if len(nodes)>0:
    for x in nodes:
      #text6 = text6.replace(x,"")
      text6 = re.sub(r'\b' + x + r'\b'," ", text6)
      noadjNV = text6
      #print('noadjNV',noadjNV)
  else:
    noadjNV = text6

  noadjNV2 = []
  for token in nlp(noadjNV):
    if token.pos_ in ['ADJ','NOUN','VERB']:
        noadjNV2.append(token.text)
  noadjNV3 = " ".join(noadjNV2)
  if verbose:
    print('noadjNV3:' ,noadjNV3)
  other2N_edges, otherNN_edges = av2Nedge([noadjNV3])

  ## --- 3 all noun to noun set ---
  allnouns = []
  for token in nlp(text5):
    if token.pos_ == 'NOUN' and token.text != 'be':  # in case be changed as noun
      #print(token.text)
      allnouns.append(token.text)
  allNN_edges0 = list(itertools.combinations(set(allnouns), 2))


  ##  --- all edges --- ## 
  if include_otherEdge:
    if only_otherNouns: # does not have other2N_edges other than av2n, the other2N_edeges are greedy to mach the rest adj, verb, noun instead of considering match pattern
      all_adjV2N_edges = adjV2N_edges
      allNNedges = allNN_edges0
    else:
      all_adjV2N_edges = adjV2N_edges+other2N_edges
      allNNedges = allNN_edges0
  
  else:
    all_adjV2N_edges = adjV2N_edges
    allNNedges = nn_edges
  
 
  return all_adjV2N_edges, allNNedges, text4b, emojis2





## --target plot --

def targetPlot(text_T, avnEdges,saveAdd =False,image_size = [10,2], font_size = 20, word_close = 5, arc_rad= -0.3):
  """green curve: Adjective2Noun,  red curve: Verb2Noun,  blue cure: Noun2Noun"""
  words = text_T.split()
  #figure(figsize=(10,9))
  fig, _ = plt.subplots()
  #fig.set_tight_layout(False)
  #plt.rcParams['axes.linewidth'] = 100

  plt.rcParams["figure.figsize"] = image_size
  plt.rcParams["figure.autolayout"] = True

  G = nx.DiGraph()

  #G.add_node('color represent v', pos=(1,19))
  startP = 1.5
  type1s = []
  for i, node in enumerate(words):
    
    
    if '2a' in node:
      type1 = node.replace('2aaa',"")
      if type1[-1].isnumeric():
        type1 = type1[:-1]
      color1 = 'green'
    elif '2v' in node:
      type1 = node.replace('2vvv',"")
      if type1[-1].isnumeric():
        type1 = type1[:-1]
      color1 = 'red'
    elif '2n' in node:
      type1 = node.replace('2nnn',"")
      if type1[-1].isnumeric():
        type1 = type1[:-1]
      color1 = 'blue'
    else:
      type1 = node
      if type1[-1].isnumeric():
        type1 = type1[:-1]
      color1 = 'black'
    type1s.append(type1)
    if 0 < i and i < len(words):
      #spaceL = (len(words[i-1]) + len(words[i]))/2
      spaceL = (len(type1s[i-1]) + len(type1s[i]))/2
      spaceN = spaceL/word_close
      startP += spaceN 

    #print(node)
    #print('startP:',startP)

    G.add_node(node,pos=(startP,20), type=type1,color =color1)
    
  for edge in avnEdges:
    edgestring = "".join(edge)
    if '2a' in edgestring:
      color1 = 'green'
      weight1 = 1
    elif '2v' in edgestring:
      color1 = 'red'
      weight1 = 1
    elif '2n' in edgestring: #22.09.2022
      edge0 = re.sub(r'[\d+]',"",edge[0])
      edge1 = re.sub(r'[\d+]',"",edge[1])
      if edge0 == edge1:
        color1 = 'None'
        weight1 =.0001
      else:
        color1 = 'blue'
        weight1 =.3
    else:
      color1 = 'black'
      weight1 =.3
    G.add_edge(edge[0],edge[1],color=color1,weight=weight1)
    #G.add_edge(b,c,color='b',weight=1)
    #G.add_edge(c,d,color='g',weight=1)

  pos=nx.get_node_attributes(G,'pos')

  #labels = {}
  nodes = G.nodes()
  nodes_col = [nodes[node]['color'] for node in nodes]


  '''pos_attrs = {}
  for node, coords in pos1.items():
      pos_attrs[node] = (coords[0], coords[1] + 0.08)'''
  #pos = pos_attrs
  #nx.draw(G, with_labels=True, connectionstyle="arc3,rad=0.4")
  node_attrs = nx.get_node_attributes(G, 'type')

  edges = G.edges()
  ecolors = [G[u][v]['color'] for u,v in edges]
  weights = [G[u][v]['weight'] for u,v in edges]
  nx.draw(G, pos, edge_color=ecolors,node_size = 1000,font_size =font_size,node_color='None',font_color ='black', width=weights,with_labels= True, labels = node_attrs,connectionstyle="arc3,rad={}".format(arc_rad),)
  if saveAdd:
    plt.savefig(saveAdd)
  else:
    plt.savefig('nlp_target.png') 
  plt.show()
  return type1s


