function sendAJAX(url,type) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('GET', url);
    xhr.send();
    // 处理结果
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.readyState==4 && xhr.status==200) {
          resolve(xhr.response);
        } else {
          reject(xhr.status);
        }
      }
    }
  })
}

window.onload = async function() {
  let fourData = await sendAJAX('http://112.74.37.0:5657/overview-data');

  let staNums= document.querySelectorAll('.sta-num');
  let num = 0;

  for(let x in fourData){
    staNums[num++].innerHTML = fourData[x]
  }

}