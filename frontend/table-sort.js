function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementsByTagName("TABLE")[0];
    switching = true;
    dir = "asc"; 
    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        switch (n) {  
          case 0: // Название дома (алфавит)
            if (dir == "asc") {
              if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                shouldSwitch= true;
                break;
              }
            } else if (dir == "desc") {
              if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
              }
            }
            break;
          case 1: // Дата аренды (ближайшая/последняя)
            let dateX = new Date(x.innerHTML.split('-')[0].trim()); // Обработка дат
            let dateY = new Date(y.innerHTML.split('-')[0].trim());
            if (dir == "asc") {
              if (dateX > dateY) {
                shouldSwitch = true;
                break;
              }
            } else if (dir == "desc") {
              if (dateX < dateY) {
                shouldSwitch = true;
                break;
              }
            }
            break;
          case 2: // Цена (возрастание/убывание)
            let priceX = parseInt(x.innerHTML.replace(/\D/g, ''));
            let priceY = parseInt(y.innerHTML.replace(/\D/g, ''));
            if (dir == "asc") {
              if (priceX > priceY) {
                shouldSwitch = true;
                break;
              }
            } else if (dir == "desc") {
              if (priceX < priceY) {
                shouldSwitch = true;
                break;
              }
            }
            break;
            case 3: // Оценка (по количеству желтых звезд)
            let ratingX = x.querySelectorAll('img[data-color="yellow"]').length;
            let ratingY = y.querySelectorAll('img[data-color="yellow"]').length;
            if (dir == "asc") {
              if (ratingX < ratingY) {
                shouldSwitch = true;
                break;
              }
            } else if (dir == "desc") {
              if (ratingX > ratingY) {
                shouldSwitch = true;
                break;
              }
            }
            break;        
        }  
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        }
      }
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }