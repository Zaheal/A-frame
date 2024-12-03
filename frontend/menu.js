const menuTrigger = document.querySelector('.header__menu');
        const menu = document.querySelector('.menu-container');
      
        menuTrigger.addEventListener('click', () => {
          menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        });
      
        // Закрытие меню при клике вне меню (важно для предотвращения конфликтов)
        document.addEventListener('click', (event) => {
          if (!menuTrigger.contains(event.target) && !menu.contains(event.target)) {
            menu.style.display = 'none';
          }
        });