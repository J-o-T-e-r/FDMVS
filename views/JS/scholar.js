

let btn = document.getElementsByClassName('btn');
let graphExist = document.getElementById('graph-exist');
let graphPredict = document.getElementById('graph-predict');


btn[0].parentNode.addEventListener('click',(e)=>{
    /* switch(e.target.innerHTML){
        case "结果":{
            graphExist.style.display = "block";
            btn[1].classList.toggle('btn-unact');
            btn[1].classList.toggle('btn-act');
            graphPredict.style.display = "none";
            btn[0].classList.toggle('btn-act');
            btn[0].classList.toggle('btn-unact');
            
        };break;
        case "预测":{
            graphPredict.style.display = "block";
            graphExist.style.display = "none";
            btn[0].classList.toggle('btn-unact');
            btn[0].classList.toggle('btn-act');
            btn[1].classList.toggle('btn-act');
            btn[1].classList.toggle('btn-unact');
        };break;

    } */
    for(let x of btn) {
        if(x.classList[1] !== 'btn-unact') {
            x.classList.toggle('btn-unact');
            x.classList.toggle('btn-act');
        }
    }
    e.target.classList.toggle('btn-unact');
    e.target.classList.toggle('btn-act');
    if(e.target.innerHTML == "结果"){
        graphExist.style.display = "block";
        graphPredict.style.display = "none";
    }else{
        graphExist.style.display = "none";
        graphPredict.style.display = "block";
    }
})