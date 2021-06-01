
################### GÖREV - 1 #####################
import pandas as pd
df = pd.read_csv("datasets/persona.csv")
df.head()

# Veri seti ile ilgili genel bilgiler
def check_df(dataFrame, head=5):
    print("##################### Shape #####################")
    print(dataFrame.shape)
    print("##################### Types #####################")
    print(dataFrame.dtypes)
    print("##################### Head #####################")
    print(dataFrame.head(head))
    print("##################### Tail #####################")
    print(dataFrame.tail(head))
    print("##################### NA #####################")
    print(dataFrame.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataFrame.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Soru1: Source unique sayısı
df["SOURCE"].nunique()

# Soru2: Source unique frekansı
df["SOURCE"].value_counts()

# Soru3: Price unique sayısı
df["PRICE"].nunique()

# Soru4: Her bir price satış adedi
df["PRICE"].value_counts()

# Soru5: Hangi ülkeden kaç satış var?
df["COUNTRY"].value_counts()

# Soru6: Ülkelere göre satışlardan gelen kazanç
df.groupby(["COUNTRY"]).agg({"PRICE":"sum"})

# Soru7: Source türüne göre satış sayısı
df.groupby(["SOURCE"]).agg({"SEX":"count"})

# Soru8: Ülkelere göre PRICE ortalaması
df.groupby(["COUNTRY"]).agg({"PRICE":"mean"})

# Soru 9: SOURCE' a göre PRICE ortalaması
df.groupby(["SOURCE"]).agg({"PRICE":"mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalaması
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE":"mean"})

################### GÖREV - 2 #####################

# COUNTRY, SOURCE, SEX, AGE kırılımında toplam kazanç
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"sum"})


################### GÖREV - 3 #####################

# Price değişkenini azalan sort values ile sıralama
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"sum"})
agg_df.sort_values("PRICE",ascending=False)
################### GÖREV - 4 #####################

# index isimlerini değişken ismine dönüştürme
agg_df = agg_df.reset_index()

################### GÖREV - 5 #####################

# Age değişkenini kategorik değişkene çevirme
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 40, 90], labels=["0_18","18_23","23_40","40_90"])
agg_df.head(20)

################### GÖREV - 6 #####################

# Customers level based sutun isimleri
col = [col for col in agg_df.columns if col not in ["AGE","PRICE"]]
agg_df[col]
len(agg_df[col])
# Yeni değişken oluşturma
agg_df["customers_level_based"] = ["_".join(i).upper() for i in agg_df[col].values]

# Yeni df oluşturma
col2 = [col for col in agg_df if col in ["customers_level_based","PRICE"]]
new_df = agg_df[col2]

# Gruplama
new_df.groupby(["customers_level_based"]).agg({"PRICE":"mean"})

################### GÖREV - 7 #####################
new_df["SEGMENT"] = pd.qcut(new_df["PRICE"], 4, labels=["D","C","B","A"])
new_df.groupby(["SEGMENT"]).agg({"PRICE":["mean","max","sum"]})
new_df[new_df["SEGMENT"] == "C"].describe()

# 33 yaşındaki Turk android kullanıcısının ortalama sağladığı kazanç
new_user = "TUR_ANDROID_FEMALE_23_40"
new_df[new_df["customers_level_based"] == new_user].agg({"PRICE":"mean"})

# 35 yaşındaki Fransız ios kullanıcısının ortalama sağladığı kazanç
new_user2 = "FRA_IOS_FEMALE_23_40"
new_df[new_df["customers_level_based"] == new_user2].agg({"PRICE":"mean"})