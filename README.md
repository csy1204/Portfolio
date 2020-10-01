# 조상연의 Portfolio


## 1. ML & DL

### 1.1. Tobigs 우수과제

|주제|설명|링크|
|--|--|--|
| **아파트 경매가격 데이터 분석 EDA** | 아파트 경매겨가격 데이터 기반 데이터 분석, 시각화 및 Feature 생성 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week1_EDA/w1_eda_cho_sangyeon.md) |
| **Decision Tree** | Decision Tree 알고리즘 구현 (Gini, Entrophy) |[링크1](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week4_DT_Assignment1.md), [링크2](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML&DL/Week4_DT_Assignment2.md) |
| **Deep Learning Framework** | Kannada MNIST를 위한 하이퍼파라미터 서칭 및 VGG, SOPCNN 구현  | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week7_Deep%20Learning/w7_DL_Framework.md) |
| **NLP** | 뉴스 빅데이터 기반 형태소 추출기(khaiii, twitter, kkma) 비교 및<br>임베딩 모델(Skipgram, CBOW, FastText) 비교 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week8_NLP/w8_nlp_cho.md)|

### 1.2. Tobgis 

| Title | Link |
|--|--|
| **추천시스템 세미나 발표: DL기반 추천시스템, 멀티암드밴딧, 랭킹**  | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Recommender_Systyem_dl_multi-armed-bandits-ranking.pdf) |
| Training Deep Autoencoders for CF 논문 리뷰 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/CF_Autoencoder_paper_review.pdf)||
| Recsys 2019 2등 논문 리뷰 | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/recsys_2019_2nd_paper_review.pdf) |
| 크롤링 강의 자료 및 코드 | [강의자료](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/week5_crawling_csy.pdf), [코드](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week5_Crawler_Mentor/Week5_Crawler_Mentor.md)|


### 1.3. Project: TripBigs

[[프로젝트 링크]](https://github.com/csy1204/TripBigs_Web)

사용자의 이벤트 로그 기반으로 세션 기반 추천을 제공합니다. 실시간 ML 모델 서빙을 통한 실시간 추론을 제공하며, 오토인코더, 협업필터링 기반 호텔별 맛집 추천 리스트를 보여줍니다.

**주요 특징**
1. Session 기반 추천 모델은 [Boosting algorithms for session-based, context-aware recommender system in online travel domain.](https://drive.google.com/file/d/1SOoO0vBYXEpE6-1MY0MYNBvCQnQRjp5_/view) (Recsys 2019) 을 기반으로 구현되었으며 서울 데이터를 기반으로 파인튜닝 및 최적화를 진행하였습니다.
2. 호텔 기반 맛집 추천 모델은 오토인코더, 협업필터링, DeepFM, Wide&Deep 모델이 사용되었으며, 로컬 맛집과 외국인을 위한 맛집을 구분한 것이 특징입니다. 로컬 맛집의 경우 이전 히스토리를 선택할 수 있는 옵션을 제공합니다.
3. Session 기반 추천순 정렬을 이용할 시 Redux-Saga를 이용한 비동기 통신 제어를 하였으며, 전반적으로 Redux를 통한 상태관리르 구현하였습니다. 백엔드 서버는 Flask로 구현되었으며 실시간 인퍼런스를 제공합니다.


|Main|Info Tab|Recommendation|
|--|--|--|
|![](https://github.com/csy1204/TripBigs_Web/raw/master/tripbigs1.png)|![](https://github.com/csy1204/TripBigs_Web/raw/master/tripbigs2.png)|![](https://github.com/csy1204/TripBigs_Web/raw/master/tripbigs3.png)|
















