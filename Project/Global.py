import math
def calc_TFIDF(frequencyTokens, totalTokens, numberOfResources, totalResourceAppears):
    weight = ((frequencyTokens/totalTokens)*(.99) + .01) * math.log((numberOfResources/(totalResourceAppears)+1)+1,10)
    return weight