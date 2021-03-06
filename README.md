# stockProject

<h1> 프로젝트 소개</h1>
인원: 1인 개발<br>
개발 기간: 24일<br>
배포: 아직 안함(AWS나 pythonanywhere 예정)<br>
개요: 웹 풀스택으로 구현한 주식 커뮤니티 사이트<br>
주요 기능(앱별 작성)<br>
타 사이트와 차별화되는 점 :<br>
- 회원가입시 자신의 투자 성향 선택, 글 작성시에도 자신의 투자 성향 선택하게함 -> 특정 주식에 대해 어떤 투자 성향의 의견이 많은지 알 수 있음<br>
- 주식 종목 세부페이지에서 3가지 지표(거래량, 코스피 지수, 종가)에 대해 분석 가능. 0~1 사이의 값으로 스케일링 하기 때문에 유저가 선택한 지표들 사이의 관계를 한눈에 볼 수 있음
<table>
<tr><th>앱</th><th>기능</th></tr>
<tr><td>Main</td><td>홈 화면(5분에 한번씩 검색/좋아요 기준으로 5위안의 주식들 리턴), krx의 csv 기준으로 주식 검색</td></tr>
<tr><td>User</td><td>회원가입, 로그인/로그아웃, 마이페이지 정보 수정, 좋아요 한 주식들의 코스피와 비교한 등락률 리턴</td></tr>
<tr><td>Post</td><td>글 CRUD</td></tr>
<tr><td>Comment</td><td>댓글, 대댓글 CRUD</td></tr>
<tr><td>Stock</td><td>검색한 주식 종목의 기본적인 정보 리턴<br>주식 종목 세부 페이지에서 유저가 선택한 시작 날짜 및 지표들(거래량, 코스피 지수, 종가)을 sklearn의 maxabsscaler로 전처리하여 시각화 결과 리턴 </td></tr>
</table>

<h1> 사용한 기술</h1>
프론트: html, css, js<br>
백: django<br>
개발 환경: visual studio code<br>
db: mysql<br>

<h1> 사용한 오픈소스 및 데이터</h1>
open api: yfinance<br>
lib: pandas, numpy, matplotlib, mpld3, apscheduler등<br>
데이터: krx의 주식 기본 정보(.csv)<br>

<h1>프로젝트 설명</h1>
회원)<br>

-회원가입<br>
models.py: 장고 abstractUser 상속 후 이메일 필드 오버라이드, 투자 전략 필드 추가<br>
views.py: 회원가입 폼을 통한 에러 관리<br>
![signUp](https://user-images.githubusercontent.com/103106183/167763406-212ac57c-2b2c-434d-8700-ddb3b7b76887.png)<br>
-로그인<br>
views.py: <br>
1. 로그인 시 해당 유저가 좋아요한 주식들에 대해 각 주식을 많이 좋아요한 유저수에 따른 주식 종류(안전/위험/중립)분류<br>
2. 현재 날짜로부터 야후 파이낸스에서 주가 데이터를 가지고 올 수 있는(공휴일 등이 아닌) 가장 빠른 날짜 2개를 계산해 각 주식 종목과 코스피 지수의 등락값 비교(성능 개선 필요)<br>
![signIn](https://user-images.githubusercontent.com/103106183/167763431-9fa09790-679d-4752-9c9b-2bd8aab32435.png)<br>
-로그아웃<br>
-회원정보<br>
![userInfo](https://user-images.githubusercontent.com/103106183/167763248-c1ca8926-4c50-4a61-849a-5f10ed46b1a2.png)<br>
-회원정보 수정<br>
![mdfUserInfo](https://user-images.githubusercontent.com/103106183/167763496-5c70fced-f53c-40f9-8b05-c08eb49a7208.png)<hr>
db)<br>
-mysql 주식 정보<br>
![stockInfoMysql](https://user-images.githubusercontent.com/103106183/167763332-1ddf43d4-23ff-4d65-b523-f2c773a86cc6.png)<hr>
홈)<br>
-로그인 후 홈 화면<br>
views.py: apscheduler 통해 백그라운드에서 5분에 한번씩 좋아요 상위 5개 종목, 조회 상위 5개 종목 갱신<br>
![index](https://user-images.githubusercontent.com/103106183/167763635-06bd1bce-8db7-4703-a054-60c9008e6a46.png)<br>
-검색<br>
![search](https://user-images.githubusercontent.com/103106183/167763456-5b849925-7e0f-4289-9c70-52740f27efab.png)<hr>
주식)<br>
-주식 기본 정보<br>
views.py: 게시글 중 좋아요 5개 이상일 시 인기글에 포함, 페이지네이션, 분석탭의 경우 상장일 이후부터 시작 날짜 선택 가능하게 함<br>
![stockInfo](https://user-images.githubusercontent.com/103106183/167763362-6151232a-c9f3-4d95-b24e-8d580a137a3c.png)<br>
-주식 기본 정보에서 분석탭 사용한 결과<br>
views.py: 판다스의 데이터프레임 활용해 데이터 정제 후 sklearn의 maxabsscaler로 데이터 전처리. 이후 matplotlib으로 데이터 시각화 <br>
![indexResult](https://user-images.githubusercontent.com/103106183/167763609-3253a572-6be0-4a96-8631-3205e0cb606a.png)<hr>
게시글)<br>
-게시글 화면<br>
views.py: 게시글 수정/삭제, 댓글 수정/삭제, 대댓글 수정/삭제 구현<br>
![detailPost](https://user-images.githubusercontent.com/103106183/167763776-0217a2e4-32bc-4fa0-9f56-2d4b0c2eb82c.png)<br>



