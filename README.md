[![PyPI - Python](https://img.shields.io/badge/python-v3.7+-blue.svg)](https://pypi.org/project/keypartx/)
[![docs](https://img.shields.io/badge/docs-Passing-green.svg)](https://github.com/pengKiina/KeypartX/)
[![PyPI - PyPi](https://img.shields.io/pypi/v/keypartx)](https://pypi.org/project/keypartx/)
[![PyPI - License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pengKiina/KeypartX/blob/main/LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-2203.05794-<COLOR>.svg)](https://arxiv.org/abs/2209.11844)
<a href="https://pypi.org/project/keypartx/"><img src="https://static.pepy.tech/badge/keypartx" alt="PyPi downloads"></a>

# KeypartX
<img src="https://github.com/pengKiina/KeypartX/raw/main/images/keypartx_logo.png" width="40%" height="20%" align="right" />

*  No more Topic Modeling
*  No need Training 
*  No more Machine Learning but Human-like Reading
*  Get the Insights of Text Big and Small

KeypartX: a graph-based approach to represent perception (text in general) by key parts of speech. KeypartX solved the coherence crux that current topic modeling algorithms are trying to deal with but failed. KeypartX extracts the topics from text corpus syntactically, semantically and pragmatically instead of a meaningless combination of words from topic modeling.


## Key Parts: Noun, Adjective, Verb and Emoji 

KeypartX Vs Topic Modeling results from the following text:

``` “Thai food was great we loved it. Thiland also has beautiful beach resorts, we will come to Thailand again👍” ```

* KeypartX Result 

<img style="border:1px solid black"
src="https://github.com/pengKiina/KeypartX/raw/main/images/keyparts_sent_network.png" width="40%" height="40%" align="center" />

* Topic Modeling Result

```['food','thailand','resort','great','love', 'beautiful']```


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

* 2 Keyparts Wordclouds

The following wordclouds are generated from a real example of corpus comprised of reviews by those who visit Thailand.

<img src="https://github.com/pengKiina/KeypartX/raw/main/images/keypart_wordcloud.png" width="35%" height="35%" align="center" />

* 3 Community and Gray Perceptual Unit Networks 

<img src="https://github.com/pengKiina/KeypartX/raw/main/images/community_gray.gif" width="70%" height="50%" align="center" />



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
