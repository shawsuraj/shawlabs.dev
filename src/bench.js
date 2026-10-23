(function(){
  function $(s,r){return (r||document).querySelector(s);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}

  /* ---------- World Chaos Map: live board ---------- */
  var wcm=$("[data-wcm]");
  if(wcm){
    var NAMES={YE:"Yemen",SD:"Sudan",UA:"Ukraine",RU:"Russia",MM:"Myanmar",FR:"France",PS:"Palestine",IL:"Israel",SY:"Syria",HT:"Haiti",CD:"DR Congo",SO:"Somalia",AF:"Afghanistan",MU:"Mauritius",AL:"Albania",PK:"Pakistan",IN:"India",NG:"Nigeria",ML:"Mali",ET:"Ethiopia",LB:"Lebanon",IR:"Iran",IQ:"Iraq",VE:"Venezuela",MX:"Mexico",CO:"Colombia",BD:"Bangladesh",KE:"Kenya",BF:"Burkina Faso",NE:"Niger",TD:"Chad",CF:"Central African Republic",SS:"South Sudan",LY:"Libya",US:"United States",GB:"United Kingdom",DE:"Germany",TR:"Turkey",SA:"Saudi Arabia",EG:"Egypt"};
    var COL={stable:"var(--stable)",moderate:"var(--moderate)",unstable:"var(--unstable)",severe:"var(--severe)"};
    function regionName(iso){try{return new Intl.DisplayNames(["en"],{type:"region"}).of(iso)||iso;}catch(e){return iso;}}
    function band(s){return s>=85?"severe":s>=60?"unstable":s>=30?"moderate":"stable";}
    // Fallback: real scores seen on the live map on 23 Oct 2026, shown only if the live feed cannot be reached.
    var FALLBACK={generated_at:"2026-10-23T10:00:00Z",fallback:true,counts:{stable:110,moderate:22,unstable:8,severe:7},
      countries:[{country_iso:"YE",score:97},{country_iso:"SD",score:97},{country_iso:"FR",score:93},{country_iso:"UA",score:93},{country_iso:"RU",score:93}]};
    function draw(d){
      var counts={stable:0,moderate:0,unstable:0,severe:0}, list=d.countries||[];
      if(d.counts)counts=d.counts; else list.forEach(function(c){counts[band(c.score)]++;});
      var total=counts.stable+counts.moderate+counts.unstable+counts.severe||1;
      $(".wcm-bands",wcm).innerHTML=["stable","moderate","unstable","severe"].map(function(b){return '<span style="width:'+(counts[b]/total*100)+'%;background:'+COL[b]+'"></span>';}).join("");
      $(".wcm-count",wcm).innerHTML=["stable","moderate","unstable","severe"].map(function(b){return '<div><b style="color:'+COL[b]+'">'+counts[b]+'</b>'+b[0].toUpperCase()+b.slice(1)+'</div>';}).join("");
      var top=list.slice().sort(function(a,b){return b.score-a.score;}).slice(0,5);
      $(".wcm-top",wcm).innerHTML=top.map(function(c,i){var s=Math.round(c.score),bb=band(s),name=NAMES[c.country_iso]||regionName(c.country_iso);
        return '<li><span>'+(i+1)+'</span><span>'+esc(name)+'<div class="bar"><i style="width:'+s+'%;background:'+COL[bb]+'"></i></div></span><b style="color:'+COL[bb]+'">'+s+'</b></li>';}).join("");
      var t=new Date(d.generated_at), h=Math.max(0,Math.round((Date.now()-t)/36e5));
      $(".wcm-now .lbl span",wcm).textContent=d.fallback?"Scores from 23 Oct 2026 · live feed not reachable here":(h<1?"Live · updated within the hour":"Live · updated "+h+"h ago");
    }
    draw(FALLBACK);
    if(location.protocol.indexOf("http")===0&&!/claude/.test(location.hostname)){
      fetch("/live/wcm",{cache:"no-store"}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(d){if(d&&d.countries&&d.countries.length)draw(d);}).catch(function(){});
    }
  }

  /* ---------- One Sentence: write once, let go ---------- */
  var os=$("[data-os]");
  if(os){
    var STORY=["The lighthouse keeper had not spoken to anyone in eleven days.","On the twelfth, a letter washed up with her name already on it.","She did not open it until the tide went out.","Inside was a single sentence, written in her own handwriting.","It said: do not trust the boat that comes at dawn.","At dawn, a boat came."];
    var idx=0, prev=$(".os-prev span",os), ta=$("textarea",os), go=$(".os-go",os), gone=$(".os-gone",os);
    prev.textContent=STORY[0];
    ta.addEventListener("input",function(){go.disabled=ta.value.trim().length<3;});
    go.addEventListener("click",function(){
      var line=ta.value.trim(); if(line.length<3)return;
      gone.textContent="“"+line+"”"; gone.classList.remove("os-fly"); void gone.offsetWidth; gone.classList.add("os-fly");
      ta.value=""; go.disabled=true;
      prev.parentNode.style.opacity=0;
      setTimeout(function(){idx=(idx+1)%STORY.length;prev.textContent=STORY[idx];prev.parentNode.style.opacity=1;
        $(".os-note",os).textContent="Passed on. The next stranger sees only your line. You will not see what they write.";},900);
    });
  }

  /* ---------- MaetriXs: grow a social graph ---------- */
  var mx=$("[data-mx]");
  if(mx){
    var svg=$("svg",mx), xpEl=$(".mx-xp b",mx), xp=0, nodes=[], W=600, H=210, cx=W/2, cy=H/2;
    function render(){
      var s='<defs><linearGradient id="mxg" x1="0" x2="1"><stop offset="0" stop-color="#5b8def"/><stop offset="1" stop-color="#d65fc4"/></linearGradient></defs>';
      nodes.forEach(function(n){s+='<line x1="'+cx+'" y1="'+cy+'" x2="'+n.x+'" y2="'+n.y+'" stroke="url(#mxg)" stroke-width="'+(1+n.w)+'" opacity=".7"/>';});
      nodes.forEach(function(n,i){s+='<g class="'+(i===nodes.length-1?"mx-pop":"")+'" style="transform-origin:'+n.x+'px '+n.y+'px"><circle cx="'+n.x+'" cy="'+n.y+'" r="'+(7+n.w*2)+'" fill="#2a2b36" stroke="#d65fc4" stroke-width="1.5"/><text x="'+n.x+'" y="'+(n.y+(n.y>cy?24:-14))+'" fill="#9a9ab0" font-size="11" text-anchor="middle" font-family="sans-serif">'+n.t+'</text></g>';});
      s+='<circle cx="'+cx+'" cy="'+cy+'" r="18" fill="url(#mxg)"/><text x="'+cx+'" y="'+(cy+4)+'" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">You</text>';
      svg.innerHTML=s; xpEl.textContent=xp;
    }
    mx.querySelectorAll(".mx-acts button").forEach(function(b){b.addEventListener("click",function(){
      xp+=+b.dataset.xp;
      var who=b.dataset.who, ex=nodes.filter(function(n){return n.t===who;})[0];
      if(ex&&b.dataset.again){ex.w=Math.min(4,ex.w+1);}
      else{var a=nodes.length*2.39996+0.6, r=62+((nodes.length*37)%38);nodes.push({x:cx+Math.cos(a)*r*2.2,y:cy+Math.sin(a)*r*.95,t:who,w:1}); if(nodes.length>12)nodes.shift();}
      render();
    });});
    render();
  }

  /* ---------- VerumVeil: Emoji Crypt ---------- */
  var vv=$("[data-vv]");
  if(vv){
    var EM=Array.from("😀😃😄😁😆😅😂🙂🙃😉😊😇🥰😍🤩😘😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯🤠🥳😎🤓🧐😕😟🙁😮😯😲😳🥺");
    var B64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    function rng(seed){return function(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return ((seed>>>0)%100000)/100000;};}
    function table(pw){var h=2166136261;for(var i=0;i<pw.length;i++){h^=pw.charCodeAt(i);h=Math.imul(h,16777619);}var r=rng(h>>>0||1),t=EM.slice();for(var j=t.length-1;j>0;j--){var k=Math.floor(r()*(j+1));var x=t[j];t[j]=t[k];t[k]=x;}return t;}
    function enc(msg,pw){var b=btoa(unescape(encodeURIComponent("vv|"+msg))).replace(/=+$/,""),t=table(pw);return Array.from(b).map(function(c){return t[B64.indexOf(c)];}).join("");}
    function dec(s,pw){var t=table(pw);var b=Array.from(s.replace(/\s/g,"")).map(function(e){var i=t.indexOf(e);if(i<0)throw 0;return B64[i];}).join("");while(b.length%4)b+="=";var m=decodeURIComponent(escape(atob(b)));if(m.slice(0,3)!=="vv|")throw 0;return m.slice(3);}
    var msg=$("#vv-msg"),pw=$("#vv-pw"),out=$(".vv-out",vv),st=$(".vv-status",vv);
    $("#vv-enc").addEventListener("click",function(){out.textContent=enc(msg.value||"meet me at nine",pw.value||"veil");st.textContent="Sealed. Only the same password turns this back into words. Try decoding it with a different one.";});
    $("#vv-dec").addEventListener("click",function(){try{var m=dec(out.textContent,pw.value||"veil");msg.value=m;st.textContent="Opened with that password.";}catch(e){st.textContent="Wrong password. It stays a row of faces.";}});
    out.textContent=enc("meet me at nine","veil");
  }

  /* ---------- Last Drink: pace the night ---------- */
  var ld=$("[data-ld]");
  if(ld){
    var t=20*60, pts=0, drinks=[], lastWasDrink=false, scoreEl=$(".ld-score b",ld), clock=$(".ld-clock",ld), msgEl=$(".ld-msg",ld), log=$(".ld-log",ld);
    var HOUR_CAP=2, NIGHT_CAP=6;
    function hhmm(m){var h=Math.floor(m/60)%24,mm=m%60;return (h<10?"0":"")+h+":"+(mm<10?"0":"")+mm;}
    function upd(text){scoreEl.textContent=pts;clock.textContent="It is "+hhmm(t)+". Drinks tonight: "+drinks.length+".";if(text){msgEl.textContent=text;log.insertAdjacentHTML("afterbegin","<li>"+hhmm(t)+" · "+esc(text)+"</li>");}}
    function lastHour(){return drinks.filter(function(d){return t-d<60;}).length;}
    ld.querySelectorAll(".ld-acts button").forEach(function(b){b.addEventListener("click",function(){
      var k=b.dataset.k;
      if(k==="time"){t+=30;lastWasDrink=lastWasDrink;upd("Half an hour passes.");return;}
      if(k==="water"){
        if(lastWasDrink){pts+=5;lastWasDrink=false;upd("Water between rounds. +5");}
        else upd("Water is great, but it only earns points between drinks. No farming.");
        return;}
      drinks.push(t); var h=lastHour();
      lastWasDrink=true;
      if(drinks.length>NIGHT_CAP){upd("Past tonight's cap. No more points, and that is the point.");}
      else if(h>HOUR_CAP){upd(h>=4?"That is "+h+" in an hour. Slow down, have some water.":"Hourly cap reached. This one earns nothing.");}
      else{pts+=10;upd((k==="pint"?"A pint":"A cocktail")+". +10");}
    });});
    upd();
  }
})();
