#!/usr/bin/env python3
"""深宫弈 竖屏沉浸大改版：去重+压缩图片、去 Google Fonts、竖屏重排、
少文字折叠、视觉小说式对话、Ken Burns 场景、localStorage 存档。
只改表现层，不改游戏数值/剧情逻辑。输入原 upload.html，输出优化版 index.html。"""
import base64, hashlib, io, re, sys
from pathlib import Path
from PIL import Image

SRC = Path.home() / "workspace/user/files/upload.html"
OUT = Path.home() / "workspace/shengongyi-ios/Shengongyi/index.html"
OUT_WEB = Path.home() / "workspace/shengongyi-deploy/index.html"

t = SRC.read_text(encoding="utf-8")
orig_bytes = SRC.stat().st_size
print(f"original: {orig_bytes/1e6:.2f} MB, {t.count(chr(10))+1} lines")

# ---------- 1. 图片去重 + 压缩 ----------
pat = re.compile(r'"data:image/jpeg;base64,([A-Za-z0-9+/=]+)"')
matches = list(pat.finditer(t))
print(f"image refs: {len(matches)}")
hash_to_var = {}
var_to_b64 = {}
order = []
for m in matches:
    b64 = m.group(1)
    h = hashlib.sha256(b64.encode()).hexdigest()[:8]
    if h not in hash_to_var:
        var = f"IMG_{chr(65+len(order))}"  # IMG_A, IMG_B, ...
        hash_to_var[h] = var
        order.append(h)
        # 解码、缩放到宽 1200、JPEG q72 重编码
        raw = base64.b64decode(b64)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        print(f"  {var} hash={h} orig={im.size} bytes~{len(raw)} count={sum(1 for x in matches if hashlib.sha256(x.group(1).encode()).hexdigest()[:8]==h)}")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=72, optimize=True)
        new_b64 = base64.b64encode(buf.getvalue()).decode()
        var_to_b64[var] = new_b64
        print(f"      -> {im.size} bytes~{len(buf.getvalue())} b64len={len(new_b64)}")

# 替换：从后往前，避免偏移错乱。第 0 处在 renderScenic 单引号字符串里，用 '+IMG_X+' 拼接；其余用裸变量。
def var_for(m):
    h = hashlib.sha256(m.group(1).encode()).hexdigest()[:8]
    return hash_to_var[h]

# 先按位置记录每处的替换文本
replacements = []
for idx, m in enumerate(matches):
    v = var_for(m)
    if idx == 0:
        repl = f"'+{v}+'"
    else:
        repl = v
    replacements.append((m.start(), m.end(), repl))

new_t = t
for s, e, repl in reversed(replacements):
    new_t = new_t[:s] + repl + new_t[e:]
assert "data:image/jpeg;base64," not in new_t, "仍有未替换的图片！"
print(f"unique images kept: {len(order)} -> {list(var_to_b64)}")

# 在第一个 <script> 里定义 IMG 常量（紧跟 "use strict";）
const_block = "\n/* ---- 优化：实景图去重，只留 4 张（原 16 处引用同一批图） ---- */\n" + "\n".join(
    f'var {v}="data:image/jpeg;base64,{b}";' for v, b in var_to_b64.items()
) + "\n"
# 第一个 script 标签后的 "use strict"; 位置
m0 = re.search(r'<script>\s*"use strict";', new_t)
assert m0, "找不到第一个 script"
new_t = new_t[:m0.end()] + const_block + new_t[m0.end():]

# ---------- 2. 去 Google Fonts，改系统字体 ----------
new_t = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com" />', "", new_t)
new_t = re.sub(r'\s*<link href="https://fonts\.googleapis\.com[^>]*>', "", new_t)
assert "fonts.googleapis" not in new_t
new_t = new_t.replace('"Noto Serif SC","Songti SC","STSong",serif',
                      '"Songti SC","STSong","Noto Serif SC",serif')
new_t = new_t.replace('"Ma Shan Zheng","Noto Serif SC",serif',
                      '"Kaiti SC","STKaiti","Songti SC",serif')
new_t = new_t.replace('font-family:"Ma Shan Zheng","Noto Serif SC",serif',
                      'font-family:"Kaiti SC","STKaiti","Songti SC",serif')

# ---------- 2.5 向导式建角：一步一页（HTML 重组） + 全身立绘调用点 ----------
# 只动开局页（setupView 到游戏主界面注释之间）：4 张卡依次编号 sgStep1-4，
# 步骤条插在 hero 之后，第 5 页确认卡（含选秀入宫按钮）插在 startbar 之前，
# 底部上一步/下一步导航插在 setupView 末尾。原四卡堆叠排版不再保留。
_marker = "<!-- ================= 游戏主界面 ================= -->"
_si = new_t.find(_marker)
assert _si > 0
_setup, _rest = new_t[:_si], new_t[_si:]
# 步骤条
_stepbar = ('<div id="sgStepBar">'
  '<span class="sg-dot on">1 · 定你</span><span class="sg-dot">2 · 属性</span>'
  '<span class="sg-dot">3 · 才艺</span><span class="sg-dot">4 · 皇帝</span>'
  '<span class="sg-dot">5 · 确认</span><span id="sgStepNum">1/5</span></div>')
_setup = _setup.replace('\n\n  <div class="card">', '\n\n  ' + _stepbar + '\n\n  <div class="card">', 1)
assert 'id="sgStepBar"' in _setup
# 4 张卡编号
_card_ids = ["sgStep1", "sgStep2", "sgStep3", "sgStep4"]
_n = [0]
def _tag_card(m):
    _n[0] += 1
    return '<div class="card" id="%s">' % _card_ids[_n[0] - 1]
_setup = re.sub(r'<div class="card">', _tag_card, _setup, count=4)
assert _n[0] == 4, f"开局卡只找到 {_n[0]} 张"
# 第 5 页确认卡：把选秀入宫按钮从 startbar 移进来
_startbtn = '<button class="btn primary" id="startBtn">选秀入宫</button>'
assert _startbtn in _setup
_setup = _setup.replace(_startbtn, "", 1)
_summary = ('<div class="card" id="sgStep5"><h2>五 · 确认总览</h2>'
  '<div class="desc">核对一遍，没问题就选秀入宫。</div><div id="sgSummary"></div>'
  '<div style="text-align:center;margin-top:14px">' + _startbtn + '</div></div>')
_setup = _setup.replace('  <div class="startbar">', '  ' + _summary + '\n  <div class="startbar">', 1)
assert 'id="sgStep5"' in _setup
# 底部导航：插在 setupView 闭合 </div> 之前
_nav = ('<div id="sgWizardNav"><button class="btn" id="sgPrevBtn">← 上一步</button>'
  '<button class="btn primary" id="sgNextBtn">下一步 →</button></div>')
_s = _setup.rstrip()
assert _s.endswith("</div>")
_setup = _s[:-len("</div>")] + _nav + "\n</div>\n"
new_t = _setup + _rest
# 全身立绘调用点：嫔妃卡、攻略卡、对话立绘改走 sgPortrait(..., "full")；地图小像仍用 face
for _old, _new in [
    ('portraitSVG(profForNpc(i,n.name),"bust")', 'sgPortrait(profForNpc(i,n.name),"full")'),
    ('portraitSVG(profForLead(l.id),"bust")', 'sgPortrait(profForLead(l.id),"full")'),
    ('$("dlgPortrait").innerHTML=portraitSVG(profForSpeaker(who),"bust");',
     '$("dlgPortrait").innerHTML=sgPortrait(profForSpeaker(who),"full");'),
]:
    assert new_t.count(_old) == 1, f"调用点不唯一/缺失: {_old[:40]} x{new_t.count(_old)}"
    new_t = new_t.replace(_old, _new)
print("wizard: 5 步向导已重组，全身立绘调用点已替换 3 处")

# ---------- 3. 竖屏沉浸 CSS（追加一个 style 块，覆盖原样式） ----------
css = """
/* ============ 深宫弈·竖屏沉浸版覆盖样式（只改表现，不改逻辑） ============ */
:root{--sg-w:430px}
html,body{overflow-x:hidden}
body{background:linear-gradient(180deg,#241809,#171008)}
.wrap,.statusbar .in,.tabs,.pane{max-width:var(--sg-w)}
.wrap{padding:12px 12px 120px}
.hero{padding:22px 6px 4px}
.hero .big{font-size:clamp(48px,15vw,72px)}
.card{padding:16px 14px;margin:14px 0}
/* 状态栏：只留关键数，横向滚动不挤 */
.statusbar .in{flex-wrap:nowrap;overflow-x:auto;gap:6px 10px;padding:8px 12px;scrollbar-width:none}
.statusbar .in::-webkit-scrollbar{display:none}
.statusbar .who{font-size:17px;white-space:nowrap}
/* 导航：单行横滑，拇指区在底部更顺手；主按钮加高 */
.tabs{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;gap:6px}
.tabs::-webkit-scrollbar{display:none}
.tabs button{flex:none;padding:10px 14px;min-height:44px}
.btn{min-height:46px}
.startbar .btn{width:100%;padding:15px 0;font-size:19px}
.pane .sheet{padding:14px 12px}
/* 场景图全屏底 + Ken Burns 缓慢缩放（不是真视频，省体积） */
.scenic{height:min(600px,72vh);min-height:420px}
.scenic img.venue{animation:sgKenBurns 30s ease-in-out infinite alternate}
.stage>img{height:430px;animation:sgKenBurns 30s ease-in-out infinite alternate}
.scenehero img{height:240px}
@keyframes sgKenBurns{from{transform:scale(1) translate(0,0)}to{transform:scale(1.13) translate(-1.2%,-1.5%)}}
/* 地图人物小像放大，走到哪儿一眼看见 */
.player-token .pt-ava{width:52px;height:52px;border-width:3px}
.player-token .pt-name{font-size:12.5px}
.pin{font-size:13px;padding:4px 11px}
/* 地点一览改两列大卡，点着方便 */
.mapgrid{grid-template-columns:repeat(2,1fr);gap:10px}
.loc{padding:16px 8px 12px}
/* 视觉小说式对话：大立绘在上，气泡在下，一句一句点 */
.dlgbox{max-width:var(--sg-w)}
.dlg-layout{grid-template-columns:1fr;gap:10px}
.dlg-side{position:static;display:flex;gap:12px;align-items:center;text-align:left}
.dlg-portrait{width:118px;flex:none;aspect-ratio:200/240}
.dlg-speaker{font-size:18px}
.dlglog{max-height:38vh}
.bubble{max-width:94%;font-size:16px;padding:11px 14px}
.dlgops .btn{min-height:48px;font-size:15.5px}
/* 舞台人物放大 */
.stage-char{width:104px}
.stage-char .sc-ava{width:86px;height:110px}
.stage-bubble{font-size:14.5px}
/* 少文字：长文默认只露两行/六行，点一下展开全文 */
#logList li{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
#logList li.sg-open{display:block}
.modal .mbody{display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
.modal .mbody.sg-open{display:block}
.card .desc,.loc span,.act span,.person .meta{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.person .meta{cursor:pointer}
.person .meta.sg-open,.card .desc.sg-open,.loc span.sg-open,.act span.sg-open{display:block}
/* 底部存档浮钮 */
#sgSaveFab{position:fixed;right:14px;bottom:calc(18px + env(safe-area-inset-bottom));z-index:70;
  display:none;align-items:center;justify-content:center;min-width:56px;min-height:56px;border-radius:50%;
  background:var(--red);color:#fdf3da;border:2px solid var(--gold2);font-size:15px;font-weight:900;
  box-shadow:0 6px 20px rgba(0,0,0,.4)}
@media (prefers-reduced-motion: reduce){
  .scenic img.venue,.stage>img{animation:none}
}
/* ---------- 向导式建角：一步一页 ---------- */
#setupView .card{display:none}
#setupView .card.sg-on{display:block}
#setupView .startbar{display:none}
#setupView .startbar.sg-on{display:block}
#sgStepBar{display:flex;align-items:flex-end;gap:4px;margin:12px 0 2px}
.sg-dot{flex:1;text-align:center;font-size:12px;font-weight:700;color:var(--ink2);
  border-bottom:3px solid var(--line);padding-bottom:6px;cursor:pointer;white-space:nowrap}
.sg-dot.on{color:var(--red);border-color:var(--red)}
.sg-dot.done{color:var(--jade);border-color:var(--jade)}
#sgStepNum{font-size:13px;font-weight:900;color:var(--gold);padding-bottom:6px;white-space:nowrap}
#sgWizardNav{position:sticky;bottom:calc(10px + env(safe-area-inset-bottom));display:flex;gap:8px;margin:16px 0 8px;z-index:30}
#sgWizardNav .btn{flex:1;min-height:54px;font-size:17px}
#sgStep1 .pickgrid,#sgStep4 .pickgrid{grid-template-columns:1fr 1fr;gap:8px}
#sgStep1 .pick .box,#sgStep4 .pick .box{padding:10px 10px 10px 38px;min-height:118px}
#sgStep1 .pick .box b,#sgStep4 .pick .box b{font-size:15px}
#sgStep1 .pick input,#sgStep4 .pick input{top:10px;left:10px}
#sgStep1 .pick .box span,#sgStep4 .pick .box span{font-size:12.5px}
.statrow .ctl input[type=range]{height:30px}
.sg-sum-portrait{width:126px;margin:0 auto 8px}
.sg-sum-portrait svg{width:100%;height:auto;display:block}
.sg-sum-rows div{padding:7px 2px;border-bottom:1px dashed var(--line);font-size:14.5px;line-height:1.6}
/* ---------- 全身立绘：对话与人物卡 ---------- */
.dlg-portrait{width:150px;aspect-ratio:200/340}
.person .p-head .pava{width:76px;height:128px;flex:none}
.person .p-head .pava svg{width:100%;height:100%}
/* ---------- 宫城示意图 ---------- */
#sgPalaceMap{border:2px solid var(--gold);border-radius:14px;overflow:hidden;margin-bottom:14px;background:#efe3c6}
.sg-map-cap{padding:8px 12px;font-size:13px;font-weight:700;color:#7c1f18;background:#f6ecd4;border-bottom:1px solid var(--line)}
.sg-map-svg svg{display:block;width:100%;height:auto}
.sg-map-node{cursor:pointer}
.sg-map-node text{pointer-events:none}
"""
new_t = new_t.replace("</head>", "<style>" + css + "</style>\n</head>", 1)

# ---------- 4. 存档 JS（追加在 </body> 前，所有游戏脚本之后） ----------
js = """
<script>
"use strict";
/* ============ 深宫弈·竖屏版存档（新增，不改原逻辑） ============ */
var SG_SAVE_KEY="shengongyi-save-v1";
function sgSave(manual){
  if(!window.G||G.over)return;
  try{localStorage.setItem(SG_SAVE_KEY,JSON.stringify({v:1,savedAt:Date.now(),G:G}));
    if(manual&&typeof toast==="function")toast("已存档");}catch(e){}
}
function sgLoad(){
  try{var d=JSON.parse(localStorage.getItem(SG_SAVE_KEY)||"null");
    return (d&&d.G)?d:null;}catch(e){return null;}
}
function sgContinue(){
  var d=sgLoad();
  if(!d){if(typeof toast==="function")toast("还没有存档");return;}
  G=d.G;
  document.getElementById("setupView").classList.add("hidden");
  document.getElementById("gameView").classList.remove("hidden");
  renderAll();
  var f=document.getElementById("sgSaveFab");if(f)f.style.display="flex";
  if(typeof toast==="function")toast("已读取存档 · "+new Date(d.savedAt).toLocaleString("zh-CN"));
}
function sgClearSave(){
  try{localStorage.removeItem(SG_SAVE_KEY);}catch(e){}
  var b=document.getElementById("sgContinueBtn");if(b){b.disabled=true;b.textContent="继续上局（无存档）";}
  if(typeof toast==="function")toast("存档已清除");
}
/* 自动存档：每次渲染完存一次；切后台/关闭前再存一次 */
(function(){
  var _renderAll=renderAll;
  renderAll=function(){_renderAll();sgSave(false);};
  var _start=startGame;
  startGame=function(){_start();sgSave(false);
    var f=document.getElementById("sgSaveFab");if(f)f.style.display="flex";};
  document.addEventListener("visibilitychange",function(){if(document.hidden)sgSave(false);});
  window.addEventListener("beforeunload",function(){sgSave(false);});
  /* 长文点一下展开全文 */
  document.addEventListener("click",function(e){
    var t=e.target.closest("#logList li,.modal .mbody,.person .meta,.card .desc,.loc span,.act span");
    if(t)t.classList.toggle("sg-open");
  });
  /* 开局页：继续上局 + 清除存档 */
  var bar=document.querySelector(".startbar");
  if(bar){
    var d=sgLoad();
    var row=document.createElement("div");
    row.style.cssText="display:flex;gap:8px;margin-top:10px";
    row.innerHTML='<button class="btn gold" id="sgContinueBtn" style="flex:1"'+(d?"":" disabled")+'>'+(d?"继续上局 · "+new Date(d.savedAt).toLocaleDateString("zh-CN"):"继续上局（无存档）")+'</button>'
      +'<button class="btn danger" id="sgClearBtn">清除存档</button>';
    bar.appendChild(row);
    document.getElementById("sgContinueBtn").addEventListener("click",sgContinue);
    document.getElementById("sgClearBtn").addEventListener("click",sgClearSave);
  }
  /* 底部存档浮钮 */
  var fab=document.createElement("button");
  fab.id="sgSaveFab";fab.textContent="存档";
  fab.addEventListener("click",function(){sgSave(true);});
  document.body.appendChild(fab);
})();
</script>
"""
js2 = (Path.home() / "workspace/shengongyi-ios/wizard.js").read_text(encoding="utf-8")
new_t = new_t.replace("</body>", js + '\n<script>\n"use strict";\n' + js2 + "\n</script>\n</body>", 1)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(new_t, encoding="utf-8")
OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
OUT_WEB.write_text(new_t, encoding="utf-8")
print(f"optimized: {OUT.stat().st_size/1e6:.2f} MB -> {OUT}")
print(f"web copy:  {OUT_WEB}")
print(f"saved: {(orig_bytes-OUT.stat().st_size)/1e6:.2f} MB ({100*(1-OUT.stat().st_size/orig_bytes):.0f}% smaller)")
