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
let search = document.getElementById('search');
let searchBtn = document.getElementById('search-btn');
let userDetail = document.getElementsByClassName('user-data');
let username = document.getElementById('usernameText');
let urlRoot = 'http://112.74.37.0:5657/';
let interest = [];
for(let i = 0;i<interestItem.length;i++){
  interestItem[i].onclick = ()=>{
      interest.push(interestItem[i].innerHTML);
      interestItem[i].style.backgroundColor = "#f9f0ff";
  }
}
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
    inputBox[0].innerHTML = userDetail[1].innerHTML;
    inputBox[1].innerHTML = userDetail[2].innerHTML;
    interest = Array.from(new Set(interest));

    let data = {

    }
    $.post('http://112.74.37.0:5657/api-ChangeInfo',data,(res)=>{

    })
}

const checkLog = ()=>{
  let url = urlRoot + '/api-login-verify';

  let data = {
    token:'MTYyNzgyNzE4NS45NzE4NDg1OjU2YWY4MmI5MDBmZGNjZTZkNTU5MTc5NTE1NWUzYjNmYTk3MWMyZGY=',
    username:'asd'
  }
  $.post(url,data,(res)=>{
    if(!$.isEmptyObject(res)){
        let dataRes = JSON.parse(res);
        logedBox.style.display = "block";
        unlogedBox.style.display = "none";
        username.innerHTML = dataRes.username;
        if(eval(dataRes.interest)!=null && dataRes.age!=null && dataRes.workplace!=null){
            userDetail[0].innerHTML = eval(dataRes.interest).join(',');
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







searchBtn.onclick = ()=>{

    $.post(urlRoot+'api-login-verify',(res)=>{      
        if(!$.isEmptyObject(res)){
            window.open(urlRoot+search.value+'/page');
        }   
        else{
            alert('请先登录再进行此操作！');
            location.href = '../html/log-reg.html'
        }
    })
   

}

userBtn[1].onclick = ()=>{
    sessionStorage.removeItem('token');
}