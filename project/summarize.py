import json

def read_data():


    name = open('name.txt', 'r')
    print("Users taken for analysis are:")
    print(name.read())
    common = open('common.txt', 'r')
    print("\nCommon users followed by main users taken for analysis are:")
    print(common.read())
    a = json.load(open("c_f.txt"))
    cf = 0
    fr = 0
    for i, j in a.items():
        cf += 1
        fr += len(j)
    print('\nNumber of friends collected for analysis: %d' %(cf+fr) )
    tweets = json.load(open("tweets.txt"))
    tw = 0
    for t in tweets:
        tw += len(t['text'])
    print('\nNumber of messages collected: %d' % tw)
    clusters = open('clusters.txt', 'r')
    cl = clusters.readlines()
    nm = 1
    for i in cl:
        nm += 1
    print('\nNumber of communities discovered: %d' % nm)
    avg = (cf+fr)//nm
    print('\nAverage number of users per community: %f' %avg)
    (positives,negatives,mixed) = json.load(open("sentiments.txt"))
    print('\nNumber of instances per class found: %d positive instances , %d negative instances and %d mixed instances'
    %(len(positives), len(negatives), len(mixed)))
    print('\nOne example from each class:')
    for tweet, pos, neg in sorted(positives, key=lambda x: x[1], reverse=False):
        positive=(pos,neg,tweet)
    print('Example of positive class:')
    print(positive)
    for tweet, pos, neg in sorted(negatives, key=lambda x: x[2], reverse=False):
        negative=(neg,pos,tweet)
    print('Example of negative class:')
    print(negative)

    for tweet, pos, neg in sorted(mixed, key=lambda x: x[2], reverse=True):
        mixed=(pos,neg,tweet)
    print('Example of mixed class:')
    print(mixed)

    file = open("summary.txt", "w")
    file.write(('\nNumber of friends collected for analysis: %d' %(cf+fr)))
    file.write(('\nNumber of messages collected: %d' % tw))
    file.write(('\nNumber of communities discovered: %d' % nm))
    file.write(('\nAverage number of users per community: %f' %avg))
    file.write(('\nNumber of instances per class found: %d positive instances , %d negative instances and %d mixed instances'
    %(len(positives), len(negatives), len(mixed))))
    #file.write(('Example of positive class:' %positive))
    #file.write(('Example of negaive class:' %negative))
    #file.write(('Example of mixed class:' %mixed))


def main():
    read_data()



if __name__ == '__main__':
    main()
