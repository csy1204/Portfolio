# 👨‍💻 PlayDev's Portfolio

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fcsy1204%2FPortfolio&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Hits&edge_flat=false)](https://hits.seeyoufarm.com)

## 1. 💡 ML & DL

### 1.1. Tobigs 우수과제

> 13기 우수과제로 선정된 코드들입니다. 전체 우수과제는 [여기서](https://github.com/tobigs-datamarket/tobigs-13th) 확인 가능합니다.

|주제|설명|링크|
|--|--|--|
| **아파트 경매가격 데이터 분석 EDA** | 아파트 경매겨가격 데이터 기반 데이터 분석, 시각화 및 Feature 생성 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week1_EDA/w1_eda_cho_sangyeon.md) |
| **Decision Tree** | Decision Tree 알고리즘 구현 (Gini, Entrophy) |[링크1](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week4_DT_Assignment1.md), [링크2](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML&DL/Week4_DT_Assignment2.md) |
| **Deep Learning Framework** | Kannada MNIST를 위한 하이퍼파라미터 서칭 및 VGG, SOPCNN 구현  | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week7_Deep%20Learning/w7_DL_Framework.md) |
| **NLP** | 뉴스 빅데이터 기반 형태소 추출기(khaiii, twitter, kkma) 비교 및<br>임베딩 모델(Skipgram, CBOW, FastText) 비교 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week8_NLP/w8_nlp_cho.md)|

### 1.2. Tobgis 

> Tobigs 활동을 하며 만든 자료들입니다. 주로 추천시스템 세미나 자료입니다.

| Title | Link |
|--|--|
| **추천시스템 세미나 발표: DL기반 추천시스템, 멀티암드밴딧, 랭킹**  | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Recommender_Systyem_dl_multi-armed-bandits-ranking.pdf) |
| Training Deep Autoencoders for CF 논문 리뷰 |[링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/CF_Autoencoder_paper_review.pdf)||
| Recsys 2019 2등 논문 리뷰 | [링크](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/recsys_2019_2nd_paper_review.pdf) |
| 크롤링 강의 자료 및 코드 | [강의자료](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/week5_crawling_csy.pdf), [코드](https://github.com/csy1204/Portfolio/blob/master/Tobigs-ML%26DL/Week5_Crawler_Mentor/Week5_Crawler_Mentor.md)|


### 1.3. Project: TripBigs

> 2020.07<br>
> React, Redux, Redux-saga, Flask, LightGBM<br>
> 투빅스 컨퍼런스 프로젝트로 세션 기반의 호텔 추천시스템을 개발하였습니다.

[[프로젝트 링크]](https://github.com/csy1204/TripBigs_Web)

사용자의 이벤트 로그 기반으로 세션 기반 추천을 제공합니다. 실시간 ML 모델 서빙을 통한 실시간 추론을 제공하며, 오토인코더, 협업필터링 기반 호텔별 맛집 추천 리스트를 보여줍니다.

**주요 특징**
1. Session 기반 추천 모델은 [Boosting algorithms for session-based, context-aware recommender system in online travel domain.](https://drive.google.com/file/d/1SOoO0vBYXEpE6-1MY0MYNBvCQnQRjp5_/view) (Recsys 2019) 을 기반으로 구현되었으며 서울 데이터를 기반으로 파인튜닝 및 최적화를 진행하였습니다.
2. 호텔 기반 맛집 추천 모델은 오토인코더, 협업필터링, DeepFM, Wide&Deep 모델이 사용되었으며, 로컬 맛집과 외국인을 위한 맛집을 구분한 것이 특징입니다. 로컬 맛집의 경우 이전 히스토리를 선택할 수 있는 옵션을 제공합니다.
3. Session 기반 추천순 정렬을 이용할 시 Redux-Saga를 이용한 비동기 통신 제어를 하였으며, 전반적으로 Redux를 통한 상태관리르 구현하였습니다. 백엔드 서버는 Flask로 구현되었으며 실시간 인퍼런스를 제공합니다.

<br><br><br>

## 2. 🚀 Web Full Stack

### 2.1. Dynamic Subtitle Generator & Web Editor

> 2020.01, 개발인원 1명<br>
> React, Flask, NCloud Clova AI API, OpenCV<br>
> NAVER AI Bunring Day 본선 참가작으로 WebVTT 기반 동적 자막 생성 및 웹에디터를 개발하였습니다.

[[프로젝트 레포지토리]](https://github.com/csy1204/Dynamic-Subtitle-Auto-generator) | [[시연 영상]](https://www.youtube.com/watch?v=zkR_4aC83iA&ab_channel=PlayDev) | [[발표자료]](https://github.com/csy1204/Dynamic-Subtitle-Auto-generator/blob/master/OCCR_%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C.pdf)

|데모 스크린샷|
|--|
|![](https://user-images.githubusercontent.com/18041103/94856297-baaee280-046a-11eb-86d0-1c31abe09021.png)|

**주요 특징**
1. WebVTT 기반 동적 자막 생성 및 실시간 웹 에디터 기능 제공
2. 프레임 별 OCR 텍스트 및 위치 인식 정보 기반으로 하여 WebVTT 자막 파일 생성 
2. HTML5 플레이어 호환 가능하며 위치, 내용 수정 및 번역 기능 제공 (Firefox기준)


### 2.2. 경매 가능한 중고거래 웹사이트 구현 (웹프로그래밍실습)

> 2019.11 ~ 2019.12, 개발인원 3명<br>
> django, google api, html, css, js

[[프로젝트 레포지토리]](https://github.com/csy1204/ecommerce_project) | [[레포트]](https://github.com/csy1204/Portfolio/blob/master/CS%20Reports/Web%20Programming%20Lab_Final_Report.pdf)

**주요 특징**
1. 관리자, 판매자, 구매자가 있으며 판매자는 경매나 바로 구매하기로 물건을 올릴 수 있으며 경매 종료 기한을 설정할 수 있다.
2. 구매자는 경매에 참여하거나 바로 구매를 할 수 있으며 경매가 종료되어 입찰을 받을 경우 확인이 가능하다.
3. Google Map API를 이용해 거래 위치와 경로를 확인할 수 있다.


<br><br><br>

## 3. ✍🏻 CS

### Computer Network (Python)

|주제|설명|링크|
|--|--|--|
| **MultiThreading File Transfer** | 멀티쓰레딩을 통한 대용량 파일 복사 및 로그 작성 프로그램 |[코드](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment1%20MultiThreading%20File%20Transfer/main.py) [레포트](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment1%20MultiThreading%20File%20Transfer/2013313217_report.pdf) |
| **HTTP Web Server** | TCP 소켓 프로그래밍을 통한 HTTP 서버 구현 (쿠키, Keep Alive 구현) | [코드](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment2%20HTTP%20Web%20Server/2013313217.py) [레포트](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment2%20HTTP%20Web%20Server/HW2_Report.pdf) |
| **Pipelined Reliable Data Transfer over UDP** | UDP기반 데이터 전송 프로그램 | [코드](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment3%20Pipelined%20Reliable%20Data%20Transfer%20over%20UDP/receiver.py) [레포트](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment3%20Pipelined%20Reliable%20Data%20Transfer%20over%20UDP/2013313217_ChoSangYeon.pdf) |
| **Chatting (NAT traversal)** | NAT traversal를 해결한 P2P 채팅 프로그램 | [코드](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment4%20NAT%20traversal/server.py) [레포트](https://github.com/csy1204/Portfolio/blob/master/ComputerNetworks/Assignment4%20NAT%20traversal/2013313217_ChoSangYeon.pdf)|







