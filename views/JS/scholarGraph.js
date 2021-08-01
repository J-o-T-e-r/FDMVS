
let detailData = document.getElementsByClassName('detail-data');
let relateData = document.getElementsByClassName('relate-data');
let graphData1 = {nodes:[],edges:[]};
let graphData2 = {nodes:[],edges:[]};
/* let id = 'http://112.74.37.0:5657/1548/page'.split('/')[3]; */
let id = location.href.slice(location.href.indexOf("?")+1)
console.log(id);
let btn = document.getElementsByClassName('btn');
let graphExist = document.getElementById('graph-exist');
let graphPredict = document.getElementById('graph-predict');
let userbtn = document.getElementsByClassName('user-btn');

userbtn[1].onclick = ()=>{
  sessionStorage.removeItem('token');
  location.href = '../html/log-reg.html';
}

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

const loadData = function(){

  getDetail(id);
}

function randomNum(minNum,maxNum){ 
  switch(arguments.length){ 
      case 1:  return parseInt(Math.random()*minNum+1,10); 
      case 2:  return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);  
      default: return 0; 
  } 
} 
const getDetail = function(id){
  
  let dataT = {
    id:id,
  }
  let url = 'http://112.74.37.0:5657/'+id+'/root-data';
  $.get(url,dataT,(res)=>{
    let data = JSON.parse(res);
    let root  = {
      id:id,
      label:id,
      class:'class1',
      hobby:[eval(data.interest).join(',')],
      style:{
        fill:'#f9f0ff',
        lineDash:'1'
      },
      labelCfg:{
        color:'#873bf4'
      },
    }
    
    graphData1.nodes.push(root);
    graphData2.nodes.push(root);
    detailData[0].innerHTML = data.id;
    detailData[1].innerHTML = eval(data.interest).join(',');
    relateData[0].innerHTML = data['ori-num'];
    relateData[1].innerHTML = data['predict-num'];
    getExistData();
  })
}
function refreshDragedNodePosition(e) {
  const modelDrag = e.item.get('model');
  modelDrag.fx = e.x;
  modelDrag.fy = e.y;
}
const tooltip1 = new G6.Tooltip({
  offsetX: 10,
  offsetY: 20,
  getContent(e) {
    const outDiv = document.createElement('div');
    outDiv.style.width = '120px';
    outDiv.innerHTML = `
      <li><span style="color:#b78dff;">ID:</span> ${e.item.getModel().id}</li>
      <span style="color:#b78dff;">科研兴趣:</span>
      <li> ${e.item.getModel().hobby.join(',')}</li>
    `
    
    return outDiv;
  },
  itemTypes: ['node']
});
const tooltip2 = new G6.Tooltip({
  offsetX: 10,
  offsetY: 20,
  getContent(e) {
    const outDiv = document.createElement('div');
    outDiv.style.width = '120px';
    outDiv.innerHTML = `
      <li><span style="color:#b78dff;">ID:</span> ${e.item.getModel().id}</li>
      <span style="color:#b78dff;">科研兴趣:</span>
      <li> ${e.item.getModel().hobby.join(',')}</li>
    `
    
    return outDiv;
  },
  itemTypes: ['node']
});
  const createGraph1 = function(){
    const graph1 = new G6.Graph({
      container:'graph-exist',
      layout:{
        type:'force',
        nodeStrength: -100,
        collideStrength: 0.7,
        alphaDecay: 0.01,
        preventOverlap: true,
        linkDistance:d=>{
        
          return randomNum(100,300);
        }
      },
      width:910,
      height:550,
      fitView: true,
      fitViewPadding: [20, 40, 50, 20],
      modes: {
        default: ['drag-canvas', 'zoom-canvas', 'drag-node'], // 允许拖拽画布、放缩画布、拖拽节点
      
      },
      defaultNode:{
        type:'circle-animate',
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
      plugins:[tooltip1],
    });

    graph1.data(graphData1);
      const nodes =graphData1.nodes;
      nodes.forEach((node)=>{
        if(!node.style){
          node.style = {};
        }
      
        switch(node.class){
          case 'class1':{
            node.size = 60;     
            break;
          }
          case 'class2':{
            node.size = 40;
            break;
          }
          default:{
            node.size = 20; 
          }
        }
      })
      graph1.render(); 
      // 鼠标进入节点
    graph1.on('node:mouseenter', (e) => {
      const nodeItem = e.item; // 获取鼠标进入的节点元素对象
      graph1.setItemState(nodeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
    });

    // 鼠标离开节点
    graph1.on('node:mouseleave', (e) => {
      const nodeItem = e.item; // 获取鼠标离开的节点元素对象
      graph1.setItemState(nodeItem, 'hover', false); // 设置当前节点的 hover 状态为 false
    });
    graph1.on('edge:mouseenter', (e) => {
      const edgeItem = e.item; // 获取鼠标进入的节点元素对象
      graph1.setItemState(edgeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
    });

    // 鼠标离开边
    graph1.on('edge:mouseleave', (e) => {
      const edgeItem = e.item; // 获取鼠标离开的边元素对象
      graph1.setItemState(edgeItem, 'hover', false); // 设置当前边的 hover 状态为 false
    });
 
    // 点击节点
    graph1.on('node:click', (e) => {
      // 先将所有当前是 click 状态的节点置为非 click 状态

      const nodeItem = e.item; // 获取被点击的节点元素对象
      const linkNodes = Object.assign(nodeItem.getNeighbors('target'),nodeItem.getNeighbors('source'));
      const linkEdges = nodeItem.getEdges();
      graph1.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
        graph1.setItemState(cn, 'click', false);
        cn._cfg.group.attrs.opacity = 0.3;
      });
      graph1.cfg.edges.forEach((ce) => {
        graph1.setItemState(ce, 'click', false);
        ce._cfg.group.attrs.opacity = 0.3;
      });
      graph1.setItemState(nodeItem, 'click', true); // 设置当前节点的 click 状态为 true
      nodeItem._cfg.group.attrs.opacity = 1;
      linkNodes.forEach((cn) => { 
        graph1.setItemState(cn, 'click', true);
        cn._cfg.group.attrs.opacity = 1;
      });
      linkEdges.forEach((ce) => {
        graph1.setItemState(ce, 'click', true);
        ce._cfg.group.attrs.opacity = 1;
      });
    });

    //点击空白处，全部出现
    graph1.on('canvas:click',(e)=>{
      graph1.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
        graph1.setItemState(cn, 'click', false);
        cn._cfg.group.attrs.opacity = 1;
      });
      graph1.cfg.edges.forEach((ce) => {
        graph1.setItemState(ce, 'click', false);
        ce._cfg.group.attrs.opacity = 1;
      });
    })

    graph1.on('node:dragstart', function (e) {
      graph1.layout();
      refreshDragedNodePosition(e);
    });
    graph1.on('node:drag', function (e) {
      refreshDragedNodePosition(e);
    });
    graph1.on('node:dragend', function (e) {
      e.item.get('model').fx = null;
      e.item.get('model').fy = null;
    });
    
  }

  const createGraph2 = function(){
    const graph2 = new G6.Graph({
      container:'graph-predict',
      layout:{
        type:'force',
        nodeStrength: -100,
        collideStrength: 0.7,
        alphaDecay: 0.01,
        preventOverlap: true,
        linkDistance:d=>{
          let len = d.target.id;
          if(len > 400 && len <800){
            return len*0.75;
          }else if(len<400){
            return len*0.8;
          }else if(len>800 && len < 1200){
            return len*0.75*0.25;
          }
          else if(len>1200 &&  len < 1600){
            return len*0.75*0.25*0.25
          }
          else if(len>1600 &&  len < 2000){
            return len*0.75*0.25*0.25*0.25;
          }
          else if(len>2400 &&  len < 2800){
            return len*0.75*0.25*0.25*0.25*0.25;
          }else{
            return 400;
          }
        }
      },
      width:910,
      height:550,
      fitView: true,
      fitViewPadding: [20, 40, 50, 20],
      modes: {
        default: ['drag-canvas', 'zoom-canvas', 'drag-node'], // 允许拖拽画布、放缩画布、拖拽节点
      
      },
      defaultNode:{
        type:'circle-animate',
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
          lineWidth:1.5,
          lineDash:[5,8]
        },
       
      },
      edgeStateStyles: {
        // 鼠标点击边，即 click 状态为 true 时的样式
        
        hover: {
          stroke: '#ffab57',
        },
      },
      plugins:[tooltip2],
    });

    graph2.data(graphData2);
      const nodes =graphData2.nodes;
      nodes.forEach((node)=>{
        if(!node.style){
          node.style = {};
        }
        switch(node.class){
          case 'class1':{
            node.size = 60;     
            break;
          }
          case 'class2':{
            node.size = 40;
            break;
          }
          default:{
            node.size = 20; 
          }
        }
      })
      graph2.render(); 
      // 鼠标进入节点
    graph2.on('node:mouseenter', (e) => {
      const nodeItem = e.item; // 获取鼠标进入的节点元素对象
      graph2.setItemState(nodeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
    });

    // 鼠标离开节点
    graph2.on('node:mouseleave', (e) => {
      const nodeItem = e.item; // 获取鼠标离开的节点元素对象
      graph2.setItemState(nodeItem, 'hover', false); // 设置当前节点的 hover 状态为 false
    });
    graph2.on('edge:mouseenter', (e) => {
      const edgeItem = e.item; // 获取鼠标进入的节点元素对象
      graph2.setItemState(edgeItem, 'hover', true); // 设置当前节点的 hover 状态为 true
    });

    // 鼠标离开边
    graph2.on('edge:mouseleave', (e) => {
      const edgeItem = e.item; // 获取鼠标离开的边元素对象
      graph2.setItemState(edgeItem, 'hover', false); // 设置当前边的 hover 状态为 false
    });

    // 点击节点
    graph2.on('node:click', (e) => {
      // 先将所有当前是 click 状态的节点置为非 click 状态

      const nodeItem = e.item; // 获取被点击的节点元素对象
      const linkNodes = Object.assign(nodeItem.getNeighbors('target'),nodeItem.getNeighbors('source'));
      const linkEdges = nodeItem.getEdges();
      graph2.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
        graph2.setItemState(cn, 'click', false);
        cn._cfg.group.attrs.opacity = 0.3;
      });
      graph2.cfg.edges.forEach((ce) => {
        graph2.setItemState(ce, 'click', false);
        ce._cfg.group.attrs.opacity = 0.3;
      });
      graph2.setItemState(nodeItem, 'click', true); // 设置当前节点的 click 状态为 true
      nodeItem._cfg.group.attrs.opacity = 1;
      linkNodes.forEach((cn) => { 
        graph2.setItemState(cn, 'click', true);
        cn._cfg.group.attrs.opacity = 1;
      });
      linkEdges.forEach((ce) => {
        graph2.setItemState(ce, 'click', true);
        ce._cfg.group.attrs.opacity = 1;
      });
    });

    //点击空白处，全部出现
    graph2.on('canvas:click',(e)=>{
      graph2.cfg.nodes.forEach((cn) => {    //把所有click的节点和边设为非click
        graph2.setItemState(cn, 'click', false);
        cn._cfg.group.attrs.opacity = 1;
      });
      graph2.cfg.edges.forEach((ce) => {
        graph2.setItemState(ce, 'click', false);
        ce._cfg.group.attrs.opacity = 1;
      });
    })

    graph2.on('node:dragstart', function (e) {
      graph2.layout();
      refreshDragedNodePosition(e);
    });
    graph2.on('node:drag', function (e) {
      refreshDragedNodePosition(e);
    });
    graph2.on('node:dragend', function (e) {
      e.item.get('model').fx = null;
      e.item.get('model').fy = null;
    });
  }
  const getExistData = function(id){

    let url = 'http://112.74.37.0:5657/'+id+'/ori-connections';
    $.get(url,id,(res)=>{
      let data = eval(JSON.parse(res));
      for(let n in data){
        graphData1.nodes.push(CreateNode(n,'class2',eval(data[n])));
        graphData1.edges.push(CreateEdge(id,n));
      }
      createGraph1();
      getPredictData();
    })
  }
  const getPredictData = function(){
    let url = 'http://112.74.37.0:5657/'+id+'/predict-connections';
    $.get(url,(res)=>{
      let data = eval(JSON.parse(res));
      for(let n in data){
        graphData2.nodes.push(CreateNode(n,'class2',eval(data[n])));
        graphData2.edges.push(CreateEdge(id,n));
      }
      createGraph2();
    })
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



  G6.registerNode(
    'circle-animate',
    {
      afterDraw(cfg, group) {
        // 获取该节点上的第一个图形
        const shape = group.get('children')[0];
        // 该图形的动画
        shape.animate(
          (ratio) => {
            // 每一帧的操作，入参 ratio：这一帧的比例值（Number）。返回值：这一帧需要变化的参数集（Object）。
            // 先变大、再变小
            const diff = ratio <= 0.5 ? ratio * 10 : (1 - ratio) * 10;
            let radius = cfg.size;
            if (isNaN(radius)) radius = radius[0];
            // 返回这一帧需要变化的参数集，这里只包含了半径
            return {
              r: radius / 2 + diff,
            };
          },
          {
            // 动画重复
            repeat: true,
            duration: 3000,
            easing: 'easeCubic',
          },
        ); // 一次动画持续的时长为 3000，动画效果为 'easeCubic'
      },
    },
    'circle',
);


loadData();










