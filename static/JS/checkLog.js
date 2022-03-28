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
let usernameSes = sessionStorage.getItem('username');
let userDetail = document.getElementsByClassName('user-data');
let username = document.getElementById('usernameText');
let urlRoot = 'http://127.0.0.1:5000/';
let interest = [];
let token = sessionStorage.getItem('token');
for(let i = 0;i<interestItem.length;i++){
  interestItem[i].onclick = ()=>{
    if(interestItem[i].classList.toggle('tagsactive')) interest.push(interestItem[i].innerHTML);
    else interest.splice($.inArray(interestItem[i].innerHTML,interest),1);
      console.log(interest)
  }
}
inputBox[0].value = userDetail[1].innerHTML;
    inputBox[1].value = userDetail[2].innerHTML;
userBtn[0].onclick = ()=>{
  coverBox.style.display = "block";
  modifyBox.style.display = "block";
    inputBox[0].value = userImfText[1].innerHTML;
    inputBox[1].value = userImfText[2].innerHTML;
  for(let n of interestItem){
    n.classList.remove('tagsactive');
  }
  reloadBtn.click();
}
reloadBtn.onclick = ()=>{
    $.get('http://127.0.0.1:5000/api-interest-given',(res)=>{
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
        
        $.post('http://127.0.0.1:5000/api-ChangeInfo',data,(res)=>{
            if(res == 'success'){
                alert('修改成功！');
                userImfText[0].innerHTML = interest.join(',')||'暂无';
                userImfText[1].innerHTML = inputBox[0].value;
                userImfText[2].innerHTML = inputBox[1].value;
                userImfText[2].innerHTML = inputBox[1].value;
                interest=[];
                shutMod.click();
            }else{
                alert('修改失败，请重试！')
            }
        })
    }else{
        alert('请输入合法字符！');
    }
    }
    
   





const checkLog = ()=>{
  let url = urlRoot + '/api-login-verify';
  let token = sessionStorage.getItem('token');
    if(!token){
      console.log(111)
        location.href = '/login_register';
    }
  let data = {
    token:token,
    username:usernameSes
  }
  $.post(url,data,(res)=>{

    if(!$.isEmptyObject(res)){
        let dataRes = JSON.parse(res);
        console.log(dataRes)
        logedBox.style.display = "block";
        unlogedBox.style.display = "none";
        username.innerHTML = dataRes.username;
        if(dataRes.age!=null && dataRes.workplace!=null){
            if(eval(dataRes.interest)!=null) {
                userDetail[0].innerHTML = eval(dataRes.interest).join(',');
                interest = eval(dataRes.interest);
                console.log(interest)
            }

            userDetail[1].innerHTML = dataRes.age;
            userDetail[2].innerHTML = dataRes.workplace;
        }
    }else{
        unlogedBox.style.display = "block";
        logedBox.style.display = "none";

    }

  })
}
checkLog();


