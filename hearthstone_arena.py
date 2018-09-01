import sys
import pandas as pd

def parse_bucket_list(bucket_list):
    dic = {}
    for i in open(bucket_list, "r").readlines()[1:]:
        v = i.split(",")
        card_name = v[2]
        if card_name not in dic:
            dic[v[2]] = v[0]
        else:
            dic[v[2]] = dic[v[2]] + "_" + v[0]
    return dic

def main(apearance, bucket_list):
    a_df = pd.read_csv(apearance, header=0, index_col=0)
    bucket = parse_bucket_list(bucket_list)
    bucket_kind = sorted(sorted(set(bucket.values())), 
                         key=lambda x: x.split("_")[0])
    heroes = a_df.index.unique().tolist()

    mtx = []
    for hero in heroes:
        ex = a_df.ix[hero, :]
        counts = [0 for i in bucket_kind]
        for j in range(ex.shape[0]):
            card_name = ex.iloc[j, 0]
            try:
                index = bucket_kind.index(bucket[card_name])
            except:
                print card_name
            counts[index] += ex.iloc[j, 5]
        mtx.append(counts)
    df = pd.DataFrame(mtx, index=heroes, columns=bucket_kind).T
    df = df / df.sum(axis=0) * 100
    df.to_csv(apearance + ".bucket.csv")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])