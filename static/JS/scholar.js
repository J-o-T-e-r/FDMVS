

let btn = document.getElementsByClassName('btn');
let graphExist = document.getElementById('graph-exist');
let graphPredict = document.getElementById('graph-predict');

for(let i = 0;i<2;i++){
    btn[i].onclick = function(){
        for(let x of btn) {
            if(x.classList[1] !== 'btn-unact') {
                x.classList.toggle('btn-unact');
                x.classList.toggle('btn-act');
            }
        }
        btn[i].classList.toggle('btn-unact');
        btn[i].classList.toggle('btn-act');
        if(i==0){
            graphExist.style.display = "block";
            graphPredict.style.display = "none";
        }else{
            graphExist.style.display = "none";
            graphPredict.style.display = "block";
        }
    }
}

