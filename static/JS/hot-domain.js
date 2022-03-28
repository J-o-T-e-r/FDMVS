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

window.onload = async function(){
        let useData = await sendAJAX('http://127.0.0.1:5000/hot_domain');
        let getData = [];

        for(let x in useData) {
            let a = {
                type: x,
                value: useData[x]
            }
            getData.unshift(a);
        }
        console.log(getData);



        // const data = [
        //     { type: '计算机', value: 888 },
        //     { type: 'rua', value: 85 },
        //     { type: '住宿旅游', value: 103 },
        //     { type: '交通运输与仓储邮政', value: 142 },
        //     { type: '建筑房地产', value: 251 },
        //     { type: '教育', value: 367 },
        //     { type: 'IT 通讯电子', value: 491 },
        //     { type: '社会公共管理', value: 672 },
        //     { type: '医疗卫生', value: 868 },
        //     { type: '金融保险', value: 1234 },
        // ];
        const chart = new G2.Chart({
            container: 'container',
            width:500,
            height: 300,
        });
        chart.data(getData);
        chart.scale({
        value: {
            max: 1400,
            min: 0,
            alias: '热门领域',
        },
        });
        chart.axis('type', {
        title: null,
        tickLine: null,
        line: null,
        });

        chart.axis('value', {
        label: null,
        title: {
            offset: 30,
            style: {
            fontSize: 12,
            fontWeight: 200,
            },
        },
        });
        chart.legend(false);
        chart.coordinate().transpose();
        chart
        .interval()
        .position('type*value')
        .size(18)
        .label('value', {
            style: {
            fill: '#8d8d8d',
            },
            offset: 10,
        });
        chart.interaction('element-active');
        chart.render();
    }