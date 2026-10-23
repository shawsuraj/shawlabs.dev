(function(){
  function $(s,r){return (r||document).querySelector(s);}
  function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
  function hhmm(m){m=Math.round(m);var h=Math.floor(m/60),mm=m%60;return (h<10?"0":"")+h+":"+(mm<10?"0":"")+mm;}

  /* ---------- The scale: tiles, leader lines, log axis ---------- */
  var scale=$("[data-scale]");
  if(scale){
    var tiles=$$(".tile",scale), svg=$(".leads",scale), axis=$(".axis",scale), ticks=$(".ticks",scale), gap=$(".gap-note",scale);
    var LBL=["1","10","100","1k","10k","100k","1M","10M","100M","1bn","10bn"];
    var WORDS=[[1,"you"],[2,"a pair"],[15,"a circle"],[120,"strangers"],[3e7,"everyone online"],[8.1e9,"the world"]];
    var cur=null;
    function frac(n){return Math.log(n)/Math.LN10/10;}
    function buildAxis(){
      var h="";
      for(var i=0;i<=10;i++){h+='<span class="tk" style="left:'+(i*10)+'%"><i></i>'+LBL[i]+'</span>';}
      WORDS.forEach(function(w){h+='<span class="wd" style="left:'+(frac(w[0])*100)+'%">'+w[1]+'</span>';});
      tiles.forEach(function(t){h+='<span class="dot" data-for="'+t.id+'" style="left:'+(frac(+t.dataset.n)*100)+'%"></span>';});
      ticks.innerHTML=h;
      gap.style.left=(frac(120)*100)+"%"; gap.style.width=((frac(3e7)-frac(120))*100)+"%";
    }
    function draw(){
      var box=scale.getBoundingClientRect(), ab=axis.getBoundingClientRect(), top=Infinity;
      tiles.forEach(function(t){top=Math.min(top,t.getBoundingClientRect().top);});
      svg.setAttribute("width",box.width); svg.setAttribute("height",ab.top-box.top);
      svg.style.width=box.width+"px"; svg.style.height=(ab.top-box.top)+"px";
      var ay=ab.top-box.top, p="";
      tiles.forEach(function(t){
        var r=t.getBoundingClientRect(), tx=r.left+r.width/2-box.left, ty=r.bottom-box.top;
        var dx=ab.left-box.left+frac(+t.dataset.n)*ab.width, k=Math.max(30,(ay-ty)*.55);
        p+='<path class="'+(t.id===cur?"on":"")+'" d="M'+tx+','+ty+' C'+tx+','+(ty+k)+' '+dx+','+(ay-k)+' '+dx+','+ay+'"/>';
      });
      svg.innerHTML=p;
    }
    function select(id,focus){
      cur="tab-"+id;
      tiles.forEach(function(t){var on=t.id===cur;t.setAttribute("aria-selected",on);t.tabIndex=on?0:-1;if(on&&focus)t.focus();});
      $$(".sp").forEach(function(s){s.hidden=s.id!=="sp-"+id;});
      $$(".dot",scale).forEach(function(d){d.classList.toggle("on",d.dataset.for===cur);});
      draw();
      try{history.replaceState(null,"","#"+id);}catch(e){}
    }
    tiles.forEach(function(t,i){
      t.addEventListener("click",function(){select(t.id.slice(4));});
      t.addEventListener("keydown",function(e){
        var j=e.key==="ArrowRight"?i+1:e.key==="ArrowLeft"?i-1:e.key==="Home"?0:e.key==="End"?tiles.length-1:null;
        if(j===null)return; e.preventDefault(); j=(j+tiles.length)%tiles.length; select(tiles[j].id.slice(4),true);
      });
    });
    buildAxis();
    var start=(location.hash||"").slice(1);
    select($("#tab-"+start)?start:"wc");
    window.addEventListener("resize",draw);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(draw);
  }

  /* ---------- Public Opinion: one question, a moving crowd ---------- */
  var po=$("[data-po]");
  if(po){
    var OPT=["Yes","No","Not sure"], votes=[612,341,251], mine=null, bars=$(".po-bars",po), note=$(".po-note",po), ticker=null, left=0;
    function render(){
      var tot=votes[0]+votes[1]+votes[2];
      bars.innerHTML=OPT.map(function(o,i){var pc=Math.round(votes[i]/tot*100);
        return '<div class="po-bar'+(mine===i?" me":"")+'"><span>'+o+(mine===i?" · you":"")+'</span><i style="width:'+pc+'%"></i><b>'+pc+'%</b></div>';}).join("");
      note.textContent=tot.toLocaleString("en-GB")+" votes. The crowd in this demo is simulated. The real one is not public yet.";
    }
    $$(".po-vote button",po).forEach(function(b){b.addEventListener("click",function(){
      if(mine!==null)votes[mine]--; mine=+b.dataset.v; votes[mine]++;
      $$(".po-vote button",po).forEach(function(x){x.setAttribute("aria-pressed",x===b);});
      po.classList.add("voted"); render(); left=14;
      if(!ticker)ticker=setInterval(function(){if(left--<=0){clearInterval(ticker);ticker=null;return;}
        var r=Math.random(); votes[r<.5?0:r<.78?1:2]+=1+Math.floor(Math.random()*4); render();},700);
    });});
  }

  /* ---------- LifeOS: a tiny model of one person ---------- */
  var lo=$("[data-lo]");
  if(lo){
    var DAYS=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], BASE=[410,425,440,415,460], vals=BASE.slice(), MIN=300, MAX=720;
    var wrap=$(".lo-days",lo), out=$(".lo-out",lo), plot=$(".lo-plot",lo);
    function stats(){var n=vals.length,m=vals.reduce(function(a,b){return a+b;},0)/n,v=vals.reduce(function(a,b){return a+(b-m)*(b-m);},0)/Math.max(1,n-1);return [m,Math.sqrt(v)];}
    function pos(m){return ((m-MIN)/(MAX-MIN)*100)+"%";}
    function render(){
      wrap.innerHTML=vals.map(function(v,i){return '<label><span>'+DAYS[i]+'</span><input type="range" min="'+MIN+'" max="'+MAX+'" step="5" value="'+v+'" data-i="'+i+'" aria-label="Wake time '+DAYS[i]+'"><b>'+hhmm(v)+'</b></label>';}).join("");
      $$("input",wrap).forEach(function(inp){inp.addEventListener("input",function(){vals[+inp.dataset.i]=+inp.value;inp.nextSibling.textContent=hhmm(+inp.value);update();});});
      update();
    }
    function update(){
      var s=stats(), m=s[0], sd=Math.max(5,s[1]);
      $("b",out).textContent=hhmm(m);
      $("span",out).textContent="tomorrow, give or take "+Math.round(sd)+" min";
      var h='<i class="band" style="left:'+pos(m-sd)+';width:'+((2*sd)/(MAX-MIN)*100)+'%"></i><i class="guess" style="left:'+pos(m)+'"></i>';
      vals.forEach(function(v){h+='<i class="pt" style="left:'+pos(v)+'"></i>';});
      h+='<span class="l">05:00</span><span class="r">12:00</span>';
      plot.innerHTML=h;
    }
    $(".lo-late",lo).addEventListener("click",function(){if(vals.length<7){vals.push(vals.length===5?645:690);render();}});
    $(".lo-reset",lo).addEventListener("click",function(){vals=BASE.slice();render();});
    render();
  }
})();
