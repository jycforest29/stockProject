// const pop_rel_keyword = document.querySelector('.pop_rel_keyword')
// const rel_keyword = document.querySelector('.rel_keyword')
// const search_input = document.querySelector('.search_input')

// // 일정 시간 간격으로 search_input dom 객체의 내용 체크하는 함수
// const checkInput = () => {
//     const beforeInput = search_input.value;
//     // 0.5초 차이
//     timer(beforeInput);
// }

// const timer = (beforeInput) => {
//     setTimeout(() => {
//     if(search_input.value == beforeInput){
//         console.log('입력멈춤');
//         checkInput();
//     } else{
//         console.log('입력창 변함');
//         loadData(search_input.value);
//         checkInput();
//     }

//     if(search_input.value == ''){
//         rel_keyword.classList.remove('rel_search');
//     }else{
//         rel_keyword.classList.add('rel_search');
//     }
//     }, 500)
// }

// const loadData = (input) => {
//     // 전체 db에 있는 주식명 중 input을 포함하는 값 있으면 화면에 나타내기
//     // 없으면 아무것도 띄우지 말기
// }

// const fillSearch = (suggestArr) => {
//     ul.innerHTML = "";
//     suggestArr.forEach((element, index) => {
//     const li = document.createElement("li");
//     li.innerHTML = element.value;
//     ul.appendChild(li);
//     });
// }
