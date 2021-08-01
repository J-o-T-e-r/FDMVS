function isLegal(type,obj,icon,tip,flag){       //检测输入内容是否合法
    if(type == 0){		
        var legal = /^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9]){2,10}$/g;    
    }else if(type == 1){
        var legal = /^\w{6,14}$/g;	//密码匹配
    }
    var arr = new Array();
    arr = obj.value.split(" ");		//将输入的内容存进数组
    if(legal.test(obj.value) && arr.length == 1){
        flag = 1;
        if(obj.value){
	        icon[0].style.visibility = 'visible';   //控制
	        icon[1].style.visibility = 'hidden';
	        tip.style.visibility = 'hidden';
    	}
    }else{
    	if(obj.value){
	        icon[0].style.visibility = 'hidden';
	        icon[1].style.visibility = 'visible';
	        tip.style.visibility = 'visible';
    	}
    }
    return flag;
}

window.onload = function(){
    let loginFlag = new Array();
	let signFlag = new Array();
	loginFlag[0] = [0,0,0];     //作为匹配成功与否的标识
	signFlag[0] = [0,0];
    let logBox = document.getElementById('log-box');
    //模式选择
	let enLogin = document.getElementById('login-btn');
	let enSignup = document.getElementById('signup-btn');
	//表单
	let form1 = document.getElementById('login');
	let form2 = document.getElementById('sign-up');
    //输入框
	let user = document.getElementsByClassName('user-name');
	let pw = document.getElementsByClassName('password');
	let tips = document.getElementsByClassName('tips');
	//按钮
	let btn = document.getElementsByClassName('btn');
    //icon
	let icon1 = document.getElementsByClassName('icon1');
	let icon2 = document.getElementsByClassName('icon2');
	let icon3 = document.getElementsByClassName('icon3');
	let icon4 = document.getElementsByClassName('icon4');
    let icon5 = document.getElementsByClassName('icon5');
    //提示框
    let prompt = document.getElementById('prompt');
    let prmBtn = document.getElementById('prm-btn');
    let prmP = document.getElementsByClassName('prm-p');
    let cover = document.getElementById('cover');
    let flagRep = 1;
    let token;
    let localStorage = window.localStorage;
    //回车登录
	user[0].addEventListener("keyup",function(){
		if(event.keyCode === 13){
			btn[0].click();
		}
	})
	user[1].addEventListener("keyup",function(){
		if(event.keyCode === 13){
			btn[0].click();
		}
	})
	pw[0].addEventListener("keyup",function(){
		if(event.keyCode === 13){
			btn[0].click();
		}
	})
	pw[1].addEventListener("keyup",function(){
		if(event.keyCode === 13){
			btn[0].click();
		}
	})
	pw[2].addEventListener("keyup",function(){
		if(event.keyCode === 13){
			btn[0].click();
		}
	})
    //表单切换
	enLogin.onclick = function(){
		enLogin.style.borderBottom = "1px solid #81afe0";
        logBox.classList.remove('reg-style');
        logBox.classList.add('log-style');
		if(form2.style.visibility !="hidden"){
			icon1[0].style.visibility = "hidden";
			icon1[1].style.visibility = "hidden";
			icon2[0].style.visibility = "hidden";
			icon2[1].style.visibility = "hidden";
			icon3[0].style.visibility = "hidden";
			icon3[1].style.visibility = "hidden";
			icon4[0].style.visibility = "hidden";
			icon4[1].style.visibility = "hidden";
            icon5[0].style.visibility = "hidden";
			icon5[1].style.visibility = "hidden";
			tips[2].style.visibility = "hidden";
			tips[3].style.visibility = "hidden";
		}
		enSignup.style.borderBottom = "0";		
		form1.style.visibility = "visible";
		form1.style.opacity = "1";
		form2.style.visibility ="hidden";
		form2.style.opacity = "0";
        btn[0].style.transform = "translateY(0px)";
        btn[0].style.display = 'block';
 
		btn[1].style.transform = "translateY(0px)";	
	}
	enSignup.onclick = function(){
        logBox.classList.remove('log-style');
        logBox.classList.add('reg-style');
        enLogin.style.borderBottom = "0";
		enSignup.style.borderBottom = "1px solid #81afe0";
		form1.style.visibility = "hidden";
		form1.style.opacity = "0";
		form2.style.visibility ="visible";
		form2.style.opacity = "1";
		if(form1.style.visibility =="hidden"){
			icon1[0].style.visibility = "hidden";
			icon1[1].style.visibility = "hidden";
			icon2[0].style.visibility = "hidden";
			icon2[1].style.visibility = "hidden";
			icon3[0].style.visibility = "hidden";
			icon3[1].style.visibility = "hidden";
			icon4[0].style.visibility = "hidden";
			icon4[1].style.visibility = "hidden";
            icon5[0].style.visibility = "hidden";
			icon5[1].style.visibility = "hidden";
			tips[0].style.visibility = "hidden";
			tips[1].style.visibility = "hidden";
            		
            btn[1].style.display = 'block';
     
            btn[0].style.transform = "translateY(60px)";
            btn[1].style.transform = "translateY(60px)";
	    }
    }
    user[0].onfocus = function(){
		tips[0].style.visibility = "visible";
		this.onblur = function(){
			loginFlag[0] = isLegal(0,this,icon1,tips[0],loginFlag[0]);
		}
	}

	pw[0].onfocus = function(){
		tips[1].style.visibility = "visible";
		this.onblur = function(){
			loginFlag[1] = isLegal(1,this,icon2,tips[1],loginFlag[1]);
		}
	}
	user[1].onfocus = function(){
		tips[2].style.visibility = "visible";
        
		this.onblur = function(){
            let data = {
                username:user[1].value
            }
            $.post('http://112.74.37.0:5657/api-register-verify',data,(res)=>{
                if(res=='success'){
                    tips[2].innerHTML = "请输入长度为2到14的中文或英文";
                    flagRep = 1;
                    tips[2].style.color = "black";
                    signFlag[0] = isLegal(0,this,icon3,tips[2],signFlag[0]);
                    
                }else{
                    flagRep = 0;
                    tips[2].innerHTML = "用户名已存在！";
                    tips[2].style.color = "red";
                    tips[2].style.visibility = "visible";
                }
            })
			
		}
	}
	pw[2].onfocus = function(){
		this.onblur = function(){
            if(pw[1].value != pw[2].value){
                tips[4].innerHTML = "两次密码输入不一致，请重新输入！"
                tips[4].style.color = "red";
                tips[4].style.visibility = "visible";  
                icon5[1].style.visibility = 'visible';   //控制
	            icon5[0].style.visibility = 'hidden'; 
                signFlag[1] = 0;
            }else{
                icon5[0].style.visibility = 'visible';   //控制
	            icon5[1].style.visibility = 'hidden';
                tips[4].style.visibility = "hidden"; 
                signFlag[1] = 1;
            }
		}
	}
    pw[1].onfocus = function(){
		tips[3].style.visibility = "visible";
		this.onblur = function(){
			loginFlag[1] = isLegal(1,this,icon4,tips[3],loginFlag[2]);
            
		}
	}


    
    btn[0].onclick = function(){
        cover.style.display = "block";
        if(loginFlag[0] && loginFlag[1] &&user[0].value && pw[0].value){
            let url = "http://112.74.37.0:5657/api-login";
            let data = {
                username : user[0].value,
        		pwd : pw[0].value,
            }
            
            $.post(url,data,function(res){
            if(res.length!=0){
                sessionStorage.setItem('token',res);
                token = res;;
                prmP[2].innerHTML = '登陆成功！';   
                      
            }else{
                prmP[2].innerHTML = '用户名或密码错误，请重试！';
            }
            prompt.style.display = "block"; 
            prmBtn.addEventListener("click",function(){
                prompt.style.display = "none";
                prmP[2].innerHTML = '';
            })
            });
            prompt.style.display = "block";
            prmBtn.addEventListener("click",function(){
                prompt.style.display = "none";
                cover.style.display = "none";
                if(prmP[2].innerHTML = '登陆成功！')location.href = 'http://112.74.37.0:5657/';   
            })
        }else if(!user[0].value && !pw[0].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "用户名和密码都没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            })			
        }else if(!user[0].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "用户名还没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            prmP[2].innerHTML = '';
            })		
        }else if(!pw[0].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "密码还没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            prmP[2].innerHTML = '';
            })
        }else{
            prompt.style.display = "block";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            })
        }
    }
    
    btn[1].onclick = function(){
        cover.style.display = "block";
        if(!user[1].value && !pw[1].value && !pw[2].value){
            prompt.style.display = "block";
            
            prmP[2].innerHTML = "用户名和密码都没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            
            prmP[2].innerHTML = '';
            })		
        }else if(!user[1].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "用户名还没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            prmP[2].innerHTML = '';
            })		
        }else if(!pw[1].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "密码还没填哦！";
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            prmP[2].innerHTML = '';
            })
        }else if(!pw[2].value){
            prompt.style.display = "block";
            prmP[2].innerHTML = "还没有重新输入密码哦！";
            
            prmBtn.addEventListener("click",function(){
            prompt.style.display = "none";
            cover.style.display = "none";
            prmP[2].innerHTML = '';
            })
        }
        else if(signFlag[1]==0){
            prmP[2].innerHTML = '输入密码不一致，请重试！';
            prompt.style.display = "block";
            prmBtn.addEventListener("click",function(){
                prompt.style.display = "none";
                cover.style.display = "none";
            })
        }else if(flagRep == 0){
            prmP[2].innerHTML = '用户名已存在，请重试！';
            prompt.style.display = "block";
            prmBtn.addEventListener("click",function(){
                prompt.style.display = "none";
                cover.style.display = "none";
            })
        }
        else if(signFlag[0] && signFlag[1]){
            let url = "http://112.74.37.0:5657/api-register-data";
            let data = {
                username : user[1].value,
        		pwd : pw[1].value,
             }
             $.post(url,data,function(res){
                 
                    if(res=="success"){
                        prmP[2].innerHTML = '注册成功！';                 
                        enLogin.click();
                    }else{
                        prmP[2].innerHTML = '注册失败，请稍后重试！';
                    }
                    prmBtn.addEventListener("click",function(){                  
                    prompt.style.display = "none";
                })
             }); 
                prompt.style.display = "block";		
                prmBtn.addEventListener("click",function(){
                prompt.style.display = "none";
                cover.style.display = "none";
            })
        }
    }
    
    }
    
    
