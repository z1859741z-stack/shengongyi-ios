/* ============ 深宫弈·竖屏版新增：向导式建角 + 古风全身立绘 + 宫城示意图 ============
   画风标准（全部手绘 SVG，不用任何网图/版权图/生成图）：
   女：交领右衽汉服/宫装（襦裙·袄裙·宫装·披风四款），发髻（高髻/双鬟/垂鬟/盘发/散发）
       +簪钗步摇花钿，柳叶眉、凤眼（细长小眼，绝不大眼萌系）、樱桃口、长裙曳地不见鞋。
   男：束发+玉冠/金冠/乌纱，交领长袍/蟒袍/铠甲，腰封玉佩，持扇/剑/书卷/拂尘/笏板。
   全部汉族服饰，不混其他民族与现代元素。原 portraitSVG 的小眼+发髻+交领已合规，沿用其配色体系。 */
var sgQ = 0;
function sgHash(s){var h=0;s=String(s||"");for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;return h;}
function sgMotif(pattern,x,y,c){
  if(pattern==="mei"){var s="";for(var k=0;k<5;k++){var a=k/5*6.283;s+='<circle cx="'+(x+Math.cos(a)*5).toFixed(1)+'" cy="'+(y+Math.sin(a)*5).toFixed(1)+'" r="3" fill="'+c+'"/>';}return s+'<circle cx="'+x+'" cy="'+y+'" r="2.4" fill="#c0452f"/>';}
  if(pattern==="mudan")return '<circle cx="'+x+'" cy="'+y+'" r="7" fill="'+c+'" opacity=".8"/><circle cx="'+x+'" cy="'+y+'" r="4" fill="#fdf6e3" opacity=".7"/><circle cx="'+x+'" cy="'+y+'" r="2" fill="#c0452f"/>';
  if(pattern==="yun")return '<path d="M'+x+' '+y+' q9 -9 13 0 q4 9 -5 11 q-9 2 -9 -7" stroke="'+c+'" stroke-width="2" fill="none"/>';
  return '<path d="M'+x+' '+y+' L'+(x-7)+' '+(y-9)+' M'+x+' '+y+' L'+x+' '+(y-11)+' M'+x+' '+y+' L'+(x+7)+' '+(y-9)+'" stroke="'+c+'" stroke-width="1.8" fill="none" stroke-linecap="round"/>';
}
var SG_STYLE={
  "lindu":{prop:"medicine",crown:"yuguan"},
  "jiangzhe":{prop:"sword",crown:"shudai"},
  "xieyuan":{prop:"scroll",crown:"yuguan"},
  "rongzhi":{prop:"whisk",crown:"yuguan"},
  "xiaoyun":{prop:"sword",crown:"shudai"},
  "shangguan":{prop:"fan",crown:"wusha"},
  "emperor:wenrou":{prop:"jade",crown:"jinguan"},
  "emperor:fuhei":{prop:"fan",crown:"jinguan"},
  "emperor:fengliu":{prop:"fan",crown:"jinguan"},
  "emperor:lengmo":{prop:"jade",crown:"jinguan"},
  "emperor:gangzheng":{prop:"hu",crown:"jinguan"},
  "player:gaomen":{dress:"gong",hairF:"gaoji",pattern:"mudan"},
  "player:jiangmen":{dress:"cloak",hairF:"gaoji",pattern:"yun"},
  "player:pingmin":{dress:"ruqun",hairF:"chuihuan",pattern:"mei"},
  "player:fushang":{dress:"aoqun",hairF:"panfa",pattern:"mudan"},
  "player:jianghu":{dress:"cloak",hairF:"shuanghuan",pattern:"zhu"},
  "player:taiyi":{dress:"ruqun",hairF:"panfa",pattern:"mei"},
  "player:gongnv":{dress:"gong",hairF:"shuanghuan",pattern:"yun"},
  "player:heqin":{dress:"gong",hairF:"gaoji",pattern:"mudan"},
  "dowager":{dress:"gong",hairF:"panfa",pattern:"yun"},
  "maid":{dress:"ruqun",hairF:"shuanghuan",pattern:"mei"},
  "cold":{dress:"ruqun",hairF:"loose",pattern:"zhu"},
  "momo":{dress:"aoqun",hairF:"panfa",pattern:"yun"}
};
function sgBodySVG(p,key){
  if(!p)p={g:"f",robe:"#8a6d3b",trim:"#e6c87a",hair:"#2a1a10",skin:"#f8dfc4",jewel:"#c9a44a",mark:"宫",bg:"#f3dfba"};
  var h=sgHash(key||(p.mark+"|"+p.robe));
  var st=SG_STYLE[key]||{};
  var gid="sg"+(++sgQ);
  var s='<svg viewBox="0 0 200 340" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="古风人物立绘">';
  s+='<defs><linearGradient id="'+gid+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+p.robe+'"/><stop offset="1" stop-color="'+p.robe+'" stop-opacity=".7"/></linearGradient></defs>';
  s+='<rect x="0" y="0" width="200" height="340" fill="'+(p.bg||"#f3dfba")+'"/>';
  s+='<circle cx="100" cy="170" r="92" fill="#ffffff" opacity=".25"/>';
  s+='<circle cx="30" cy="40" r="12" fill="'+p.trim+'" opacity=".3"/><circle cx="172" cy="300" r="10" fill="'+p.trim+'" opacity=".3"/>';
  var isF=(p.g==="f");
  /* ---- 衣袍底 ---- */
  s+='<path d="M100 104 C62 114 42 168 36 340 L164 340 C158 168 138 114 100 104 Z" fill="url(#'+gid+')"/>';
  if(isF){
    var dress=st.dress||["ruqun","aoqun","gong","cloak"][h%4];
    if(dress==="ruqun"){
      s+='<path d="M64 108 L136 108 L132 192 L68 192 Z" fill="'+p.trim+'" opacity=".85"/>';
      s+='<path d="M64 108 L100 150 L136 108 L136 118 L100 160 L64 118 Z" fill="'+p.robe+'"/>';
      s+='<path d="M64 122 C48 142 42 176 42 206 L60 209 C62 176 68 148 78 130 Z" fill="url(#'+gid+')"/>';
      s+='<path d="M136 122 C152 142 158 176 158 206 L140 209 C138 176 132 148 122 130 Z" fill="url(#'+gid+')"/>';
    }else if(dress==="aoqun"){
      s+='<path d="M62 106 C58 140 60 170 66 194 L134 194 C140 170 142 140 138 106 Z" fill="'+p.robe+'" stroke="'+p.trim+'" stroke-width="1.5"/>';
      s+='<circle cx="100" cy="130" r="3" fill="'+p.trim+'"/><circle cx="100" cy="152" r="3" fill="'+p.trim+'"/><circle cx="100" cy="174" r="3" fill="'+p.trim+'"/>';
      s+='<path d="M66 194 L134 194 L164 340 L36 340 Z" fill="url(#'+gid+')"/>';
    }else if(dress==="cloak"){
      s+='<path d="M100 96 C48 106 28 170 24 330 L46 330 C52 200 66 140 92 110 Z" fill="'+p.trim+'" opacity=".9"/>';
      s+='<path d="M100 96 C152 106 172 170 176 330 L154 330 C148 200 134 140 108 110 Z" fill="'+p.trim+'" opacity=".9"/>';
      s+='<circle cx="100" cy="110" r="6" fill="'+(p.jewel||"#c0452f")+'" stroke="'+p.trim+'" stroke-width="2"/>';
    }else{
      s+='<path d="M62 116 C38 140 28 192 26 238 L52 242 C56 200 64 160 78 132 Z" fill="url(#'+gid+')"/>';
      s+='<path d="M138 116 C162 140 172 192 174 238 L148 242 C144 200 136 160 122 132 Z" fill="url(#'+gid+')"/>';
    }
    /* 交领 + 腰封 + 纹样 */
    s+='<path d="M78 108 L100 152 L122 108 L132 118 L100 172 L68 118 Z" fill="'+p.trim+'"/>';
    s+='<path d="M88 112 L100 136 L112 112 L100 124 Z" fill="#fdf6e3"/>';
    s+='<rect x="70" y="184" width="60" height="12" rx="6" fill="'+p.trim+'"/>';
    s+='<circle cx="100" cy="190" r="7" fill="'+(p.jewel||"#c0452f")+'"/>';
    s+='<path d="M96 196 L92 224 M104 196 L108 224" stroke="'+p.trim+'" stroke-width="2.5"/>';
    var pat=st.pattern||["mei","mudan","yun","zhu"][(h>>4)%4];
    s+=sgMotif(pat,76,258,p.trim)+sgMotif(pat,126,282,p.trim)+sgMotif(pat,100,312,p.trim);
    s+='<path d="M52 200 L48 330 M148 200 L152 330" stroke="#2e2118" stroke-width="1" opacity=".12"/>';
  }else{
    /* 男：直身长袍 + 腰封玉佩 */
    s+='<path d="M78 108 L100 150 L122 108 L132 118 L100 170 L68 118 Z" fill="'+p.trim+'"/>';
    s+='<rect x="72" y="182" width="56" height="12" rx="6" fill="'+p.trim+'"/>';
    s+='<rect x="94" y="196" width="12" height="20" rx="4" fill="'+(p.jewel||"#c9a44a")+'" stroke="#2e2118" stroke-opacity=".2"/>';
    s+='<path d="M100 216 L97 238 M100 216 L103 238" stroke="'+(p.jewel||"#c9a44a")+'" stroke-width="2"/>';
    if(p.armor){
      s+='<circle cx="56" cy="128" r="14" fill="'+p.trim+'"/><circle cx="144" cy="128" r="14" fill="'+p.trim+'"/>';
      s+='<path d="M70 130 L130 130 M74 150 L126 150" stroke="#2e2118" stroke-width="1.6" opacity=".3"/>';
    }
    s+='<path d="M62 116 C40 140 32 192 30 236 L54 240 C58 200 66 160 80 132 Z" fill="url(#'+gid+')"/>';
    s+='<path d="M138 116 C160 140 168 192 170 236 L146 240 C142 200 134 160 120 132 Z" fill="url(#'+gid+')"/>';
    var patM=["yun","zhu","mei","mudan"][(h>>4)%4];
    s+=sgMotif(patM,100,268,p.trim);
  }
  /* ---- 脖子与脸（统一古风：细眉凤眼小口） ---- */
  s+='<rect x="92" y="88" width="16" height="22" rx="6" fill="'+p.skin+'"/>';
  s+='<circle cx="74" cy="64" r="5" fill="'+p.skin+'"/><circle cx="126" cy="64" r="5" fill="'+p.skin+'"/>';
  s+='<ellipse cx="100" cy="62" rx="26" ry="32" fill="'+p.skin+'"/>';
  if(isF){
    s+='<path d="M76 54 Q83 49 90 54" stroke="#3a2413" stroke-width="2" fill="none" stroke-linecap="round"/>';
    s+='<path d="M110 54 Q117 49 124 54" stroke="#3a2413" stroke-width="2" fill="none" stroke-linecap="round"/>';
    s+='<path d="M75 65 Q82 60 89 65 Q82 68 75 65Z" fill="#2b1c10"/>';
    s+='<path d="M111 65 Q118 60 125 65 Q118 68 111 65Z" fill="#2b1c10"/>';
    s+='<path d="M100 70 L98 78 Q100 80 102 78" stroke="#c99b78" stroke-width="1.6" fill="none" stroke-linecap="round"/>';
    s+='<circle cx="78" cy="79" r="5" fill="#e89a8a" opacity=".4"/><circle cx="122" cy="79" r="5" fill="#e89a8a" opacity=".4"/>';
    s+='<ellipse cx="100" cy="88" rx="5.5" ry="2.8" fill="#b03a2e"/>';
    s+='<circle cx="100" cy="42" r="2.2" fill="'+(p.jewel||"#c0452f")+'"/>';
  }else{
    var browY=p.stern?52:54;
    s+='<path d="M76 '+browY+' L90 '+(browY-1)+'" stroke="#3a2413" stroke-width="3" fill="none" stroke-linecap="round"/>';
    s+='<path d="M110 '+(browY-1)+' L124 '+browY+'" stroke="#3a2413" stroke-width="3" fill="none" stroke-linecap="round"/>';
    s+='<path d="M76 63 Q82 60 88 63 Q82 66 76 63Z" fill="#2b1c10"/>';
    s+='<path d="M112 63 Q118 60 124 63 Q118 66 112 63Z" fill="#2b1c10"/>';
    s+='<path d="M100 68 L98 77 Q100 79 102 77" stroke="#c99b78" stroke-width="1.6" fill="none" stroke-linecap="round"/>';
    s+='<ellipse cx="100" cy="87" rx="5" ry="2" fill="#9a6a55"/>';
  }
  if(p.elder)s+='<path d="M80 52 Q100 48 120 52" stroke="#8a6a4a" stroke-width="1.2" fill="none" opacity=".4"/>';
  /* ---- 发型发饰 ---- */
  if(isF){
    var hairF=st.hairF||["gaoji","shuanghuan","chuihuan","panfa"][(h>>2)%4];
    if(p.loose)hairF="loose";
    s+='<path d="M70 66 C64 22 82 8 100 8 C118 8 136 22 130 66 C124 44 114 38 100 38 C86 38 76 44 70 66 Z" fill="'+p.hair+'"/>';
    if(hairF==="gaoji"){
      s+='<circle cx="100" cy="12" r="12" fill="'+p.hair+'"/>';
      s+='<line x1="106" y1="8" x2="130" y2="2" stroke="'+p.trim+'" stroke-width="3" stroke-linecap="round"/>';
      s+='<circle cx="132" cy="2" r="4" fill="'+(p.jewel||"#c0452f")+'"/><circle cx="122" cy="8" r="3" fill="'+(p.jewel||"#c0452f")+'" opacity=".85"/>';
      s+='<line x1="130" y1="5" x2="130" y2="16" stroke="'+p.trim+'" stroke-width="1.6"/><circle cx="130" cy="19" r="2.4" fill="'+p.trim+'"/>';
    }else if(hairF==="shuanghuan"){
      s+='<circle cx="64" cy="30" r="10" fill="'+p.hair+'"/><circle cx="136" cy="30" r="10" fill="'+p.hair+'"/>';
      s+='<circle cx="64" cy="30" r="3" fill="'+p.trim+'"/><circle cx="136" cy="30" r="3" fill="'+p.trim+'"/>';
      s+='<circle cx="70" cy="22" r="2" fill="'+(p.jewel||"#c0452f")+'"/><circle cx="130" cy="22" r="2" fill="'+(p.jewel||"#c0452f")+'"/>';
    }else if(hairF==="chuihuan"){
      s+='<circle cx="68" cy="58" r="8" fill="'+p.hair+'"/><circle cx="132" cy="58" r="8" fill="'+p.hair+'"/>';
      s+='<path d="M68 62 C64 84 66 100 70 112 L77 108 C73 92 72 76 73 64 Z" fill="'+p.hair+'"/>';
      s+='<path d="M132 62 C136 84 134 100 130 112 L123 108 C127 92 128 76 127 64 Z" fill="'+p.hair+'"/>';
    }else if(hairF==="panfa"){
      s+='<ellipse cx="100" cy="12" rx="20" ry="8" fill="'+p.hair+'"/>';
      s+='<line x1="108" y1="10" x2="132" y2="4" stroke="'+p.trim+'" stroke-width="3" stroke-linecap="round"/>';
      s+='<circle cx="134" cy="4" r="3.4" fill="'+(p.jewel||"#c0452f")+'"/>';
      s+='<line x1="128" y1="8" x2="128" y2="15" stroke="'+p.trim+'" stroke-width="1.4"/><circle cx="128" cy="18" r="2.2" fill="'+p.trim+'"/>';
    }else{
      s+='<path d="M70 60 C62 96 62 130 68 152 L80 148 C74 118 74 88 76 62 Z" fill="'+p.hair+'"/>';
      s+='<path d="M130 60 C138 96 138 130 132 152 L120 148 C126 118 126 88 124 62 Z" fill="'+p.hair+'"/>';
    }
    s+='<circle cx="74" cy="86" r="2.5" fill="'+p.trim+'"/><circle cx="126" cy="86" r="2.5" fill="'+p.trim+'"/>';
  }else{
    s+='<path d="M72 64 C70 26 84 14 100 14 C116 14 130 26 128 64 C122 44 112 40 100 40 C88 40 78 44 72 64 Z" fill="'+p.hair+'"/>';
    s+='<circle cx="100" cy="12" r="9" fill="'+p.hair+'"/>';
    var crown=st.crown||["yuguan","jinguan","wusha"][(h>>2)%3];
    if(p.crown)crown="jinguan";
    if(crown==="jinguan"){
      s+='<rect x="82" y="0" width="36" height="10" rx="3" fill="'+p.trim+'"/>';
      s+='<circle cx="88" cy="14" r="2.4" fill="'+p.trim+'"/><circle cx="100" cy="14" r="2.4" fill="'+p.trim+'"/><circle cx="112" cy="14" r="2.4" fill="'+p.trim+'"/>';
    }else if(crown==="wusha"){
      s+='<rect x="80" y="4" width="40" height="10" rx="4" fill="#2e2a33"/>';
      s+='<path d="M80 8 L50 0 L54 12 L80 12 Z" fill="#2e2a33"/><path d="M120 8 L150 0 L146 12 L120 12 Z" fill="#2e2a33"/>';
    }else{
      s+='<path d="M84 14 Q100 2 116 14 L116 20 L84 20 Z" fill="'+p.trim+'"/>';
      s+='<circle cx="100" cy="10" r="2.6" fill="'+(p.jewel||"#c9a44a")+'"/>';
    }
    /* 手持物 */
    var prop=st.prop||"jade";
    s+='<circle cx="160" cy="202" r="6" fill="'+p.skin+'"/>';
    if(prop==="fan")s+='<path d="M152 210 Q168 186 180 212 Q166 224 152 210 Z" fill="#fdf6e3" stroke="'+p.trim+'" stroke-width="1.5"/><path d="M160 208 L156 218 M166 204 L166 216 M172 206 L174 216" stroke="'+p.trim+'" stroke-width="1.2"/>';
    else if(prop==="sword")s+='<rect x="163" y="180" width="6" height="72" rx="2" fill="#cfd6dd" stroke="#5d4630"/><rect x="155" y="176" width="22" height="6" rx="3" fill="'+p.trim+'"/><circle cx="166" cy="256" r="4" fill="'+p.trim+'"/>';
    else if(prop==="scroll")s+='<rect x="148" y="198" width="36" height="13" rx="6" fill="#f6ecd4" stroke="'+p.trim+'"/><circle cx="150" cy="204" r="6" fill="'+p.trim+'"/><circle cx="182" cy="204" r="6" fill="'+p.trim+'"/>';
    else if(prop==="whisk")s+='<line x1="166" y1="182" x2="166" y2="228" stroke="#5d4630" stroke-width="3"/><path d="M166 228 Q150 250 146 268 M166 228 Q166 252 166 270 M166 228 Q182 250 186 268" stroke="#e8e2d2" stroke-width="3" fill="none" stroke-linecap="round"/>';
    else if(prop==="hu")s+='<path d="M158 186 L174 186 L170 246 L162 246 Z" fill="'+p.trim+'" stroke="#2e2118" stroke-opacity=".2"/>';
    else if(prop==="medicine")s+='<circle cx="166" cy="216" r="12" fill="#3f6f5a"/><path d="M166 204 L166 196" stroke="#3f6f5a" stroke-width="2.5"/><circle cx="166" cy="216" r="5" fill="#e6c87a"/>';
  }
  s+="</svg>";
  return s;
}
function sgResolveKey(p){
  var m=p.mark||"";
  var leadByMark={"医":"lindu","卫":"jiangzhe","书":"xieyuan","星":"rongzhi","将":"xiaoyun","辅":"shangguan"};
  if(m==="主"){
    var idn="gaomen";try{var r=document.querySelector('input[name="identity"]:checked');if(r)idn=r.value;}catch(e){}
    if(window.G&&G.identity)idn=G.identity.id;
    return "player:"+idn;
  }
  if(m==="龙")return "emperor:"+((window.G&&G.emperor)?G.emperor.pers:"wenrou");
  if(leadByMark[m])return leadByMark[m];
  if(m==="慈")return "dowager";
  if(m==="鸾")return "maid";
  if(m==="福")return "eunuch";
  if(m==="林")return "cold";
  if(m==="厨"||m==="乐")return "momo";
  return m+"|"+p.robe;
}
function sgPortrait(p,mode){
  if(mode==="full")return sgBodySVG(p,sgResolveKey(p));
  return portraitSVG(p,mode);
}
/* 对话立绘改全身：覆盖原 updateDlgPortrait（逻辑照抄，只换立绘） */
updateDlgPortrait=function(){
  if(!DLG)return;
  var ln=DLG.lines[DLG.idx],who=null;
  if(ln.side==="me")who=G.name;
  else if(ln.side==="them")who=ln.who;
  else{for(var i=DLG.idx;i>=0;i--){if(DLG.lines[i].side==="them"){who=DLG.lines[i].who;break;}}}
  if(!who)who=G.name;
  $("dlgPortrait").innerHTML=sgPortrait(profForSpeaker(who),"full");
  $("dlgPortrait").classList.toggle("speaking",ln.side!=="narr");
  $("dlgSpeaker").innerHTML=esc(who)+(speakerRole(who)?'<span class="role">'+esc(speakerRole(who))+"</span>":"");
  $("dlgAutoTag").classList.toggle("show",!!DLG.auto);
};
/* ============ 向导式建角：一步一页（5 步） ============ */
(function(){
  var cards=[document.getElementById("sgStep1"),document.getElementById("sgStep2"),
    document.getElementById("sgStep3"),document.getElementById("sgStep4"),document.getElementById("sgStep5")];
  if(!cards[0]||!cards[4])return;
  var cur=0;
  var bar=document.getElementById("sgStepBar");
  var prev=document.getElementById("sgPrevBtn"),next=document.getElementById("sgNextBtn");
  var startbar=document.querySelector(".startbar");
  function fillSummary(){
    var name=($("pName").value||"").trim()||"沈知意";
    var pAge=clamp(parseInt($("pAge").value)||17,14,40);
    var idn=document.querySelector('input[name="identity"]:checked').value;
    var it=IDENTITIES.filter(function(x){return x.id===idn;})[0];
    var eName=($("eName").value||"").trim()||"萧景珩";
    var eAge=clamp(parseInt($("eAge").value)||24,16,50);
    var pers=document.querySelector('input[name="pers"]:checked').value;
    var pn=PERSONALITIES.filter(function(p){return p.id===pers;})[0];
    var stats=readStats("attr",ATTRS),talents=readStats("talent",TALENTS);
    var op=calcOpening(it,stats,talents,pers);
    var statLine=ATTRS.map(function(a){return a[1]+stats[a[0]];}).join(" · ");
    var talLine=TALENTS.map(function(a){return a[1]+talents[a[0]];}).join(" · ");
    $("sgSummary").innerHTML=
      '<div class="sg-sum-portrait">'+sgPortrait(profPlayer(),"full")+'</div>'
      +'<div class="sg-sum-rows">'
      +'<div><b>你　</b>'+esc(name)+' · '+pAge+'岁 · '+it.name+'（'+it.trait+'）</div>'
      +'<div><b>六维</b>'+statLine+'</div>'
      +'<div><b>才艺</b>'+talLine+'</div>'
      +'<div><b>皇帝</b>'+esc(eName)+' · '+eAge+'岁 · '+pn.name+'（偏爱'+persPrefText(pers)+'）</div>'
      +'<div><b>选秀预测</b>表现分 '+op.selScore+' · 开局宠爱 '+op.favor+'（'+favorTier(op.favor)+'）· 初封'+op.rankName+(op.steps>0?'（连升'+op.steps+'位）':'')+'</div>'
      +'</div>';
  }
  function showStep(n){
    cur=Math.max(0,Math.min(4,n));
    cards.forEach(function(c,i){if(c)c.classList.toggle("sg-on",i===cur);});
    if(startbar)startbar.classList.toggle("sg-on",cur===4);
    var dots=bar.querySelectorAll(".sg-dot");
    dots.forEach(function(d,i){d.classList.toggle("on",i===cur);d.classList.toggle("done",i<cur);});
    document.getElementById("sgStepNum").textContent=(cur+1)+"/5";
    prev.disabled=(cur===0);
    next.style.display=(cur===4?"none":"");
    if(cur===4)fillSummary();
    window.scrollTo({top:0,behavior:"smooth"});
  }
  prev.addEventListener("click",function(){showStep(cur-1);});
  next.addEventListener("click",function(){showStep(cur+1);});
  bar.querySelectorAll(".sg-dot").forEach(function(d,i){
    d.addEventListener("click",function(){if(i<=cur)showStep(i);});
  });
  /* 继续上局那行提到步骤条下面，第 1 页就能看见 */
  var cb=document.getElementById("sgContinueBtn");
  if(cb&&cb.parentNode){var row=cb.parentNode;row.style.marginTop="10px";bar.parentNode.insertBefore(row,bar.nextSibling);}
  showStep(0);
})();
/* ============ 宫城示意图（手绘 SVG，可点前往） ============ */
var SG_MAP_NODES=[
  ["garden","御花园",200,72],["guoshi","钦天监",330,80],["cold","冷宫",60,88],
  ["cining","慈宁宫",72,205],["library","藏书阁",328,205],
  ["yangxin","养心殿",72,325],["self","我的寝宫",328,325],["banquet","交泰殿",200,300],
  ["music","乐坊",328,425],["kitchen","尚食局",72,430],["visits","嫔妃宫所",200,440],
  ["martial","演武场",330,505],["taiyi","太医院",70,505],["court","前朝大门",200,568]
];
function sgPalaceMapSVG(){
  var halls=[[200,190,"坤宁宫"],[200,360,"乾清宫"],[200,522,"太和殿"]];
  var hallSVG=halls.map(function(h){
    return '<g><path d="M'+(h[0]-34)+' '+(h[1]+6)+' L'+h[0]+' '+(h[1]-12)+' L'+(h[0]+34)+' '+(h[1]+6)+' Z" fill="#9c2b23" stroke="#c9a44a" stroke-width="1.5"/>'
      +'<rect x="'+(h[0]-24)+'" y="'+(h[1]+6)+'" width="48" height="10" fill="#e6c87a" stroke="#a87e2c"/>'
      +'<text x="'+h[0]+'" y="'+(h[1]+30)+'" text-anchor="middle" font-size="10.5" fill="#6d5a43">'+h[2]+'</text></g>';
  }).join("");
  var nodes=SG_MAP_NODES.map(function(nd){
    var id=nd[0],label=nd[1],x=nd[2],y=nd[3];
    var ppl=(typeof peopleAt==="function"&&window.G)?peopleAt(id):[];
    var on=(window.G&&G.loc===id);
    return '<g class="sg-map-node'+(on?" on":"")+'" data-act="loc" data-arg="'+id+'">'
      +'<circle cx="'+x+'" cy="'+y+'" r="17" fill="'+(on?"#9c2b23":"#fbf5e6")+'" stroke="#c9a44a" stroke-width="2"/>'
      +'<text x="'+x+'" y="'+(y+4)+'" text-anchor="middle" font-size="11" font-weight="700" fill="'+(on?"#fdf3da":"#2e2118")+'">'+label.charAt(0)+'</text>'
      +'<text x="'+x+'" y="'+(y+31)+'" text-anchor="middle" font-size="11.5" font-weight="700" fill="#fdf3da" stroke="#241a05" stroke-width="3" paint-order="stroke">'+label+'</text>'
      +(ppl.length?'<circle cx="'+(x+14)+'" cy="'+(y-14)+'" r="6" fill="#c9a44a" stroke="#fdf3da" stroke-width="1"/><text x="'+(x+14)+'" y="'+(y-11)+'" text-anchor="middle" font-size="9" font-weight="900" fill="#241a05">'+ppl.length+'</text>':"")
      +'</g>';
  }).join("");
  return '<svg viewBox="0 0 400 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="宫城示意图">'
    +'<rect x="0" y="0" width="400" height="620" fill="#efe3c6"/>'
    +'<rect x="6" y="6" width="388" height="608" fill="none" stroke="#7c8a9a" stroke-width="5" opacity=".55"/>'
    +'<rect x="16" y="16" width="368" height="588" fill="#f6ecd4" stroke="#7c1f18" stroke-width="4"/>'
    +'<rect x="30" y="30" width="340" height="560" fill="none" stroke="#a87e2c" stroke-width="1.5"/>'
    +'<line x1="200" y1="30" x2="200" y2="590" stroke="#c9a44a" stroke-width="1.5" stroke-dasharray="6 5" opacity=".7"/>'
    +'<circle cx="150" cy="62" r="13" fill="#3f6f5a"/><circle cx="185" cy="52" r="16" fill="#54687e"/><circle cx="222" cy="60" r="12" fill="#3f6f5a"/><circle cx="252" cy="66" r="9" fill="#54687e"/>'
    +'<text x="200" y="46" text-anchor="middle" font-size="10.5" fill="#3f6f5a">御花园 · 树</text>'
    +hallSVG+nodes+'</svg>';
}
function sgRenderPalaceMap(){
  if(!window.G)return;
  var host=document.getElementById("sgPalaceMap");
  if(!host){
    var map=document.getElementById("tab-map");if(!map)return;
    host=document.createElement("div");
    host.id="sgPalaceMap";
    host.innerHTML='<div class="sg-map-cap">宫城示意图（手绘）· 点宫殿前往 · 金点数字表示此刻有人</div><div class="sg-map-svg"></div>';
    var sc=document.getElementById("scenicMap");
    map.insertBefore(host,sc);
  }
  host.querySelector(".sg-map-svg").innerHTML=sgPalaceMapSVG();
}
var _sgRenderMap=renderMap;
renderMap=function(){_sgRenderMap();sgRenderPalaceMap();};
