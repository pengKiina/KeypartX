from keypartx.basemodes.avn_base import countFreq
import pandas as pd

import leidenalg as la
import igraph as ig 
import networkx as nx

from matplotlib import colors as cls
#import matplotlib
import numpy as np
from scipy.stats import chisquare as cs

## --- Edges function --- ## 

def dirNN(allNNedges):
    revNNedges=[]
    for nne in allNNedges:
        a = nne[0]
        b = nne[1]
        revNNedges.append([b,a])
    allNNEdges_dir = revNNedges + allNNedges
    return allNNEdges_dir

def weighted_edges(all_edges):
  all_edges1 = [tuple(x) for x in all_edges]
  edge_df = countFreq(all_edges1,'edge')
  all_edges_count = edge_df .shape[0]
  weighted_edges = []
  nodes0= []
  nodes1= []
  weighted_edgesDICT = []
  for edge,edge_freq in zip(edge_df.edge.to_list(), edge_df.edge_freq.to_list()):
    row = (edge[0],edge[1],edge_freq )
    node0 = edge[0]
    node1 = edge[1]
    nodes0.append(node0)
    nodes1.append(node1)
    weighted_edges.append(row)
    weighted_edgesDICT.append({'node1':edge[0],'node2':edge[1],'weight':edge_freq} )
  nodes = nodes0 +nodes1
  weighted_edgesDF = pd.DataFrame(weighted_edgesDICT)
  return weighted_edges, edge_df, nodes,weighted_edgesDF


def k_edges(all_edges,weight_k =1):
  all_edges_k =[]
  for edge in all_edges:
    if edge[2]>= weight_k:
      all_edges_k.append(edge)
  return all_edges_k

def wedge_type(all_adjV2N_edges_w=[],allNNEdges_dir_w=[],nn_edges = True, aVn_edges = True,weight_k =1):
    """ weight_k: drop all edges if weight less than k 
    """
    include_nn_not =""
    all_edges1 = []
    if nn_edges == True and aVn_edges == True:
        all_edges0 = all_adjV2N_edges_w  + allNNEdges_dir_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'avN_N edges wight_k = {}'.format(weight_k)
    elif aVn_edges:
        all_edges0 = all_adjV2N_edges_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'avN edges wight_k = {}'.format(weight_k)
    else:
        all_edges0 =allNNEdges_dir_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'NN edges wight_k = {}'.format(weight_k)
    return all_edges1, include_nn_not
   
   


## --- Partition --- ## 

def parti(all_edges,com_resolution=1):
    Gdc = nx.DiGraph() 
    #all_edges = all_adjV2N_edges_w  + allNNEdges_dir_w
    Gdc.add_weighted_edges_from(all_edges)
    print('length of nodes:',len(Gdc.nodes))
    #print(Gdc.nodes)


    weights = []
    for edge in all_edges:
      weights.append(edge[2])

    iGd = ig.Graph.from_networkx(Gdc)
    iGd.vs["name"] = iGd.vs["_nx_name"] # keep the networkx name instead of numbers 
    del(iGd.vs["_nx_name"])
    partition = la.find_partition(iGd, la.RBConfigurationVertexPartition, weights = weights,resolution_parameter = com_resolution)#max_comm_size=10 # the smaller resolution, the fewer community but bigger size
  
    comNUM = []
    nodeNames = []
    for i,pt in enumerate(partition):
      #print(i,pt)
      pt_names = [iGd.vs[index]['name'] for index in pt]
      nodeNames.append(pt_names)
      comNUM.append(i)
    comDF = pd.DataFrame({'community_No':comNUM,'nodes':nodeNames})
    
    return partition,iGd,Gdc,comDF


## ---Color setting for community network ---##

def colorsList(colorL = False):
    if colorL == False:
        colorList = ['darkred','gold','blue','orange','green','purple','lime']
    else:
        colorList = colorL
    colorList_rgba = []
    for color in colorList:
      colorList_rgba.append(list(cls.to_rgba(color)))
    #print(colorList_rgba)
    colorList_rgba1= []
    for i,a in enumerate(np.arange(.01,1,0.05)[::-1]): # do not start with 0 alpha will be no color,  reverse the order 
      for colors in colorList_rgba:
        if i <len(colorList):
          colors[-1]= 1
        else:
          colors[-1]= a
          #print(colors)
        colors1 = cls.to_hex(colors, keep_alpha=True)
      
        colorList_rgba1.append(colors1)
    return colorList_rgba1


# gray unit network to sentence by order of degree and weight

class unit2sent:
  """community nodes: {('food2nnn',5),('good2aaa',2),('love2vvv',3)}
     community edges:{('good2aaa','food2nnn',2),('love2nnn','food2vvv',3)}
     ncR: core noun degree/ core nouns degree sum
     vdR: verb to core noun edge/ verbs to core noun edges sum
     adR: adjective to core noun edge/ adjectives to core noun edges sum
     ndR: noun to core noun edge/ nouns to core noun edges sum
     """   
  def __init__(self, commu_nodes,commu_edges):
    self.commu_nodes =  commu_nodes
    self.commu_edges = commu_edges

  # 1. core nouns in community 

  def corenoun(self,ncR=.01):
    commu1_nodes = self.commu_nodes
    nnodes = []
    ndegrees =[]
    for node in commu1_nodes:
      if 'nnn' in node[0]:
        nnodes.append(node[0])
        ndegrees.append(node[1])
        
    cn_nodeDF = pd.DataFrame({'cn_nodes':nnodes,'cn_degrees':ndegrees})
    cn_nodeDF = cn_nodeDF.sort_values(by='cn_degrees',ascending= False)

    noun_cores0 = cn_nodeDF.cn_nodes.to_list()
    noun_coresD = cn_nodeDF.cn_degrees.to_list()
    #ncR = .1
    core_nouns= []
    core_nounsD =[]
    for nc,ncd in zip(noun_cores0,noun_coresD):
      nrc = ncd/sum(noun_coresD)
      if nrc>ncR:
        core_nouns.append(nc)
        core_nounsD.append(ncd)
    return core_nouns,core_nounsD


  ## 2. avn order by degree

  def avn2coren(self,c_noun,c_nounD=False,vdR = .1, adR =.1,ndR =.1):
    """ 
    verb(weight to core noun), 
    adjective(weight to core noun) and
    noun(weight to core noun) edges to core_noun in list of list 
    
    """
    commu1_edges = self.commu_edges
    avns =[]
    avnWs = []
    avnPs =[]
    for edge in commu1_edges:
      if c_noun == edge[1]:
        avn = edge[0]
        if 'nnn' in avn:
          avnP ='NOUN'
        elif 'aaa' in avn:
          avnP ="ADJ"
        elif 'vvv' in avn:
          avnP ="VERB"
        avnW= edge[2]
        avns.append(avn)
        avnWs.append(avnW) # edge weight 
        avnPs.append(avnP)

    avnDF = pd.DataFrame({'avns':avns,'avnWs':avnWs,'avnPs':avnPs})

    verbDF = avnDF[avnDF['avnPs'] == 'VERB']
    verbDF = verbDF.sort_values(by ='avnWs', ascending = False)

    nounDF = avnDF[avnDF['avnPs'] == 'NOUN']
    nounDF = nounDF.sort_values(by ='avnWs', ascending = False)

    adjDF = avnDF[avnDF['avnPs'] == 'ADJ']
    adjDF =  adjDF.sort_values(by='avnWs', ascending = False)


    verbs = verbDF.avns.to_list()
    verbsD = verbDF.avnWs.to_list()

    nouns = nounDF.avns.to_list()
    nounsD = nounDF.avnWs.to_list()

    adjs = adjDF.avns.to_list()
    adjsD = adjDF.avnWs.to_list()

    c_noun1 = c_noun.replace('2nnn','')
    #vdR = 0.4
    #adR = 0.2
    #ndR = 0.1
    vlist =[]
    knWedge_vs= []
    for v, vd in zip(verbs,verbsD):
        vdr = vd/sum(verbsD)
        if vdr> vdR:
          v1 = v.replace('2vvv',"")
          vlist.append((v1 + "(" + str(vd) +")"))
          knWedge_v = (v,c_noun,vd)
          knWedge_vs.append(knWedge_v)
    alist = []
    knWedge_as= []
    for a, ad in zip(adjs,adjsD):
        adr = ad/sum(adjsD)
        if adr>adR:
          a1 = a.replace('2aaa',"")
          alist.append((a1 + "(" + str(ad) +")"))
          knWedge_a = (a,c_noun,ad)
          knWedge_as.append(knWedge_a)
    nlist = []
    knWedge_ns = []
    for n, nd in zip(nouns,nounsD):
        ndr = nd/sum(nounsD)
        if ndr> ndR:
          n1 = n.replace('2nnn',"")
          nlist.append((n1 + "(" + str(nd) +")"))
          knWedge_n = (n,c_noun,nd)
          knWedge_ns.append(knWedge_n)
    if c_nounD:
      avn2cn = {c_noun1 +"(" + str(c_nounD) +")": [vlist,alist,nlist]}
    else:
      avn2cn = {c_noun1: [vlist,alist,nlist]}
      print('{} degree NOT added'.format(c_noun))
    knWedges = knWedge_vs + knWedge_as + knWedge_ns
    return  avn2cn,knWedges
  
  
  
  
# find specific nodes or edges for compare networks in two set 


#import pandas as pd
#from scipy.stats import chisquare as cs
#Pearson's chi-squared test
def x2(key0= 90, key1= 9, other0= 110,other1 = 11):
    #key0 = 90  target kewords frequence
    #key1 = 9   reference keywords frequence
    #other0 = 110 other words number in target doc
    #other1 = 11  other words number in reference doc 

    key_all =  key0 + key1
    other_all = other0 + other1

    doc0_all = key0 + other0
    doc1_all = key1 + other1 

    all_all = doc0_all + doc1_all

    data = {'keyword':[key0, key1, key_all], 
            'others':[other0, other1,other_all],
           'total words':[doc0_all,doc1_all,all_all]} 
    df = pd.DataFrame(data,index = ['doc0','doc1','total'])

    obs=[key0,other0,key1,other1]
    exp1= doc0_all*key_all/all_all
    exp2=doc0_all*other_all/all_all
    exp3= doc1_all*key_all/all_all
    exp4= doc1_all*other_all/all_all

    exp=[exp1,exp2,exp3,exp4]
    
    #print(obs,exp)

    x2 = cs(obs,f_exp=exp)
    pvalue = x2.pvalue
    #if pvalue >0.01:
       # print('No Significant')
    return pvalue 
#You use chisquare when you want to test whether one (discrete) random variable has a specific distribution. Null hypothesis: the random variable is not significantly different from the specified distribution.

def specItem_deprecated(rovaEMO,turkuEMO,listName1 = "rovaEMO",listName2 = "turkuEMO"):
    """ 
     keys are the key items in sameItems through X2 method, turkuEMOdf1 is the frequency of same items in turku list, specItermsTurku1 is the sepcific items from Rova.
    
    """
    sameItems = list(set(rovaEMO).intersection(turkuEMO))
    specItermsRova = [ x for x in rovaEMO if x not in sameItems]
    specItermsTurku = [ x for x in turkuEMO if x not in sameItems]
    
    rovaEMOdf = countFreq(rovaEMO,listName1)
    rovaEMOdf1 = rovaEMOdf.apply(lambda row: row[rovaEMOdf[listName1].isin(sameItems)])
    
    turkuEMOdf = countFreq(turkuEMO,listName2)
    turkuEMOdf1 = turkuEMOdf.apply(lambda row: row[turkuEMOdf[listName2].isin(sameItems)]) # same item frequency in turku 
    #print(rovaEMOdf1,turkuEMOdf1)
   
    keysRova = []
    keysTurku = []
    for key in sameItems:
        list1freq = listName1 +'_freq'
        
        keyRova = rovaEMOdf1[rovaEMOdf1[listName1] == key][list1freq].to_list()[0]
        otherRova = sum(rovaEMOdf1[list1freq]) - keyRova 
        
        list2freq = listName2 +'_freq'
        keyTurku = turkuEMOdf1[turkuEMOdf1[listName2] == key][list2freq].to_list()[0]
        otherTurku = sum(turkuEMOdf1[list2freq]) - keyTurku
        #print(key,keyRova0,keyRova1)
        pvalue1 = x2(key0= keyRova, key1= keyTurku, other0= otherRova,other1 = otherTurku)
        if pvalue1 <0.05:
            keysRova.append(key)
            print( key,":",pvalue1)
        pvalue2 = x2(key0= keyTurku, key1= keyRova, other0= otherTurku ,other1 = otherRova)
        if pvalue2 <0.05:
            keysTurku.append(key)       
            #print(key,pvalue2)
    
    specItermsRova1 = countFreq(specItermsRova,listName1)
    specItermsTurku1 = countFreq(specItermsTurku, listName2)
    return  sameItems, keysRova, rovaEMOdf1 , turkuEMOdf1, specItermsRova1 ,specItermsTurku1
    # keys are the key items in sameItems, turkuEMOdf1 is the frequency of same items in turku list, specItermsTurku1 is the sepcific items from Rova. 
    # keyRova and keysTurku are the same 
    
    
def specItem(rovaEMO,turkuEMO,listName1 = "rovaEMO",listName2 = "turkuEMO"):
    """ 
     keys are the key items in sameItems through X2 method, turkuEMOdf1 is the frequency of same items in turku list, specItermsTurku1 is the sepcific items from Rova.
    
    """
    sameItems = list(set(rovaEMO).intersection(turkuEMO))
    specItermsRova = [ x for x in rovaEMO if x not in sameItems]
    #print(specItermsRova)
    specItermsTurku = [ x for x in turkuEMO if x not in sameItems]
    listName1a =  listName1 + '_common'
    listName1b =   listName1 + '_unique'
    listName2a =  listName2 + '_common'
    listName2b =  listName2 + '_unique'
    rovaEMOdf = countFreq(rovaEMO,listName1a)
    rovaEMOdf1 = rovaEMOdf.apply(lambda row: row[rovaEMOdf[listName1a].isin(sameItems)])
    
    turkuEMOdf = countFreq(turkuEMO,listName2a)
    turkuEMOdf1 = turkuEMOdf.apply(lambda row: row[turkuEMOdf[listName2a].isin(sameItems)]) # same item frequency in turku 
    #print(rovaEMOdf1,turkuEMOdf1)
   
    keysRova = []
    keysTurku = []
    for key in sameItems:
        list1freq = listName1a +'_freq'
        
        keyRova = rovaEMOdf1[rovaEMOdf1[listName1a] == key][list1freq].to_list()[0]
        otherRova = sum(rovaEMOdf1[list1freq]) - keyRova 
        
        list2freq = listName2a +'_freq'
        keyTurku = turkuEMOdf1[turkuEMOdf1[listName2a] == key][list2freq].to_list()[0]
        otherTurku = sum(turkuEMOdf1[list2freq]) - keyTurku
        #print(key,keyRova0,keyRova1)
        pvalue1 = x2(key0= keyRova, key1= keyTurku, other0= otherRova,other1 = otherTurku)
        if pvalue1 <0.05:
            keysRova.append(key)
            print( key,":",pvalue1)
        pvalue2 = x2(key0= keyTurku, key1= keyRova, other0= otherTurku ,other1 = otherRova)
        if pvalue2 <0.05:
            keysTurku.append(key)       
            #print(key,pvalue2)
    
    specItermsRova1 = countFreq(specItermsRova,listName1b)
    specItermsTurku1 = countFreq(specItermsTurku, listName2b)
    return  sameItems, keysRova, rovaEMOdf1 , turkuEMOdf1, specItermsRova1 ,specItermsTurku1
    # keys are the key items in sameItems, turkuEMOdf1 is the frequency of same items in turku list, specItermsTurku1 is the sepcific items from Rova. 
    # keyRova and keysTurku are the same 
    




#  
