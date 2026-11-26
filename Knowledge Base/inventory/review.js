'use strict';
const byID=id=>document.getElementById(id);
const labels={recurrent_panel_member:'Multiple panel families',single_panel_member:'One panel family',educational_supplement:'Educational supplement'};
function renderRoster(){
 const words=byID('query').value.toLowerCase().trim().split(/\s+/).filter(Boolean);
 const scope=byID('scope').value, group=byID('group').value;
 const genes=REVIEW_ROSTER.filter(g=>(scope==='all'||g.proposed===(scope==='proposed'))&&(!group||g.group===group)&&words.every(w=>[g.symbol,g.name,g.id,...g.aliases,...g.panels,...g.contexts].join(' ').toLowerCase().includes(w)));
 byID('count').textContent=`${genes.length} shown · ${REVIEW_ROSTER.filter(g=>g.proposed).length} proposed genes · ${REVIEW_ROSTER.filter(g=>!g.proposed).length} reserve candidates`;
 const body=byID('rows');body.replaceChildren();
 for(const g of genes){const row=document.createElement('tr');
  for(const [i,text] of [g.name,labels[g.group],g.contexts.join('; ')||'Panel membership only'].entries()){
   const cell=document.createElement('td');
   if(i===0){const strong=document.createElement('strong');strong.textContent=g.symbol;cell.append(strong,document.createElement('br'));}
   cell.append(document.createTextNode(text));
   const small=document.createElement('small');small.textContent=i===0?g.id:i===1?(g.panels.join(', ')||'No anchor-panel membership'):g.rationale;cell.append(small);row.append(cell);
  }body.append(row);
 }
 if(!genes.length){const row=document.createElement('tr'),cell=document.createElement('td');cell.colSpan=3;cell.textContent='No matching candidates. Broaden the search or select all candidates.';row.append(cell);body.append(row);}
}
for(const id of ['query','scope','group'])byID(id).addEventListener(id==='query'?'input':'change',renderRoster);
renderRoster();
