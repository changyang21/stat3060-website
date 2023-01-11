# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from jieba.analyse import *
import cnsyn
import datetime as dt
import csv
import time


class WechatArticle:
    def __init__(article, filename, publishTime, title, comp_keys, hand_keys, webLink):
        article.filename = filename
        article.publishTime = publishTime
        article.title = title
        article.comp_keys = comp_keys
        article.hand_keys = hand_keys
        article.webLink = webLink

    def displayArticleLink(article):
        print('【发布时间】{} 【文章标题】{}'.format(article.publishTime, article.title))
        print(article.webLink)

def displayResultArticles(relArticles):
    if len(relArticles) == 0:
        print('No related articles. T_T')
    else:
        relArticles.sort(key=lambda WechatArticle: WechatArticle.publishTime, reverse=True)
        for each in relArticles:
            each.displayArticleLink()

def printExtractKeyword(filePath):
    # source: https://www.jianshu.com/p/cf383fd471bb
    with open(filePath) as f:
        data = f.read()
    print("TF-idf method")
    for keyword, weight in extract_tags(data, withWeight=True):
        print('%s %s' % (keyword, weight))
    print("TextRank method")
    for keyword, weight in textrank(data, withWeight=True):
        print('%s %s' % (keyword, weight))

def cnSynonyms(sourceWord):
    # source: https://gitee.com/vencen/Chinese-Synonyms
    # 1.基于词的传统召回
    print(cnsyn.search(sourceWord))
    print(cnsyn.search(sourceWord, origin='wiki'))
    print(cnsyn.search(sourceWord, origin='cndict'))
    # 2。基于向量的语义召回Approximate Nearest Neighbor Search
    # print(cnsyn.anns(sourceWord))

def initAllArticles(allArticles, maxFileNum):
    for i in range(1, maxFileNum + 1):
        filename = str(i) + '.txt'
        with open ("article/" + filename) as f:
            title = f.readline().strip('\n')
            webLink = f.readline().strip('\n')
            temp = f.readline().strip('\n')
            temp = temp.split(' ')
            publishTime = dt.datetime(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]))

            tempArticle = WechatArticle(filename, publishTime, title, [], [], webLink)
            allArticles.append(tempArticle)

def computeKeys_textrank(allArticles, maxFileNum):
    for i in range(0, maxFileNum):
        filePath = 'article/' + allArticles[i].filename
        with open(filePath) as f:
            data = f.read()
        for keyword, weight in textrank(data, withWeight=True):
            allArticles[i].comp_keys.append(keyword)

def wordApproximate(word1, word2):
    allcnSynonyms1 = []
    allcnSynonyms1 += cnsyn.search(word1)
    allcnSynonyms1 += cnsyn.search(word1, origin='wiki')
    allcnSynonyms1 += cnsyn.search(word1, origin='cndict')
    # allcnSynonyms1 += cnsyn.anns(word1)
    for each in allcnSynonyms1:
        if word2 == each:
            return True
    allcnSynonyms2 = []
    allcnSynonyms2 += cnsyn.search(word2)
    allcnSynonyms2 += cnsyn.search(word2, origin='wiki')
    allcnSynonyms2 += cnsyn.search(word2, origin='cndict')
    # allcnSynonyms2 += cnsyn.anns(word2)
    for each in allcnSynonyms2:
        if word1 == each:
            return True
    return False

def findSubIndex(allArticles, keyword, maxFileNum):
    sub_index = [-1] * maxFileNum
    for i in range(maxFileNum):
        for j in range(len(allArticles[i].comp_keys)):
            if keyword in allArticles[i].comp_keys[j]:
                sub_index[i] = j
    return sub_index

def findSynIndex(allArticles, keyword, maxFileNum):
    syn_index = [-1] * maxFileNum
    for i in range(maxFileNum):
        for eachKeyword in allArticles[i].comp_keys:
            if wordApproximate(eachKeyword, keyword):
                syn_index[i] = allArticles[i].comp_keys.index(eachKeyword)
                break
    return syn_index

def printToCsv(allArticles):
    for eachArticle in allArticles:
        line = eachArticle.comp_keys
        with open('comp_keys.csv', 'a+') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(line)

def main():

    allArticles = []
    maxFileNum = 26
    initAllArticles(allArticles, maxFileNum)
    computeKeys_textrank(allArticles, maxFileNum)

    # printToCsv(allArticles)

    # 人工 keyword
    # //////

    while True:
        print('请输入搜索关键词和搜索类型（关键词/内容） >>> ')
        keyword = input()
        searchType = input()
        if searchType == '关键词':
            # 孙锦华
            # 输出 <= 5 篇文章（包含关键词的）
            # 输出逻辑：输出n篇第一个关键词为目标关键词的文章，输出n篇第二个关键词为目标关键词的文章，...以此类推
            # 优先 ==，如果5列以后
            start000 = time.time()
            relArticles = []
            sub_index = findSubIndex(allArticles, keyword, maxFileNum)
            syn_index = findSynIndex(allArticles, keyword, maxFileNum)

            for each in sub_index:
                if each < 5:
                    relArticles.append(allArticles[sub_index.index(each)])
                    temp = dict.fromkeys(relArticles)
                    relArticles = list(temp.keys())
                    if len(relArticles) >= 5:
                        break
            for each in syn_index:
                if each < 5:
                    relArticles.append(allArticles[syn_index.index(each)])
                    temp = dict.fromkeys(relArticles)
                    relArticles = list(temp.keys())
                    if len(relArticles) >= 5:
                        break

            displayResultArticles(relArticles)
            end000 = time.time()
            print('【共耗时】%.2f秒' % (end000 - start000))


        elif searchType == '内容':
            start000 = time.time()
            relArticles = []
            for i in range(maxFileNum):
                filename = str(i + 1) + '.txt'
                with open('article/' + filename) as f:
                    for line in f:
                        oneline = line.strip('\n')
                        if keyword in oneline:
                            relArticles.append(allArticles[i - 1])
                            break
                if len(relArticles) >= 5:
                    break
            displayResultArticles(relArticles)
            end000 = time.time()
            print('【共耗时】%.2f秒' % (end000 - start000))


        elif keyword == 'exit':
            break
        else:
            print('wrong instruction')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # sourceWord = '绿码'
    # print("test for {}".format(sourceWord))
    # cnSynonyms(sourceWord)
    # printExtractKeyword('article/1.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
