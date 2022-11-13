
KeypartX: a graph-based approach to represent perception (text in general) by key parts of speech. KeypartX solved the coherence crux that current topic modeling algorithms are trying to deal with but failed. KeypartX extract the topics from text corpus syntactically, semantically and pragmatically instead of a meaningless combination of words from topic modeling.

## Installation

```bash
if need coreferee: 
 pip install keypartx[coreferee_spacy] 
 python3 -m coreferee install en 
 python -m spacy download en_core_web_lg 

else:
 pip install spacy 
 pip install keypartx  
 python -m spacy download en_core_web_lg
```


## Getting Started
For an in-depth overview of the features of KeypartX
you can check the [**Documents**](https://medium.com/@egalitrans/topic-modeling-is-dead-long-live-keypartx-a1998a94a0b0) or you can follow along 
with one of the examples as follows:

| Name  | Link  |
|---|---|
| KeypartX Quick Start | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1hjAU-_RP7GGzMm6rnpdJZR7LSY0KS81E?usp=sharing) |
| KeypartX with Real Example  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VdKIJtMMcYRnXsne87azY7B1FXp9FpD1?usp=sharing)  |
| KeypartX VS Topic Modelling |  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14XvylCMBZ2oUnjpZhnf_658paVdvAhp0?usp=sharing) |
| KeypartX Network Comparison |  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1vTx9LwIGXt5so5IdOr4zsqrgSm4sHnYe?usp=sharing)  |

## Visualization Examples 
* 1 NLP Target  

Original sentence: """Thai food was great,delicousr and not expensive, we loved it. We visited 3 beach resorts, they are higly recommened... We had "Fire-Vodka" !!!"""

<img src="https://github.com/pengKiina/KeypartX/raw/main/images/nlp_target.png" width="70%" height="35%" align="center" />


* 2 Community and Gray Perceptual Unit Networks 

<img src="https://github.com/pengKiina/KeypartX/raw/main/images/community_gray.gif" width="70%" height="45%" align="center" />

## Citation
To cite the [KeypartX paper](https://arxiv.org/abs/2209.11844), please use the following bibtex reference:

```bibtext
@article{pengyang2022keypartx,
  title={KeypartX: Graph-based Perception (Text) Representation},
  author={Peng, Yang},
  journal={arXiv preprint arXiv:2209.11844},
  year={2022}
}
```
