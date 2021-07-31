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
//第一个统计图
  let useData = await sendAJAX('http://112.74.37.0:5657/hot_domain');
        let getData = [];

        for(let x in useData) {
            let a = {
                type: x,
                value: useData[x]
            }
            getData.unshift(a);
        }
        console.log(getData);

        const chart = new G2.Chart({
            container: 'container',
            width:600,
            height: 400,
        });
        chart.data(getData);
        chart.scale({
        value: {
            max: 1400,
            min: 0,
            alias: '科研兴趣人数',
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
            fontSize: 16,
            fontWeight: 200,
            },
        },
        });
        chart.legend(false);
        chart.coordinate().transpose();
        chart
        .interval()
        .position('type*value')
        .size(25)
        .label('value', {
            style: {
            fill: '#8d8d8d',
            },
            offset: 10,
        });
        chart.interaction('element-active');
        chart.render();

// 第二个统计图
        let useData1 = await sendAJAX('http://112.74.37.0:5657/excellent_school');

        console.log(useData1);

        let getData1 = [];

        for(let x in useData1) {
            let a = {
                item: x,
                count: useData1[x][0],
                percent: useData1[x][1],
            }
            getData1.unshift(a);

        }
        console.log(getData1);

        const chart1 = new G2.Chart({
        container: 'container1',
        width:990,
        height: 500,
        });
        chart1.data(getData1);
        chart1.scale('percent', {
        formatter: (val) => {
            val = val * 100 + '%';
            return val;
        },
        });
        chart1.coordinate('theta', {
        radius: 0.75,
        innerRadius: 0.6,
        });
        chart1.tooltip({
        showTitle: false,
        showMarkers: false,
        itemTpl: '<li class="g2-tooltip-list-item"><span style="background-color:{color};" class="g2-tooltip-marker"></span>{name}: {value}</li>',
        });
        
        chart1
        .interval()
        .adjust('stack')
        .position('percent')
        .color('item')
        .label('percent', (percent) => {
            return {
            content: (data) => {
                return `${data.item}: ${percent * 100}%`;
            },
            };
        })
        .tooltip('item*percent', (item, percent) => {
            percent = percent * 100 + '%';
            return {
            name: item,
            value: percent,
            };
        });
        chart1.interaction('element-active');

        chart1.render();

}