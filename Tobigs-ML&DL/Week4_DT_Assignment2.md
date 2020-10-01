```python
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('https://raw.githubusercontent.com/AugustLONG/ML01/master/01decisiontree/AllElectronics.csv')
df.drop("RID",axis=1, inplace = True) #RID는 그냥 Index라서 삭제
```


```python
df
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
      <th>2</th>
      <td>middle_aged</td>
      <td>high</td>
      <td>no</td>
      <td>fair</td>
      <td>yes</td>
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
      <th>6</th>
      <td>middle_aged</td>
      <td>low</td>
      <td>yes</td>
      <td>excellent</td>
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



## 함수 만들기


```python
from functools import reduce

def getEntropy(df, feature) :
    D_len = df[feature].count() # 데이터 전체 길이
    # reduce함수를 이용하여 초기값 0에 
    # 각 feature별 count을 엔트로피 식에 대입한 값을 순차적으로 더함
    return reduce(lambda x, y: x+(-(y[1]/D_len) * np.log2(y[1]/D_len)), \
                  df[feature].value_counts().items(), 0)
```


```python
getEntropy(df, "class_buys_computer")
```




    0.9402859586706311




```python
# 정답
getEntropy(df, "class_buys_computer")
```




    0.9402859586706311




```python
def get_target_true_count(col, name, target, true_val, df=df):
    """
    df[col]==name인 조건에서 Target이 참인 경우의 갯수를 반환
    """
    return df.groupby([col,target]).size()[name][true_val]

def NoNan(x):
    """
    Nan의 경우 0을 반환
    """
    return np.nan_to_num(x)

def getGainA(df, feature) :
    info_D = getEntropy(df, feature) # 목표변수 Feature에 대한 Info(Entropy)를 구한다.
    columns = list(df.loc[:, df.columns != feature]) # 목표변수를 제외한 나머지 설명변수들을 리스트 형태로 저장한다.
    gains = []
    D_len = df.shape[0] # 전체 길이
    for col in columns:
        info_A = 0
        # Col내 개별 Class 이름(c_name)과 Class별 갯수(c_len)
        for c_name, c_len in df[col].value_counts().items():
            target_true = get_target_true_count(col, c_name, feature, 'yes') 
            prob_t = target_true / c_len
            # Info_A <- |Dj|/|D| *  Entropy(label) | NoNan을 이용해 prob_t가 0인 경우 nan이 나와 생기는 오류 방지
            info_A += (c_len/D_len) * -(NoNan(prob_t*np.log2(prob_t)) + NoNan((1 - prob_t)*np.log2(1 - prob_t)))
        gains.append(info_D - info_A)
    
    result = dict(zip(columns,gains)) # 각 변수에 대한 Information Gain 을 Dictionary 형태로 저장한다.
    return(result)
```


```python
df.groupby(['age','class_buys_computer']).size()
```




    age          class_buys_computer
    middle_aged  yes                    4
    senior       no                     2
                 yes                    3
    youth        no                     3
                 yes                    2
    dtype: int64




```python
getGainA(df, "class_buys_computer")
```




    {'age': 0.24674981977443933,
     'income': 0.02922256565895487,
     'student': 0.15183550136234159,
     'credit_rating': 0.04812703040826949}



정답
```
{'age': 0.24674981977443933, 
 'income': 0.02922256565895487, 
 'student': 0.15183550136234159, 
 'credit_rating': 0.04812703040826949}
 ```

## 결과 확인하기


```python
my_dict = getGainA(df, "class_buys_computer")
def f1(x):
    return my_dict[x]
key_max = max(my_dict.keys(), key=f1)
print('정보 획득이 가장 높은 변수는',key_max, "이며 정보 획득량은", my_dict[key_max], "이다.")
```

    정보 획득이 가장 높은 변수는 age 이며 정보 획득량은 0.24674981977443933 이다.



```python
# 정답
my_dict = getGainA(df, "class_buys_computer")
def f1(x):
    return my_dict[x]
key_max = max(my_dict.keys(), key=f1)
print('정보 획득이 가장 높은 변수는',key_max, "이며 정보 획득량은", my_dict[key_max], "이다.")
```

    정보 획득이 가장 높은 변수는 age 이며 정보 획득량은 0.24674981977443933 이다.

