//make table
var tableEle = document.getElementById('tbodyID');

for (var i = 0; i < 5; i++) {
  // テーブルの行を 5行追加する
  var tr = document.createElement('tr');
  for (var j = 0; j < 3; j++) {
    // テーブルの列を 3行追加する
    var td = document.createElement('td');

    if(j == 2){
        var a_cbutton = document.createElement('a');
        a_cbutton.href = "/change";
        var cbutton = document.createElement('button');
        cbutton.type = "submit";
        cbutton.value = i;
        cbutton.onclick =
        cbutton.className = "cbutton";
        cbutton.innerHTML = "✎";
        td.innerHTML = 'データ'+(i+1)+"-"+(j+1);
        tr.appendChild(td);
        td.append(a_cbutton);
        a_cbutton.appendChild(cbutton);
        
    }else{
        td.innerHTML = 'データ'+(i+1)+"-"+(j+1);
        tr.appendChild(td);        
    }

  }
  tableEle.appendChild(tr);
}