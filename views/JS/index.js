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
  let graphData = {nodes:[],edges:[]};
  let scholarUrl = 'http://112.74.37.0:5657/';
  let detail = document.getElementsByClassName('detail-data');
  let token = sessionStorage.getItem('token');
  let userBtn = document.getElementsByClassName('user-btn');
  let search = document.getElementById('search');
  let usernameSes = sessionStorage.getItem('username');
let searchBtn = document.getElementById('search-btn');
searchBtn.onclick = ()=>{

  $.post(urlRoot+'api-login-verify',(res)=>{  
        
      if($.isEmptyObject(res)){
          window.open('html/scholar.html?'+search.value);
      }   
      else{
          alert('请先登录再进行此操作！');
          location.href = 'html/log-reg.html'
      }
  })
 

}
userBtn[1].onclick = ()=>{
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('username');
  location.href = 'html/log-reg.html';
}
  

  const checkLog = ()=>{
    let url = scholarUrl + '/api-login-verify';
    let data = {
      token:token,
      username:usernameSes
    }
    $.post(url,data,(res)=>{
    
      if(!$.isEmptyObject(res)){
          let dataRes = JSON.parse(res);
          logedBox.style.display = "block";
          unlogedBox.style.display = "none";
          username.innerHTML = dataRes.username;
          console.log(dataRes);
          if(dataRes.age!=null && dataRes.workplace!=null){
              
              if(dataRes.interest !== null)userDetail[0].innerHTML = eval(dataRes.interest).join(',');
              userDetail[1].innerHTML = dataRes.age;
              userDetail[2].innerHTML = dataRes.workplace;
              inputBox[0].value = userDetail[1].innerHTML;
              inputBox[1].value = userDetail[2].innerHTML;
          }
      }else{
          unlogedBox.style.display = "block";
          logedBox.style.display = "none";
        
      }   
      
    })
  }
  checkLog();
  for(let x in fourData){
    staNums[num++].innerHTML = fourData[x]
  }
  function randomNum(minNum,maxNum){ 
    switch(arguments.length){ 
        case 1:  return parseInt(Math.random()*minNum+1,10); 
        case 2:  return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);  
        default: return 0; 
    } 
  } 

  const getNode = function(){
    let url = 'http://112.74.37.0:5657/api-shown_nodes-data';
    $.get(url,(res)=>{
      let nodeTemp = [];
      let data = eval(res);
     
      getNodeDetail(data[0].id)
      for(let k = 0;k<3;k++){
        
        nodeTemp.push(data[k].id);
        
        let connection = (eval('('+data[k].connection+')'))[data[k].id];
        for(let n of connection){
          nodeTemp.push(n);
        }
      }
      nodeTemp = Array.from(new Set(nodeTemp));
     



      for(let j = 0;j<3;j++){
        let i = randomNum(0,nodeTemp.length);
        
        if(nodeTemp.includes(data[i].id)){
          nodeTemp.splice(nodeTemp.indexOf(data[i].id),1);
          let node  = {
            id:data[i].id+'',
            label:data[i].id+'',
            class:'class1'
          }
         
          graphData.nodes.push(node);
        }
        let connection = (eval('('+data[i].connection+')'))[data[i].id];
        for(let n of connection){
          if(nodeTemp.includes(n)){
    
            nodeTemp.splice(nodeTemp.indexOf(n),1);
   
            let node  = {
              id:n+'',
              label:n+'',
              class:data[i].class,
            }
            graphData.nodes.push(node);
          }       
        }
        for(let k = 0;k<connection.length;k++){

          if(connection[k]==6414 || connection[k]==6645){
            continue;
          }
          let edge = {
            source:JSON.stringify(data[i].id),
            target:connection[k]+''
          }
          graphData.edges.push(edge);
        }
      }
     
      createGraph();
    })
  }
  const getNodeDetail = function(id){
    let url = 'http://112.74.37.0:5657/api-id-data';
    
    let data = {
      id:id
    }
    $.post(url,data,(res)=>{
      let data = JSON.parse(res);
      detail[0].innerHTML = id;
      detail[1].innerHTML = eval(data.interest).join(',');
      detail[2].innerHTML = data.neighbour;
      detail[3].onclick = function(){
        $.post(urlRoot+'api-login-verify',(res)=>{            
          if($.isEmptyObject(res)){
            window.open('html/scholar.html?'+id);
          }   
          else{
              alert('请先登录再进行此操作！');
              location.href = 'html/log-reg.html'
          }
        })
        
      }
    })
  }
  getNode();
  function refreshDragedNodePosition(e) {
    const modelDrag = e.item.get('model');
    modelDrag.fx = e.x;
    modelDrag.fy = e.y;
  }
  
  
    const createGraph = function(){
      const graph = new G6.Graph({
        container:'scholar-graph',
        layout:{
          type:'force',
          nodeStrength: -100,
          collideStrength: 0.7,
          alphaDecay: 0.01,
          preventOverlap: true,
          linkDistance:d=>{
            return 600;
          }
        },
        width:1250,
        height:450,
        fitView: true,
        fitViewPadding: [20, 40, 50, 20],
        modes: {
          default: ['drag-canvas', 'zoom-canvas', 'drag-node'], // 允许拖拽画布、放缩画布、拖拽节点
        
        },
        defaultNode:{
          type:'circle',
          style:{
            cursor:'pointer',  
          }
        },
        nodeStateStyles: {
          // 鼠标 hover 上节点，即 hover 状态为 true 时的样式
          hover: {
            fill: 'lightsteelblue',
          },
          // 鼠标点击节点，即 click 状态为 true 时的样式
          click: {
            stroke: '#FF745A',
            lineWidth: 1.5,
          },
          
        },
        defaultEdge:{
          style:{
            stroke:"#b78dff",
            lineWidth:1.5
          },
        },
        edgeStateStyles: {
          // 鼠标点击边，即 click 状态为 true 时的样式
          
          hover: {
            stroke: '#ffab57',
          },
        },
 
      });
  
      graph.data(graphData);
        const nodes =graphData.nodes;
        nodes.forEach((node)=>{
          if(!node.style){
            node.style = {};
          }
        
          switch(node.class){
            case 'class1':{
              node.size = 40;     
              break;
            }
            case 'class2':{
              node.size = 30;
              break;
            }

          }
        })
        graph.render(); 
        // 鼠标进入节点
      graph.on('node:mouseenter', (e) => {
        const nodeItem = e.item; // 获取鼠标进入的节点元素对象
        graph.setItemState(nodeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
      });
  
      // 鼠标离开节点
      graph.on('node:mouseleave', (e) => {
        const nodeItem = e.item; // 获取鼠标离开的节点元素对象
        graph.setItemState(nodeItem, 'hover', false); // 设置当前节点的 hover 状态为 false
      });
      graph.on('edge:mouseenter', (e) => {
        const edgeItem = e.item; // 获取鼠标进入的节点元素对象
        graph.setItemState(edgeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
      });
  
      // 鼠标离开边
      graph.on('edge:mouseleave', (e) => {
        const edgeItem = e.item; // 获取鼠标离开的边元素对象
        graph.setItemState(edgeItem, 'hover', false); // 设置当前边的 hover 状态为 false
      });
   
      // 点击节点
      graph.on('node:click', (e) => {
        // 先将所有当前是 click 状态的节点置为非 click 状态
  
        const nodeItem = e.item; // 获取被点击的节点元素对象
        const linkNodes = Object.assign(nodeItem.getNeighbors('target'),nodeItem.getNeighbors('source'));
        const linkEdges = nodeItem.getEdges();
        getNodeDetail(nodeItem._cfg.id);
        graph.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
          graph.setItemState(cn, 'click', false);
          cn._cfg.group.attrs.opacity = 0.3;
        });
        graph.cfg.edges.forEach((ce) => {
          graph.setItemState(ce, 'click', false);
          ce._cfg.group.attrs.opacity = 0.3;
        });
        graph.setItemState(nodeItem, 'click', true); // 设置当前节点的 click 状态为 true
        nodeItem._cfg.group.attrs.opacity = 1;
        linkNodes.forEach((cn) => { 
          graph.setItemState(cn, 'click', true);
          cn._cfg.group.attrs.opacity = 1;
        });
        linkEdges.forEach((ce) => {
          graph.setItemState(ce, 'click', true);
          ce._cfg.group.attrs.opacity = 1;
        });
      });
  
      //点击空白处，全部出现
      graph.on('canvas:click',(e)=>{
        graph.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
          graph.setItemState(cn, 'click', false);
          cn._cfg.group.attrs.opacity = 1;
        });
        graph.cfg.edges.forEach((ce) => {
          graph.setItemState(ce, 'click', false);
          ce._cfg.group.attrs.opacity = 1;
        });
      })
  
      graph.on('node:dragstart', function (e) {
        graph.layout();
        refreshDragedNodePosition(e);
      });
      graph.on('node:drag', function (e) {
        refreshDragedNodePosition(e);
      });
      graph.on('node:dragend', function (e) {
        e.item.get('model').fx = null;
        e.item.get('model').fy = null;
      });
      
    }

    const CreateNode = function(id,className,hobby){
      let obj = {};
      obj.id =  id;
      obj.class = className;
      obj.label = id;
      obj.hobby =hobby;
      obj.type = 'circle';
      return obj;
    }
    
    const CreateEdge = function(source,target){
      let obj = {};
      obj.source = source;
      obj.target = target;
      return obj;
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