/* A small, in-browser version of World Chaos Map's harm signal.
   Constants are the real ones from packages/core/src/scoring/tuning.ts (v3.2.0).
   The production model reads far more patterns, weighs attribution and coverage,
   and then works across days and weeks. This only reads one headline. */
(function(){
  var root=document.querySelector("[data-explorer]"); if(!root) return;
  var input=root.querySelector("input"), marked=root.querySelector(".marked"), terms=root.querySelector(".terms"),
      num=root.querySelector(".gauge .n"), pin=root.querySelector(".gauge .scale b"), note=root.querySelector(".gauge p");
  var E={DEATH_BASE:.40,DEATH_SLOPE:.18,INJURY_BASE:.18,INJURY_SLOPE:.12,ARREST_BASE:.15,ARREST_SLOPE:.14,CROWD_BASE:.20,CROWD_SLOPE:.10,
         KINETIC_STRONG:.50,KINETIC_WEAK:.25,UNREST:.35,DESTRUCTION:.35,PROTEST:.15,EMERGENCY:.45,MAX:.95};
  var D={DIPLOMATIC:.35,HYPOTHETICAL:.60,WEAPONS_TEST:.35,JUDICIAL:.50,OFF_TOPIC:.10,HISTORICAL:.15};
  var WORDNUM={a:1,an:1,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,dozen:12,dozens:24,scores:40,hundreds:200,thousands:2000};
  function n(s){s=s.toLowerCase().replace(/,/g,"");if(WORDNUM[s])return WORDNUM[s];var v=parseFloat(s);if(/k$/.test(s))v*=1000;return isNaN(v)?0:v;}
  function ev(c,b,s,p){return Math.min(E.MAX,b+s*Math.log10(Math.max(1,c/p)));}
  var NUM="(\\d[\\d,.]*k?|a|an|one|two|three|four|five|six|seven|eight|nine|ten|dozens?|scores|hundreds|thousands)";
  var R={
    death:[new RegExp("\\b(?:kills?|killing|killed)\\s+(?:at least\\s+)?"+NUM,"i"),new RegExp(NUM+"\\s+(?:people\\s+|civilians\\s+|soldiers\\s+)?(?:killed|dead|die|died|deaths)","i"),new RegExp("death toll (?:rises to|reaches|hits)\\s+"+NUM,"i")],
    injury:[new RegExp(NUM+"\\s+(?:people\\s+)?(?:injured|wounded|hurt)","i"),new RegExp("(?:injures|wounds)\\s+"+NUM,"i")],
    arrest:[new RegExp(NUM+"\\s+(?:people\\s+|protesters\\s+)?(?:arrested|detained)","i"),new RegExp("(?:arrests?|detains?)\\s+"+NUM,"i")],
    crowd:[new RegExp(NUM+"\\s+(?:people\\s+)?(?:march|protest|protesters|rally|demonstrators)","i")],
    kinStrong:/\b(air ?strikes?|drone strikes?|missile strikes?|shelling|shelled|car bomb|bombardment|ground offensive|airstrike)\b/i,
    kinWeak:/\b(attack(?:s|ed)?|fighting|explosions?|gunfire|gunmen|clashes)\b/i,
    unrest:/\b(riots?|rioting|tear gas|riot police|clash(?:es|ed)? with police|water cannon)\b/i,
    destruction:/\b(loot(?:ing|ed)?|arson|torched|set (?:on )?fire|burn(?:ed|t) cars)\b/i,
    emergency:/\b(curfew|martial law|coup|state of emergency|internet shut ?down)\b/i,
    protest:/\b(protests?|protesters|march(?:es)?|rally|demonstrations?|walkout)\b/i,
    diplomatic:/\b(blasts|slams|condemns?|criticises|criticizes|rejects|denies|accuses|defends|blames|summons|urges|warns)\b/i,
    hypothetical:/\b(braces? for|could|may|might|fears?|ahead of|threatens?|plans? to)\b/i,
    weapons:/\b(missile test|weapons test|test[- ]fires?|military drills?|war games)\b/i,
    judicial:/\b(trial|court|sentenced|jailed for|convicted|verdict)\b/i,
    offtopic:/\b(football|match|film|movie|concert|festival|fireworks|celebrat\w*|cup final)\b/i,
    historical:/\b(anniversary|remembers|years ago|commemorat\w*)\b/i
  };
  function find(list,t){for(var i=0;i<list.length;i++){var m=t.match(list[i]);if(m)return m;}return null;}
  function esc(s){return s.replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}

  function read(t){
    var hits=[], items=[];
    function add(key,label,why,val,color,m){items.push({key:key,label:label,why:why,val:val,color:color});if(m)hits.push({s:m[0],c:color});}
    var m;
    var deaths=0;
    if((m=find(R.death,t))){deaths=n(m[1]);if(deaths>0)add("death","Deaths",deaths+" reported",ev(deaths,E.DEATH_BASE,E.DEATH_SLOPE,1),"var(--e-death)",m);}
    else if((m=t.match(/\b(kills?|killed|dead|deadly)\b/i))){deaths=1;add("death","Deaths","at least 1",ev(1,E.DEATH_BASE,E.DEATH_SLOPE,1),"var(--e-death)",m);}
    if((m=find(R.injury,t))){var inj=n(m[1]);add("injury","Injuries",inj+" reported",ev(inj,E.INJURY_BASE,E.INJURY_SLOPE,1),"var(--e-death)",m);}
    var unrestCtx=R.unrest.test(t)||R.protest.test(t);
    if((m=find(R.arrest,t))){var ar=n(m[1]);var v=ev(ar,E.ARREST_BASE,E.ARREST_SLOPE,10);if(!unrestCtx)v*=.5;add("arrest","Arrests",ar.toLocaleString("en-GB")+(unrestCtx?" during unrest":" (policing news, halved)"),v,"var(--e-unrest)",m);}
    if((m=find(R.crowd,t))){var cr=n(m[1]);if(cr>=500)add("crowd","Crowd size",cr.toLocaleString("en-GB")+" people",ev(cr,E.CROWD_BASE,E.CROWD_SLOPE,1000),"var(--e-unrest)",m);}
    if((m=t.match(R.kinStrong)))add("kin","Heavy weapons","airstrike, shelling, car bomb",E.KINETIC_STRONG,"var(--e-kin)",m);
    else if((m=t.match(R.kinWeak)))add("kin","Fighting or attack","weaker armed signal",E.KINETIC_WEAK,"var(--e-kin)",m);
    if((m=t.match(R.unrest)))add("unrest","Riot violence","riots, tear gas, police clashes",E.UNREST,"var(--e-unrest)",m);
    if((m=t.match(R.destruction)))add("destr","Destruction","looting, arson",E.DESTRUCTION,"var(--e-unrest)",m);
    if((m=t.match(R.emergency)))add("emerg","Emergency powers","curfew, martial law, coup",E.EMERGENCY,"var(--e-emerg)",m);
    if(!items.some(function(i){return i.key==="unrest"||i.key==="crowd";})&&(m=t.match(R.protest)))add("protest","Protest","a peaceful protest or strike",E.PROTEST,"var(--e-unrest)",m);

    var keep=items.reduce(function(p,i){return p*(1-i.val);},1), harm=1-keep;
    var hard=items.some(function(i){return /death|injury|kin|destr|emerg/.test(i.key);});
    var damp=null;
    function dm(re,val,label){var mm=t.match(re);if(mm&&(!damp||val<damp.val)){damp={val:val,label:label};hits.push({s:mm[0],c:"var(--e-damp)"});}}
    if(!hard)dm(R.diplomatic,D.DIPLOMATIC,"a reaction or statement, not an event");
    dm(R.hypothetical,D.HYPOTHETICAL,"something that has not happened yet");
    dm(R.weapons,D.WEAPONS_TEST,"a weapons test, tension not chaos");
    dm(R.judicial,D.JUDICIAL,"a court case about the past");
    dm(R.offtopic,D.OFF_TOPIC,"sport or entertainment");
    dm(R.historical,D.HISTORICAL,"an anniversary");
    if(damp)harm*=damp.val;
    var capped=false;
    var unrestOnly=deaths===0&&items.some(function(i){return /unrest|arrest|crowd|protest|emerg|destr/.test(i.key);})&&!items.some(function(i){return i.key==="kin";});
    if(unrestOnly&&harm>.6){harm=.6;capped=true;}
    return {items:items,hits:hits,harm:Math.max(0,Math.min(1,harm)),damp:damp,capped:capped,deaths:deaths};
  }

  function render(){
    var t=input.value.trim(); var r=read(t);
    // highlight matches in order of appearance
    var html=esc(t), done={};
    r.hits.sort(function(a,b){return b.s.length-a.s.length;}).forEach(function(h){
      if(done[h.s.toLowerCase()])return; done[h.s.toLowerCase()]=1;
      var i=html.toLowerCase().indexOf(esc(h.s).toLowerCase()); if(i<0)return;
      html=html.slice(0,i)+'<mark style="--c:'+h.c+'">'+html.slice(i,i+esc(h.s).length)+'</mark>'+html.slice(i+esc(h.s).length);
    });
    marked.innerHTML=html||"&nbsp;";
    var rows=r.items.map(function(i){return '<li style="--c:'+i.color+'"><span class="what">'+i.label+'<small>'+esc(i.why)+'</small></span><span class="bar"><i style="width:'+Math.round(i.val*100)+'%"></i></span><span class="v">'+i.val.toFixed(2)+'</span></li>';});
    if(r.damp)rows.push('<li style="--c:var(--e-damp)"><span class="what">Dampener × '+r.damp.val.toFixed(2)+'<small>'+r.damp.label+'</small></span><span class="bar"><i style="width:'+Math.round(r.damp.val*100)+'%"></i></span><span class="v">×'+r.damp.val.toFixed(2)+'</span></li>');
    if(r.capped)rows.push('<li style="--c:var(--ink-3)"><span class="what">Capped at 0.60<small>no reported death, so it stays below lethal violence</small></span><span class="bar"><i style="width:60%"></i></span><span class="v">0.60</span></li>');
    terms.innerHTML=rows.length?rows.join(""):'<li class="none">No hard evidence found. To the map, this headline is close to noise.</li>';
    num.textContent=r.harm.toFixed(2);
    pin.style.left=(r.harm*100)+"%";
    var h=r.harm, say;
    if(h>=.7)say="Among the heaviest single articles the map sees. One story like this can set a country's whole day.";
    else if(h>=.45)say="Serious. On a quiet day this story would move the country's score on its own.";
    else if(h>=.2)say="Real, but limited. It adds to the day without defining it.";
    else if(h>0)say="Barely registers. Lots of these still add up to very little.";
    else say="Nothing for the map to count.";
    note.textContent=say;
  }
  input.addEventListener("input",render);
  root.querySelectorAll(".examples button").forEach(function(b){b.addEventListener("click",function(){input.value=b.dataset.h||b.textContent;render();input.focus();});});
  render();
})();
