# DT Assignment1

# Data Loading


```python
import pandas as pd 
import numpy as np
```


```python
pd_data = pd.read_csv('https://raw.githubusercontent.com/AugustLONG/ML01/master/01decisiontree/AllElectronics.csv')
pd_data.drop("RID",axis=1, inplace = True) #RID는 그냥 순서라서 삭제
```

# 1. Gini 계수를 구하는 함수 만들기

- Input: df(데이터), label(타겟변수명)
- 해당 결과는 아래와 같이 나와야 합니다.


```python
from functools import reduce
```


```python
def get_gini(df, label):
    D_len = df[label].count() # 데이터 전체 길이
    # 각 클래스별 Count를 담은 Generator 생성
    count_arr = (value for key, value in df[label].value_counts().items())
    # reduce를 이용해 초기값 1에서 각 클래스 (count / D_len)^2 빼기
    return reduce(lambda x, y: x - (y/D_len)**2 ,count_arr,1)
```


```python
pd_data['class_buys_computer']
```




    0      no
    1      no
    2     yes
    3     yes
    4     yes
    5      no
    6     yes
    7      no
    8     yes
    9     yes
    10    yes
    11    yes
    12    yes
    13     no
    Name: class_buys_computer, dtype: object




```python
get_gini(pd_data,'class_buys_computer')
```




    0.4591836734693877




```python
# 정답
get_gini(pd_data,'class_buys_computer')
```




    0.4591836734693877



# 2. Feature의 Class를 이진 분류로 만들기
 ## ex) {A,B,C} -> ({A}, {B,C}), ({B}, {A,C}), ({C}, {A,B})
- CART 알고리즘은 이진분류만 가능합니다. 수업때 설명했던데로 변수가 3개라면 3가지 경우의 수에 대해 지니계수를 구해야합니다.
- 만약 변수가 4개라면, 총 7가지 경우의 수가 가능합니다. (A, BCD) (B, ACD) (C, ABD) (D, ABC) (AB, CD) (AC, BD) (AD, BC)

- Input: df(데이터), attribute(Gini index를 구하고자 하는 변수명)
- 해당 결과는 아래와 같이 나와야 합니다.


```python
import itertools 
```


```python
import itertools # 변수의 모든 클래시 조합을 얻기 위해 itertools 불러오기

def get_binary_split(df, attribute):
    attr_unique = df[attribute].unique()
    # 이중 For loop List Comprehension
    result = [
            list(item) 
            for i in range(1, len(attr_unique)) # 1부터 변수의 클래스 갯수-1 까지 Iteration
            for item in itertools.combinations(attr_unique, i) # i를 길이로 하는 조합 생성
        ]
    return result
```


```python
# 검증을 위한 테스트데이터 제작
df = pd.DataFrame([1,2,3,4,2,1,3], columns=['d'])
print(df['d'].unique())
a = get_binary_split(df,'d')
```

    [1 2 3 4]



```python
# get_binary_split 검증, 짝을 찾아 전체 클래스가 나오는지 확인
for i in range(len(a) // 2):
    b = a[i] + a[len(a)-i-1]
    b.sort()
    print(a[i], a[len(a)-i-1], '=>', b)
```

    [1] [2, 3, 4] => [1, 2, 3, 4]
    [2] [1, 3, 4] => [1, 2, 3, 4]
    [3] [1, 2, 4] => [1, 2, 3, 4]
    [4] [1, 2, 3] => [1, 2, 3, 4]
    [1, 2] [3, 4] => [1, 2, 3, 4]
    [1, 3] [2, 4] => [1, 2, 3, 4]
    [1, 4] [2, 3] => [1, 2, 3, 4]



```python
# 정답
get_binary_split(pd_data, "age")
```




    [['youth'],
     ['middle_aged'],
     ['senior'],
     ['youth', 'middle_aged'],
     ['youth', 'senior'],
     ['middle_aged', 'senior']]




```python
# 정답
get_binary_split(pd_data, "age")
```




    [['youth'],
     ['middle_aged'],
     ['senior'],
     ['youth', 'middle_aged'],
     ['youth', 'senior'],
     ['middle_aged', 'senior']]



# 3. 다음은 모든 이진분류의 경우의 Gini index를 구하는 함수 만들기
- 위에서 완성한 두 함수를 사용하여 만들어주세요!
- 해당 결과는 아래와 같이 나와야 합니다.
- 결과로 나온 Dictionary의 Key 값은 해당 class 들로 이루어진 tuple 형태로 들어가 있습니다.


```python
def get_attribute_gini_index(df, attribute, label):
    result = {}
    keys = get_binary_split(df, attribute)
    D_len = df[attribute].shape[0]
    for key in keys:
        t_index = df[attribute].map(lambda x: x in key) # Split한 클래스들에 속하는 df Index 추출
        Dj_len = sum(t_index) # Sum으로 True갯수 계산
        # Gini 식 계산,  ~index를 통해 False_index로 전환
        gini = (Dj_len / D_len) * get_gini(df[t_index], label) + ((D_len - Dj_len) / D_len) * get_gini(df[~t_index], label)
        result[tuple(key)] = gini
    return result
```


```python
get_attribute_gini_index(pd_data, "age", "class_buys_computer")
```




    {('youth',): 0.3936507936507937,
     ('middle_aged',): 0.35714285714285715,
     ('senior',): 0.4571428571428572,
     ('youth', 'middle_aged'): 0.4571428571428572,
     ('youth', 'senior'): 0.35714285714285715,
     ('middle_aged', 'senior'): 0.3936507936507937}




```python
# 정답
get_attribute_gini_index(pd_data, "age", "class_buys_computer")
```




    {('youth',): 0.3936507936507936,
     ('middle_aged',): 0.35714285714285715,
     ('senior',): 0.45714285714285713,
     ('youth', 'middle_aged'): 0.45714285714285713,
     ('youth', 'senior'): 0.35714285714285715,
     ('middle_aged', 'senior'): 0.3936507936507936}



여기서 가장 작은 Gini index값을 가지는 class를 기준으로 split해야겠죠?

결과를 확인해보도록 하겠습니다.


```python
my_dict = get_attribute_gini_index(pd_data, "age", "class_buys_computer")
key_min = min(my_dict.keys(), key=(lambda k: my_dict[k]))
print('Min -',key_min, ":", my_dict[key_min])
```

    Min - ('middle_aged',) : 0.35714285714285715



```python
# 정답
my_dict = get_attribute_gini_index(pd_data, "age", "class_buys_computer")
key_min = min(my_dict.keys(), key=(lambda k: my_dict[k]))
print('Min -',key_min, ":", my_dict[key_min])
```

    Min - ('middle_aged',) : 0.35714285714285715


# 다음의 문제를 위에서 작성한 함수를 통해 구한 값으로 보여주세요!
## 문제1) 변수 ‘income’의 이진분류 결과를 보여주세요.

## 문제2) 분류를 하는 데 가장 중요한 변수를 선정하고, 해당 변수의 Gini index를 제시해주세요.

## 문제3) 문제 2에서 제시한 feature로 DataFrame을 split한 후 나눠진 2개의 DataFrame에서 각각   다음으로 중요한 변수를 선정하고 해당 변수의 Gini index를 제시해주세요.


```python
##문제1 답안
get_binary_split(pd_data, 'income')
```




    [['high'],
     ['medium'],
     ['low'],
     ['high', 'medium'],
     ['high', 'low'],
     ['medium', 'low']]




```python
pd_data.columns[:-1]
```




    Index(['age', 'income', 'student', 'credit_rating'], dtype='object')




```python
##문제2 답안
target = "class_buys_computer"

def get_important_feature(df, target):
    cols = df.columns[df.columns != target]
    results = []
    for col_name in cols:
        my_dict = get_attribute_gini_index(df, col_name, target)
        if my_dict:
            min_key = min(my_dict.keys(), key=(lambda k: my_dict[k]))
            print(f"{col_name}) Gini Index: {my_dict[min_key]} {min_key}")
            results.append((my_dict[min_key], col_name, min_key))
    results.sort()
    return results[0]

print('최적의 값:', get_important_feature(pd_data, "class_buys_computer"))
```

    age) Gini Index: 0.35714285714285715 ('middle_aged',)
    income) Gini Index: 0.4428571428571429 ('high',)
    student) Gini Index: 0.3673469387755103 ('no',)
    credit_rating) Gini Index: 0.42857142857142855 ('fair',)
    최적의 값: (0.35714285714285715, 'age', ('middle_aged',))


Age의 Gini Index가 0.35로 가장 적기때문에 가장 중요한 변수이며 그중에서도 'middle_aged'가 Split의 기준이 될 것이다.


```python
##문제3 답안
```


```python
# Split 함수 생성
def split_by_vals(attr, vals, df=pd_data):
    t_index = pd_data[attr].map(lambda x: x in vals)
    # Index 에 따라 DF 분리
    return df[t_index], df[~t_index]
```


```python
# 기준에 따라 데이터프레임 2개 생성
df_split_t, df_split_f = split_by_vals('age',('middle_aged',))
```


```python
df_split_t
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>income</th>
      <th>student</th>
      <th>credit_rating</th>
      <th>class_buys_computer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>middle_aged</td>
      <td>high</td>
      <td>no</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>6</th>
      <td>middle_aged</td>
      <td>low</td>
      <td>yes</td>
      <td>excellent</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>11</th>
      <td>middle_aged</td>
      <td>medium</td>
      <td>no</td>
      <td>excellent</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>12</th>
      <td>middle_aged</td>
      <td>high</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_important_feature(df_split_t, 'class_buys_computer')
```

    income) Gini Index: 0.0 ('high',)
    student) Gini Index: 0.0 ('no',)
    credit_rating) Gini Index: 0.0 ('fair',)





    (0.0, 'credit_rating', ('fair',))



위에서 만든 함수를 이용해 구한 결과 모두 0이 나와 최적의 상태라 볼 수 있음


```python
# 'age',('middle_aged',)) False 그룹
df_split_f 
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>income</th>
      <th>student</th>
      <th>credit_rating</th>
      <th>class_buys_computer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>youth</td>
      <td>high</td>
      <td>no</td>
      <td>fair</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1</th>
      <td>youth</td>
      <td>high</td>
      <td>no</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
    <tr>
      <th>3</th>
      <td>senior</td>
      <td>medium</td>
      <td>no</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>4</th>
      <td>senior</td>
      <td>low</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>5</th>
      <td>senior</td>
      <td>low</td>
      <td>yes</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
    <tr>
      <th>7</th>
      <td>youth</td>
      <td>medium</td>
      <td>no</td>
      <td>fair</td>
      <td>no</td>
    </tr>
    <tr>
      <th>8</th>
      <td>youth</td>
      <td>low</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>9</th>
      <td>senior</td>
      <td>medium</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>10</th>
      <td>youth</td>
      <td>medium</td>
      <td>yes</td>
      <td>excellent</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>13</th>
      <td>senior</td>
      <td>medium</td>
      <td>no</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
  </tbody>
</table>
</div>




```python
gini, s_attr, s_vals = get_important_feature(df_split_f, 'class_buys_computer')
```

    age) Gini Index: 0.48 ('youth',)
    income) Gini Index: 0.375 ('high',)
    student) Gini Index: 0.31999999999999984 ('no',)
    credit_rating) Gini Index: 0.4166666666666667 ('fair',)



```python
print(gini, s_attr, s_vals)
```

    0.31999999999999984 student ('no',)


Student 가 no인지 아닌지에 대한 지니계수가 0.319로 최소임으로 이에 따른 분류가 최적이라는 것을 알 수 있다.


```python
# df_split_f 가지에서 한 번 더 분류 시도
df_split2_t, df_split2_f = split_by_vals(s_attr, s_vals, df=df_split_f)
```

    /Users/josang-yeon/tobigs/lib/python3.7/site-packages/ipykernel_launcher.py:5: UserWarning: Boolean Series key will be reindexed to match DataFrame index.
      """



```python
df_split2_t
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>income</th>
      <th>student</th>
      <th>credit_rating</th>
      <th>class_buys_computer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>youth</td>
      <td>high</td>
      <td>no</td>
      <td>fair</td>
      <td>no</td>
    </tr>
    <tr>
      <th>1</th>
      <td>youth</td>
      <td>high</td>
      <td>no</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
    <tr>
      <th>3</th>
      <td>senior</td>
      <td>medium</td>
      <td>no</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>7</th>
      <td>youth</td>
      <td>medium</td>
      <td>no</td>
      <td>fair</td>
      <td>no</td>
    </tr>
    <tr>
      <th>13</th>
      <td>senior</td>
      <td>medium</td>
      <td>no</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_important_feature(df_split2_t, 'class_buys_computer')
```

    age) Gini Index: 0.2 ('youth',)
    income) Gini Index: 0.26666666666666666 ('high',)
    credit_rating) Gini Index: 0.26666666666666666 ('fair',)





    (0.2, 'age', ('youth',))



2번째 좌측(True) 가지에선 Age - youth 조합이 지니계수 0.2로 최적의 변수임을 알 수 있다.


```python
df_split2_f
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>income</th>
      <th>student</th>
      <th>credit_rating</th>
      <th>class_buys_computer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>senior</td>
      <td>low</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>5</th>
      <td>senior</td>
      <td>low</td>
      <td>yes</td>
      <td>excellent</td>
      <td>no</td>
    </tr>
    <tr>
      <th>8</th>
      <td>youth</td>
      <td>low</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>9</th>
      <td>senior</td>
      <td>medium</td>
      <td>yes</td>
      <td>fair</td>
      <td>yes</td>
    </tr>
    <tr>
      <th>10</th>
      <td>youth</td>
      <td>medium</td>
      <td>yes</td>
      <td>excellent</td>
      <td>yes</td>
    </tr>
  </tbody>
</table>
</div>




```python
get_important_feature(df_split2_f, 'class_buys_computer')
```

    age) Gini Index: 0.26666666666666666 ('senior',)
    income) Gini Index: 0.26666666666666666 ('low',)
    credit_rating) Gini Index: 0.2 ('fair',)





    (0.2, 'credit_rating', ('fair',))



2번째 우측(False) 가지에선 'credit_rating', ('fair',) 조합이 지니계수 0.2로 최적의 변수임을 알 수 있다.


```python

```
