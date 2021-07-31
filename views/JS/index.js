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
        grid: {
          line: {
            style: {
              lineWidth: 0,
              lineDash: [2, 2]
            }
          }
        }
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

        let getData1 = [];

        for(let x in useData1) {
            let a = {
                item: x,
                count: useData1[x][0],
                percent: useData1[x][1],
            }
            getData1.unshift(a);

        }

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


        let useData2 = await sendAJAX('http://112.74.37.0:5657/excellent_scholar');
        let getData2 = [];

        for(let node in useData2) {
            let a = {
                name: node,
                x: useData2[node][0],
                y: useData2[node][1],
                z: useData2[node][2]*100
            }
            getData2.unshift(a);
        }

      const chart2 = new G2.Chart({
        container: 'container2',
        width:1200,
        height: 500,
        padding: [20, 20, 50, 80],
      });
      chart2.data(getData2);
      chart2.scale({
        x: {
          alias: 'rankpage值 (*10e-4)', // 定义别名
          tickInterval: 1, // 自定义刻度间距
          max: 30, // 自定义最大值
          min: 6 // 自定义最小是
        },
        y: {
          alias: '连接的边数',
          tickInterval: 50,
          max: 1200,
          min: 300
        },
        z: {
          alias: '所占比例 %'
        }
      });
      // 开始配置坐标轴
      chart2.axis('x', {
        title: {
          offset: 40
        },
        label: {
          formatter: val => {
            return val + ''; // 格式化坐标轴显示文本
          }
        },
        // grid: {
        //   line: {
        //     style: {
        //       stroke: '#d9d9d9',
        //       lineWidth: 1,
        //       lineDash: [2, 2]
        //     }
        //   }
        // }
      });
      chart2.axis('y', {
        title: {
          offset: 40
        },
        label: {
          formatter: val => {
            if (+val > 0) {
              return val + '';
            } else {
              return val;
            }
          }
        },
        grid: {
          line: {
            style: {
              lineWidth: 0,
              lineDash: [2, 2]
            }
          }
        }
      });
      chart2.legend(false);
      chart2.tooltip({
        title: 'name',
        showMarkers: false
      });
      chart2
        .point()
        .position('x*y')
        .color('#1890ff')
        .size('z', [15, 50])
        .label('name', {
          offset: 0, // 文本距离图形的距离
          style: {
            fill: '#1890FF',
            stroke: '#fff',
            lineWidth: 1,
          }
        })
        .shape('circle')
        .tooltip('x*y*z')
        .style({
          lineWidth: 0,
          stroke: '#1890ff',
          fillOpacity: 0.3,
        });

      chart2.annotation().region({
        start: ['0%', '0%'],
        end: ['100%', '100%'],
        style: {
          lineWidth: 0,
          fillOpacity: 0,
          strokeOpacity: 1,
          stroke: '#545454',
        }
      });

      chart2.interaction('element-active');

      chart2.render();


      
}