
let detailData = document.getElementsByClassName('detail-data');
let relateData = document.getElementsByClassName('relate-data');
let graphData = {nodes:[],edges:[]}
const getDetail = function(){
  let id = '123';
  let url = 'http://112.74.37.0:5657/'+id+'/root-data';
  $.get(url,id,(res)=>{
    let root  = {
      id:id,
      label:id,
      class:'class1',
      style:{
        fill:'#f9f0ff',
        lineDash:'1'
      },
      labelCfg:{
        color:'#873bf4'
      },
    }
    let data = JSON.parse(res);
    graphData.nodes.push(root);
    detailData[0].innerHTML = data.id;
    detailData[1].innerHTML = eval(data.interest).join(',');
    relateData[0].innerHTML = data['ori-num'];
    relateData[1].innerHTML = data['predict-num'];
  })
}

  const getExistData = function(){
    let id = '123';
    let url = 'http://112.74.37.0:5657/'+id+'/ori-connections';
    $.get(url,id,(res)=>{
      let data = eval(JSON.parse(res));
      for(let n in data){
        graphData.nodes.push(CreateNode(n,'class2',eval(data[n])));
        graphData.edges.push(CreateEdge(id,n));
      }
      console.log(graphData)
    })
  }
  getDetail();
  getExistData()
  
  const test = {
    hobby:["电气","自动化","呵呵"],
    neibor:['node2','node8'],
    class:"1"
  }
  let dataTest = {
  nodes:[],
  edges:[]
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

let dataUp = function(dataGet){
  let rootId = dataGet.id;
  let connectNode = dataGet.connection;
  for(let i = 0;i < connectNode.length;i++){
    dataTest.edges.push(CreateEdge(rootId,connectNode[i]));
  }
  dataTest.nodes.push(CreateNode(rootId,dataGet.class));
}

 const tooltip = new G6.Tooltip({
  offsetX: 10,
  offsetY: 20,
  getContent(e) {
    const outDiv = document.createElement('div');
    outDiv.style.width = '120px';
    outDiv.innerHTML = `
      <li><span style="color:#b78dff;">ID:</span> ${e.item.getModel().id}</li>
      <span style="color:#b78dff;">科研兴趣:</span>
      <li> ${e.item.getModel().label || e.item.getModel().id}</li>
    `
    /* e.item.getModel().hobby.join(',') */
    return outDiv;
  },
  itemTypes: ['node']
});
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


const graph = new G6.Graph({
  container:'graph-exist',
  layout:{
    type:'force',
    nodeStrength: -100,
    collideStrength: 0.7,
    alphaDecay: 0.01,
    preventOverlap: true,
    linkDistance:100,
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
  plugins:[tooltip],
});



/* let data = {
  nodes:[
    {
      id:'node1',
   
      style:{
        fill:'#f9f0ff',
        lineDash:'1'
      },
      labelCfg:{
        color:'#873bf4'
      },
      class:'class1',
    },
    {
      id:'node2',
      type:'circle',
     
    
    },
    {
      id:'node3',
      type:'circle',
      
      
    },
    {
      id:'node4',
      type:'circle',
      
      
    },
    {
      id:'node5',
      type:'circle',
      
     
    },
    {
      id:'node6',
      type:'circle',
      
    },
    {
      id:'node7',
      type:'circle',
     
    
    },
    {
      id:'node8',
      type:'circle',
     
    
    },
    {
      id:'node9',
      type:'circle',
    
 
    },
    {
      id:'node10',
      type:'circle',
     
  
    },
    {
      id:'node11',
      type:'circle',
     
    
    }
  ],
  edges:[
    {
      source:'node1',
      target:'node2',
      id:'edge1',
    },
    {
      source:'node1',
      target:'node3',
     
    },
    {
      source:'node1',
      target:'node5',
     
    },{
      source:'node1',
      target:'node4',
     
    },{
      source:'node1',
      target:'node6',
     
    },{
      source:'node1',
      target:'node7',
     
    },{
      source:'node1',
      target:'node8',
     
    },{
      source:'node9',
      target:'node8',
     
    },{
      source:'node9',
      target:'node10',
    },{
      source:'node9',
      target:'node11',
    }
  ]
} */


graph.data(graphData);
const nodes =graphData.nodes;
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
graph.render(); // 渲染


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
const modelHide = {
  style:{
    opacity:0.3
  }
}
// 点击节点
graph.on('node:click', (e) => {
  // 先将所有当前是 click 状态的节点置为非 click 状态

  const nodeItem = e.item; // 获取被点击的节点元素对象
  const linkNodes = Object.assign(nodeItem.getNeighbors('target'),nodeItem.getNeighbors('source'));
  const linkEdges = nodeItem.getEdges();
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
function refreshDragedNodePosition(e) {
  const modelDrag = e.item.get('model');
  modelDrag.fx = e.x;
  modelDrag.fy = e.y;
}
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


