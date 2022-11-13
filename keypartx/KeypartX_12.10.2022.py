
from IPython.core.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.physics import Physics
from pyvis.network import Network
import time,re,spacy,itertools
from keypartx.basemodes.text_edges import text2edges, opi_verbs,neg_words,nounDEL,adjDEL
import pandas as pd 
import math, matplotlib
from itertools import cycle, islice
from keypartx.basemodes.avn_base import nlp




## -- avnn edges-- ##
def avnn(line_en,by_review = False,other_edges = True,verbose_text = False,only_otherNouns = False, only_opiAV = True, nncompound = True, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=False,faciNN = False, emojis = True, emojiINtext= False , check_spell = True,back_again = True,myBA = False,myBAverb = False):
    """
    line_en:  string of english review 
    include_otherEdge: greedy edges of the unmatched adj, verb, noun 
    only_otherNouns: does not have adjverb in other2N_edges other than av2n, the other2N_edeges are greedy to mach the rest adj, verb, noun instead of considering match pattern
    nounDEL : nouns to be removed 
    adjDEL : adjective to be removed 
    facility: additional noun for the missing in the include_otherEdge class, e.g. I recommend! So pretty! 
    faciNN: add facility noun to NN edges, otherwise facility only add to AV2N in the otherEdges other than facilty-N in the matched AV2N to form greedy NN 
    emojis: if true, it will return a list of emojis in text, otherwise dropped 
    emojiINtext: if ture, it will tranform emojis as noun words as part of the whole text # I love 🎅 --- I love santa_claus 
    back_again:  visit, come, go, travel, be and others verbs 
    myBAverb: if false means all verbs other you can you own abverbs ['visit', 'come','go', 'travel', 'be'] to add 'back','again'
    myBA: if false ['back','again']
    """
    time_start = time.time()
    all_adjV2N_edges = []
    allNNedges = [] # noun to noun is the noun in adjV2N 
    all_new_nodes= []
    all_old_nodes= []
    new_node_nouns= []
    new_node_verbs= []
    new_node_adjs= []
    emojis1 = []

    """    by_review = False # by review or by sentence in review
        #opinion_verbs = False
        other_edges = True # not match verb, adj, noun
        verbose_text = False
        only_opiAV = True
        only_otherNouns =only_otherNouns
        nncompound = True"""
    
    sent_i = 0 

    try:
        line = line_en.replace('\n','') # remove new line in the paragraph
        line = line.replace('\t','')
        line1 = re.sub('[:@#$+=%*`)(><]', ' , ', line)
        #line1 = re.sub(r'\b\d+\b', ' ', line1)
        line1 = re.sub(" \d+", "  ", line1)
        time.sleep(.5)
        line1 = re.sub(r'\b' + "th" + r'\b', ' ', line1) 
        line1 = line1.replace("."," . ") # in case: it is great.the food become a word of great.the
        line1 = line1.replace("!"," . ") # in case: it is great.the food become a word of great.the
        line1 = line1.replace("?"," . ") # ?,!, . for the sentence dependency 
        #line1 = line1.replace("’","'")
        line1 = re.sub(u"(\u2018|\u2019)", "'", line1)
        line1 = re.sub(' +', ' ', line1).strip() #remove extra space whitespace 
        print('line:', line1)
        if by_review:
            all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0,emojis0 = text2edges(line1,verbose= False, verbose_text = verbose_text,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=facility,faciNN=faciNN,emojis = emojis,  emojiINtext = emojiINtext,  check_spell = check_spell,back_again = back_again,myBA = myBA,myBAverb = myBAverb)
            #all_adjV2N_edges, allNNedges, all_adjV2N_edges_drop, all_new_nodes, all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs
            allNNedges.extend(allNNedges0)
            all_adjV2N_edges.extend(all_adjV2N_edges0)
            all_new_nodes.extend(all_new_nodes0)
            all_old_nodes.extend(all_old_nodes0)
            new_node_nouns.extend(new_node_nouns0)
            new_node_verbs.extend(new_node_verbs0)
            new_node_adjs.extend(new_node_adjs0)
            emojis1.extend(emojis0)
        else:
            for ib,sent in enumerate(nlp(line1).sents):   # dependency parse https://spacy.io/usage/linguistic-features#sbd sentence
                #print(sent)
                
                if len(sent.text.split())>2: # minimal 2 words
                    sent_i += 1
                    print('sentence' + str(ib),sent.text)
                    all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0,emojis0 = text2edges(sent.text,verbose_text = verbose_text,verbose = False,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=facility,faciNN=faciNN,emojis = emojis, emojiINtext = emojiINtext  , check_spell = check_spell,back_again = back_again,myBA = myBA,myBAverb = myBAverb)
                    
                    allNNedges.extend(allNNedges0)
                    all_adjV2N_edges.extend(all_adjV2N_edges0)
                    all_new_nodes.extend(all_new_nodes0)
                    all_old_nodes.extend(all_old_nodes0)
                    new_node_nouns.extend(new_node_nouns0)
                    new_node_verbs.extend(new_node_verbs0)
                    new_node_adjs.extend(new_node_adjs0)
                    emojis1.extend(emojis0)
    except:
        print('---sth wrong ---')
    
    print('processing time:', time.time()-time_start)
    print('length of sentences:',sent_i)
    return all_adjV2N_edges,allNNedges,all_new_nodes,all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs,emojis1,sent_i


  
# comments_en list 
def avnn2(comments_en,by_review = False,other_edges = True,verbose_text = False,only_otherNouns = False, only_opiAV = True, nncompound = True, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=False,faciNN = False, emojis = True,check_spell = True,back_again = True,myBA = False,myBAverb = False):
    """
    comments_en:  list of text 
    include_otherEdge: greedy edges of the unmatched adj, verb, noun 
    only_otherNouns: does not have adjverb in other2N_edges other than av2n, the other2N_edeges are greedy to mach the rest adj, verb, noun instead of considering match pattern
    nounDEL : nouns to be removed 
    adjDEL : adjective to be removed 
    facility: additional noun for the missing in the include_otherEdge class, e.g. I recommend! So pretty! 
    faciNN: add facility noun to NN edges, otherwise facility only add to AV2N in the otherEdges other than facilty-N in the matched AV2N to form greedy NN 
    emojis: if true, it will return a list of emojis in text, otherwise dropped 
    back_again:  visit, come, go, travel, be and others verbs 
    myBAverb: if false means all verbs other you can you own abverbs ['visit', 'come','go', 'travel', 'be'] to add 'back','again'
    myBA: if false ['back','again']
    """
    time_start = time.time()
    all_adjV2N_edges = []
    allNNedges = [] # noun to noun is the noun in adjV2N 
    all_new_nodes= []
    all_old_nodes= []
    new_node_nouns= []
    new_node_verbs= []
    new_node_adjs= []
    emojis1 = []

    """    by_review = False # by review or by sentence in review
        #opinion_verbs = False
        other_edges = True # not match verb, adj, noun
        verbose_text = False
        only_opiAV = True
        only_otherNouns =only_otherNouns
        nncompound = True"""
    line_i = 0   
    sent_i = 0 
    for ia,line_ori in enumerate(comments_en):
        print(ia)
        line_i +=1
        try:
            line = line_ori.replace('\n','') # remove new line in the paragraph
            line = line.replace('\t','')
            line1 = re.sub('[:@#$+=%*`)(><]', ' , ', line)
            #line1 = re.sub(r'\b\d+\b', ' ', line1)
            line1 = re.sub(" \d+", "  ", line1)
            time.sleep(.5)
            line1 = re.sub(r'\b' + "th" + r'\b', ' ', line1) 
            line1 = line1.replace("."," . ") # in case: it is great.the food become a word of great.the
            line1 = line1.replace("!"," . ") # in case: it is great.the food become a word of great.the
            line1 = line1.replace("?"," . ") # ?,!, . for the sentence dependency 
            #line1 = line1.replace("’","'")
            line1 = re.sub(u"(\u2018|\u2019)", "'", line1)
            line1 = re.sub(' +', ' ', line1).strip() #remove extra space whitespace 
            print('line:', line1)
            if by_review:
                all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0,emojis0 = text2edges(line1,verbose= False, verbose_text = verbose_text,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=facility,faciNN=faciNN,emojis = emojis,check_spell = check_spell,back_again = back_again,myBA = myBA,myBAverb = myBAverb)
                #all_adjV2N_edges, allNNedges, all_adjV2N_edges_drop, all_new_nodes, all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs
                allNNedges.extend(allNNedges0)
                all_adjV2N_edges.extend(all_adjV2N_edges0)
                all_new_nodes.extend(all_new_nodes0)
                all_old_nodes.extend(all_old_nodes0)
                new_node_nouns.extend(new_node_nouns0)
                new_node_verbs.extend(new_node_verbs0)
                new_node_adjs.extend(new_node_adjs0)
                emojis1.extend(emojis0)
            else:
                for ib,sent in enumerate(nlp(line1).sents):   # dependency parse https://spacy.io/usage/linguistic-features#sbd sentence
                    #print(sent)
                    
                    if len(sent.text.split())>2: # minimal 2 words
                        sent_i += 1
                        print('sentence' + str(ib),sent.text)
                        all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0,emojis0 = text2edges(sent.text,verbose_text = verbose_text,verbose = False,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound, opi_verbs = opi_verbs ,neg_words = neg_words, nounDEL =nounDEL, adjDEL = adjDEL,facility=facility,faciNN=faciNN,emojis = emojis,check_spell = check_spell,back_again = back_again,myBA = myBA,myBAverb = myBAverb)
                        
                        allNNedges.extend(allNNedges0)
                        all_adjV2N_edges.extend(all_adjV2N_edges0)
                        all_new_nodes.extend(all_new_nodes0)
                        all_old_nodes.extend(all_old_nodes0)
                        new_node_nouns.extend(new_node_nouns0)
                        new_node_verbs.extend(new_node_verbs0)
                        new_node_adjs.extend(new_node_adjs0)
                        emojis1.extend(emojis0)
        except:
            print('---sth wrong ---')
        
    print('processing time:', time.time()-time_start)
    print('length of reviews:',line_i)
    print('length of sentences:',sent_i)
    return all_adjV2N_edges,allNNedges,all_new_nodes,all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs,emojis1


## -- avn network -- ## 
def keynet(all_edges1,heading='avN_N Network',core_K =1,plot_graph = True,save_add ="avnn.html",height='600px', width='100%',bgcolor='white',font_color="black", directed = True, notebook =True,cdn='remote'):
    """ all_edges1: weighted edges 
        core_k: if node degree is less than k then edge droped
        cdn=['remote','local'] more in pyvis 
    """
    # get Networkx 
    #import math
    Gd = nx.DiGraph() 
    #all_edges1 = all_adjV2N_edges_w + allNNEdges_dir_w
    Gd.add_weighted_edges_from(all_edges1)
    #print('length Gd nodes: ',len(Gd.nodes))
    print('length Gd edges: ',len(all_edges1))
    #print(Gd.nodes)


    # pyvis network plot 
    nt=Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed = directed, notebook =notebook,cdn_resources=cdn )
    nt.set_edge_smooth('cubicBezier')
    error_noeds =[]
    nodes = []
    values = []
    for node,degree in dict(Gd.degree).items():
      #degree = math.log(degree,100)
      degree1 = 0.01*degree
      color =""
      shape =""
      node1 = ""
      if 'vvv' in node:
        color = 'red'
        shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      elif 'aaa' in node:
        color = 'brown'
        shape = 'triangle'
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      elif 'nnn' in node:
        color = 'blue'
        shape = 'dot'
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      else:
        error_node = node
        #print(node)
        Gd.remove_node(error_node)  # remove error node
        error_noeds.append(error_node)
      nodes.append(node[:-2])
      values.append(degree)
      nt.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=degree1,color = color, shape =shape) #value=degree
    #nt.add_nodes(nodes, value = values)

    weights = []
    all_edges =[]              # get final all_edges after errors 
    for edge in all_edges1:
      if any(ern in edge for ern in error_noeds): 
        print(edge,':error edge removed')

      elif all([dict(Gd.degree)[node]>=core_K for node in edge[:2]]):         # core_k if node degree is less than k then edge droped         
        elabel = str(edge[2])
        value = int(edge[2])
        weights.append(edge[2])
        edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
        edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
        nt.add_edge(edge0,edge1, title = elabel,width = value)
        #nt.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
        all_edges.append(edge)
        
    print('length Gd nodes after error node removed:',len(Gd.nodes))
    print('all edges after k-core: ', len(all_edges))
    
    if plot_graph:
        nt.show_buttons(filter_=['physics']) 
        nt.show("network_avnn.html")
        display(HTML('network_avnn.html'))
    if save_add:      
        nt.save_graph(save_add)
    # all_edges after k-core of all_edges1
    return all_edges,Gd



## -- avn network colored by community 
def communet(partition,iGd,Gdc,all_edges,colorList_rgba1,plot_graph = True,save_add ="network_community.html",height='600px', width='100%',heading='Community Network', directed = True, notebook =True,cdn='remote'):
    #import matplotlib
    """ 
        cdn=['remote','local'] more in pyvis 
    """
    #from itertools import cycle, islice
    colorList1  = list(islice(cycle(colorList_rgba1),len(partition)))

    ntc=Network(height=height, width=width,heading=heading,bgcolor='white',font_color="black", directed = directed, notebook =notebook ,cdn_resources=cdn)
    ntc.set_edge_smooth('cubicBezier')
    #error_noeds =[]
    for com, color in zip(partition, colorList1):
      for index in com:
        
        node = iGd.vs[index]['name']
        #print(node)
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)

        if 'vvv' in node:
          shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree),color = color, value =10*degree, shape =shape) #value=degree

        elif 'aaa' in node:
          shape = 'triangle'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),color = color,value =10*degree, shape =shape) #value=degree
        elif 'nnn' in node:
          shape = 'dot'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=100*degree,color = color, shape =shape) #value=degree

    weights = []
    for edge in all_edges:
      elabel = str(edge[2])
      #value = int(edge[2])*.5
      value = math.log(int(edge[2]),2)
      #print(elabel)
      weights.append(edge[2])
      
      edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
      edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
      ntc.add_edge(edge0,edge1, title = elabel,width = value)
      #ntc.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
    if plot_graph:
        ntc.show_buttons(filter_=['physics'])  
        ntc.show('community_network.html')
        display(HTML('community_network.html'))
    if save_add:
        ntc.save_graph(save_add)
        


## --plot color by nouns in AVNN community --#

def communet_nnc(partition,iGd,Gdc,all_edges,colorList_rgba1,plot_graph = True,save_add = 'community_NNColors.html', height='600px', width='100%',heading='Community_NNColors',bgcolor='white',font_color="black", directed = True, notebook =True,cdn='remote'):
    #import matplotlib,itertools
    """ 
        cdn=['remote','local'] more in pyvis 
    """
    partition_all_names = [] 
    for index in partition:
        partition_all_names.append([iGd.vs[index]['name'] for index in index])

    #list2d_all =  [x for x in partition_all_names]
    #all_nodes_index =  list(itertools.chain(*list2d_all))
    all_nodes_index =  list(itertools.chain(*partition_all_names))

    nodes_NN_index = []
    for part in partition_all_names:
      part1 = [x for x in part if 'nnn' in x]
      nodes_NN_index.append(part1)

    #other_nodes = [x for x in all_nodes_index if x not in nodes_NN_index ]
    other_nodes = [x for x in all_nodes_index if x not in list(itertools.chain(*nodes_NN_index)) ]
    ## all com
    com_a = 0
    com_aa = []
    com_edges =[]
    com_nodes = []
    for com in partition_all_names :
      com_a += 1
      com_aa.append(com_a)
      edges = []
      nodes= []
      for node in com:
        #node = iGd.vs[index]['name']
        #print('nn',node)
        edge = Gdc.in_edges(node)
        edges.append(edge)
        nodes.append(node)
      com_edges.append(edges)
      com_nodes.append(nodes)

    ## nn com 
    colorList1  = list(islice(cycle(colorList_rgba1),len(nodes_NN_index )))

    ntc2 =Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed =directed, notebook =notebook,cdn_resources=cdn)
    ntc2.set_edge_smooth('cubicBezier')
    com_nn_a = 0
    com_nn_aa = []
    com_nn_edges =[]
    com_nn_nodes = []
    for com_nn, color_nn in zip(nodes_NN_index , colorList1):
      com_nn_a += 1
      com_nn_aa.append(com_nn_a)
      nn_edges = []
      nn_nodes= []
      for node in com_nn:
        
        #node = iGd.vs[index]['name']
        #print('nn',node)
        nn_edge = Gdc.in_edges(node)
        nn_edges.append(nn_edge)
        nn_nodes.append(node)
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)

        shape = 'dot'
        degree = dict(Gdc.degree)[node]
        title = node +':'+str(degree)
        ntc2.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color_nn, shape =shape) #value=degree
      com_nn_edges.append(nn_edges)
      com_nn_nodes.append(nn_nodes)
    for node in other_nodes:
        color = 'gray'
        #node = iGd.vs[index]['name']
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
        if 'vvv' in node:
          shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree),color = color, value =.1*degree, shape =shape) #value=degree
        elif 'aaa' in node:
          shape = 'triangle'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),color = color,value =.1*degree, shape =shape) #value=degree
        elif 'nnn' in node:
          shape = 'dot'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color, shape =shape) #value=degree



    weights = []
    for edge in all_edges:
      elabel = str(edge[2])
      #value = int(edge[2])*.5
      value = math.log(int(edge[2]),2)
      #print(elabel)
      weights.append(edge[2])

      edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
      edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
      ntc2.add_edge(edge0,edge1, title = elabel,width = value)

      #ntc2.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)

    if plot_graph:
        ntc2.show_buttons(filter_=['physics'])  
        ntc2.show('communityNNcolor.html')
        display(HTML('communityNNcolor.html'))
    if save_add:
        ntc2.save_graph(save_add)

    com_dict = []
    for com, edges,nodes in  zip(com_aa,com_edges,com_nodes):
        for edge,node in zip(edges,nodes):
            dict1 = {'community_nn':com,'edges':edge,'node':node}
            com_dict.append(dict1)
    nnColor_df = pd.DataFrame(com_dict)
    return nnColor_df



## -single community with gray connection -## 
def gray_unit(nnColor_df,Gdc,all_edges,comLen = False,plot_graph = False, save_folder='gray_units/',height='600px', width='100%',heading='Gray Unit Community Network',bgcolor='white',font_color="black", directed = True, notebook =True,cdn='remote'):
    """ 
        cdn=['remote','local'] more in pyvis 
    """    
    
    if comLen == False:
        com_len = len(set(nnColor_df.community_nn.to_list()))
    else:
        com_len = comLen
    
    commus= []
    colorEdges = []
    colorNodes = []
    grayEdges = []
    grayNodes = []
    
    for community_index in range(com_len):
      com_DF1 = nnColor_df[nnColor_df['community_nn'] == community_index +1]
      comNodes_ori = com_DF1.node.to_list()
      comEdges0 = com_DF1.edges.to_list()
      comNodes= []
      comEdges = []
      for edges in comEdges0:
        for edge in edges:
          comEdges.append(edge)
          for node in edge:
            comNodes.append(node)
      #print(len(comNodes))
      comNodes = sorted(set(comNodes))
      #print(len(comNodes))
      #print(len(comEdges))
      #print(len(set(comEdges)))
      comEdges = sorted(set(comEdges))

      ntc3=Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed = directed, notebook =notebook,cdn_resources=cdn)
      ntc3.set_edge_smooth('cubicBezier')


      for node in comNodes:
          color_v =""
          color_n = ""
          color_a =""
          if node in comNodes_ori:
            color_v = 'red'
            color_n ='blue'
            color_a ='brown'
          else:
            color_v = 'gray'
            color_n = 'gray'
            color_a = 'gray'
          

          #node = iGd.vs[index]['name']
          #node1 = node[:-2]
          node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
          if 'vvv' in node:
            shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree), value =.1*degree, color = color_v,shape =shape) #value=degree
          elif 'aaa' in node:
          
            shape = 'triangle'
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),value =.1*degree, color = color_a,shape =shape) #value=degree
          elif 'nnn' in node:
            shape = 'dot'
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color_n, shape =shape) #value=degree
            

      for edge in all_edges:
        for edge1 in comEdges:
          if edge1 == edge[:2]:
            elabel = str(edge[2])
            #value = int(edge[2])*.5
            value = math.log(int(edge[2]),2)
            #print(elabel)

            edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
            edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
            ntc3.add_edge(edge0,edge1, title = elabel,width = value)
            #ntc3.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
      if plot_graph:
        ntc3.show_buttons(filter_=['physics']) 
        if community_index == com_len-1: 
            ntc3.show(str(community_index) + '_gray_unit.html')
            display(HTML(str(community_index) + '_gray_unit.html'))
      if save_folder:
        ntc3.save_graph(save_folder+ '/{}.html'.format(community_index +1))

      # gray_color edges dataframe 
      gray_nodes = [x for x in comNodes if x not in comNodes_ori]
      gray_edges = []
      color_edges = []
      for edge in all_edges:
        for edge1 in comEdges:
          if edge1 == edge[:2]:
            if len(gray_nodes)>0:
              for node in gray_nodes:
                if node in edge1:
                  gray_edges.append(edge)
                else:
                  color_edges.append(edge)
            else:
              gray_edges = []
              color_edges.append(edge)

      color_nodes = comNodes_ori
      #if len(gray_nodes)<1:
        #gray_nodes = []
      #set(color_edges),set(color_nodes),set(gray_edges),set(gray_nodes)
      grayNodeDs= []
      for node in gray_nodes:
        degree = dict(Gdc.degree)[node]
        nodeD = (node,degree)
        grayNodeDs.append(nodeD)
      colorNodeDs = []
      for node in color_nodes:
        degree = dict(Gdc.degree)[node]
        nodeD = (node,degree)
        colorNodeDs.append(nodeD)      
    
      
      commus.append(community_index)
      colorEdges.append(set(color_edges))
      colorNodes.append(set(colorNodeDs))
      grayEdges.append(set(gray_edges))
      grayNodes.append(set(grayNodeDs))
    colorGrayDF = pd.DataFrame({'commus': commus,'colorEdges':colorEdges,'colorNodes':colorNodes,'grayEdges':grayEdges,'grayNodes':grayNodes})
    return colorGrayDF
  
if __name__ == "__main__":
  comments_en =["Once again a memorable visit to Arctic Light. Hearty staff, tasty breakfast (special mention of crispy waffles and rice porridge!), Clean and well-equipped room. Good bed. High quality and tastefully decorated. ❤️ We recommend and book your next stay at the Arctic Light Hotel. 😊"]
  comments_en = ["I love you. you are mine friend. I dont know"," you are right. I no no "]
  av2n, nn,new_nodes,old_nodes,nodesN,nodesV,nodesA,emojis = avnn(comments_en,by_review= False,verbose_text= True, emojis= True, check_spell= False)