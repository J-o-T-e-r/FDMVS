let userImf = document.getElementById('user-imf');
let userBtn = document.getElementsByClassName('user-btn');
let logedBox = document.getElementById('menu-loged');
let unlogedBox = document.getElementById('menu-unloged');
let userImfText = document.getElementsByClassName('user-data');
let modifyBox = document.getElementById('imf-modify');
let shutMod = document.getElementById('modify-shut');
let reloadBtn = document.getElementById('reload');
let modifyBtn = document.getElementById('modify');
let coverBox = document.getElementById('cover');
let inputBox = document.getElementsByClassName('text')
let interestItem = document.getElementsByClassName('interest-item');

let userDetail = document.getElementsByClassName('user-data');
let username = document.getElementById('usernameText');
let urlRoot = 'http://112.74.37.0:5657/';
let interest = [];
let token = sessionStorage.getItem('token');
for(let i = 0;i<interestItem.length;i++){
  interestItem[i].onclick = ()=>{
    interest.push(interestItem[i].innerHTML);
    interestItem[i].style.backgroundColor = "#f9f0ff";
  }
}
inputBox[0].value = userDetail[1].innerHTML;
    inputBox[1].value = userDetail[2].innerHTML;
userBtn[0].onclick = ()=>{
  coverBox.style.display = "block";
  modifyBox.style.display = "block";
  for(let n of interestItem){
    n.style.backgroundColor = "white"
  }
  reloadBtn.click();
}
reloadBtn.onclick = ()=>{
    $.get('http://112.74.37.0:5657/api-interest-given',(res)=>{
        let data = eval(res);
        for(let n =0;n<data.length;n++){
          interestItem[n].innerHTML = data[n];
        }
    })
}
shutMod.onclick = ()=>{
    modifyBox.style.display = "none";
    coverBox.style.display = "none";
}

modifyBtn.onclick = ()=>{
    let legal1 = /^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9]){2,16}$/g;
    let legal2 = /^((1[0-5])|[1-9])?\d$/g;
    interest = Array.from(new Set(interest));
    if(legal2.test(inputBox[0].value) && legal1.test(inputBox[1].value)){
        let data;
        if(interest.length == 0){
            data = {
                username:username.innerHTML,
                age:inputBox[0].value,
                workplace:inputBox[1].value,
            }
        }else{
            data = {
                username:username.innerHTML,
                interest:JSON.stringify(interest),
                age:inputBox[0].value,
                workplace:inputBox[1].value,
            }
        }
        
        $.post('http://112.74.37.0:5657/api-ChangeInfo',data,(res)=>{
            if(res == 'success'){
                alert('修改成功！');
                userImfText[0].innerHTML = interest.join(',')||'暂无';
                userImfText[1].innerHTML = inputBox[0].value;
                userImfText[2].innerHTML = inputBox[1].value;
                shutMod.click();
            }else{
                alert('修改失败，请重试！')
            }
        })
    }else{
        alert('请输入合法字符！');
    }
    }
    
   





/* search.addEventListener('keydown',(e)=>{
    e.preventDefault();
    if (e.keyCode === 13) {
        searchBtn.click();
    }
   
}) */




