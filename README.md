# A Keyword-Extraction-Algorithm Based Searching Method for Subscription Articles
### Cheng Zheng, Jinhua Sun, Yuliang Zhang, Yejia Liu  
### 2023/1/11
--------------------------------
## Background
--------------------------------
"**Wen Xu Jin Shan**" is a subsciption serving residents of Jinshan community in Fuzhou. It can help people learn about epidemic prevention policies, nucleic acid sites and other important information by pushing articles:  
![政策宣传]()  
Providing benefits such as free fruit and medicine:  
![福利放送]()  
At the same time, it also has a "**Ni Hu Wo Ying**" platform to understand people's situation and solve people's difficulties:
![你呼我应]()   
which provides people with convenience.  

However, after our team actually used the official account, we found that there are two functions worth improving inside the official account. First, the information articles in the "convenience service" mini program lack search function, and can only be sorted by time, as shown in the figure:  
![痛点1]()  
It is not easy for people to look up important articles in the past. At the same time, the problem may become more prominent in the future as the number of articles increases.

Secondly, the function of "follow automatic reply" provided by the chat interface of the official account is not perfect. At present, users can only get corresponding tweets by inputting the two keywords of community and nucleic acid:  
![痛点2.1]()  
while other keywords can only get fixed replies as shown in the figure.  
![痛点2.2]()  
It was found that many of the keywords people entered in the chat box did not get the desired tweets:  
![痛点2.3]()  
which also shows that the user support for this feature is actually very high.

Based on this, our team determined our project objectives. On the one hand, it is to realize the search function of information articles in the "convenience service", on the other hand, it is to realize the expansion of the keyword database of "Pay attention to automatic reply", both of which require us to achieve **automatic keyword extraction**, which is the core of our whole project.

## Algorithm Introduction and Synonym Thesaurus
----------------------
Keyword extraction algorithm is divided into **supervised algorithm** and **unsupervised algorithm**. At present, **unsupervised algorithm** is widely used, which consumes less resources and does not require manual annotation of data sets. It is also the algorithm used in our project.

The first keyword extraction algorithm is **TF-IDF**. Through **word frequency** and **inverse document frequency**, we can infer which words may be the key words of the article. Below is our test results of this article:  
![算法1]()  
However, the corpus used in the inverse document frequency of **TF-IDF** is not fully applicable to this project, and **Arabic numerals** may appear, so we do not use this algorithm.

We actually use the **TextRank** algorithm. The core concept of **TextRank** algorithm is "**voting**" or "**recommending**", mainly including the following steps.

The first step is to add the determined keyword as a vertex to the graph according to the lexical unit, and then connect the vertex according to the **relationship** between the two words. The importance of the vertex determines the importance of the edge connected with the vertex, and then perform iterative calculation. Finally, rank the vertices according to the vertex score to obtain the ranking of keywords. Below is the keyword obtained by TextRank in the same article:  
![算法2]()  
###### <u>In this project, 26 tweets asking for Jinshan were used, and the time range was September to December</u>

However, there is a problem with the above two algorithms that they cannot query **synonyms**. Therefore, we have introduced **cnsyn** to build synonym thesaurus using **Wikipedia** and **Chinese synonym dictionary**. When the user enters the query word, search the synonym of the word in the inverted index according to the word, and return the synonym of the input word.

## Algorithm Implementation and Results
----------------
This **flowchart** below roughly shows the implementation process of the algorithm.  
![结果1]()  
First, we need to **preprocess** the article, use **TextRank** algorithm to extract the key words of the article and record them.
We have implemented two searching methods in the project, namely, search for **article keywords** and search for **full-text content**.

In the keyword searching method, the keyword entered by the user can be used as the **substring** of the article keyword (for example, the user enters "*核酸*", and the program search contains "*做核酸*") or the **synonym** (for example, the relationship between "*抗疫*" and "*防控疫情*"), and from the perspective of relevance, the former will have higher priority in ranking than the latter.

In the content search method, the algorithm will traverse all articles and return links to articles containing the words entered by users.

Next showed four search examples. The first is **keyword searching**. After entering *防疫* and *阳* keywords. You can see that 2 and 3 articles containing relevant keywords in the database are returned here.  
![防疫 阳]()  
However, it is noted that the search for keywords here takes 14 seconds, which is a long time and is not feasible in practice. This problem will be analyzed later in the paper.

The second is **full text content searching**. Input the full text of *做核酸* and *水果* to search the whole article, and also return the web links of multiple articles.  
![做核酸 水果]()  
Finally, we have solved the pain points mentioned at the beginning and realized the **keyword extraction** and **searching** function of the article. For example, this table represents the hot words entered by the user in the chat box of the official account. The algorithm can be introduced to **automatically respond to any keyword**.

## Analysis and Prospect
-------------
Next, I will explain the analysis of the algorithm and the future directions of improvement.

First of all, compare the keywords extracted by manual and algorithm. The figure below shows the keywords extracted by our four members for a subscription article and ranked in descending order by the number of overlaps:  
![分析1]()  
while this figure below shows the keywords retrieved by the algorithm and ranked by the relevance:  
![分析2]()  
We filtered the keywords given by the algorithm with the manually selected keywords as the criteria. Then, we can find a total of 6 keywords that are in line with each other, which  is indicated by the red bar chart on the right. In fact, the algorithm gave a total of 20 keywords, because the latter ones did not overlap and had low relevance, they were not placed in the chart. After a rough calculation, we can conclude that this algorithm has an accuracy of 30%.

At the same time, we found that the highest keyword accuracy obtained by the TextRank algorithm was 31.2% by searching the relevant literature, which is close to the result of 30% obtained by our algorithm. Moreover, since most of the valid keywords are concentrated in the first 10, we can increase the precision by delimiting the **keyword relevance range**, for example, by limiting the relevance to greater than 0.4. Therefore, I think the precision of the algorithm meets the requirement of use.

In terms of the efficiency of the algorithm, we found that the time for each keyword search was more than 10 seconds. This is because our search for keywords includes **synonym searching**, and the algorithm needs to cross-reference the synonyms of the search terms with the synonyms of the extracted keywords, each comparison requiring re-searching for synonyms. Furthermore, the search for synonyms requires access to multiple web resources, so the overall efficiency is much lower.

For this, our proposed solution is to build a local thesaurus and put in advance the synonyms of all article keywords, as well as the synonyms.

