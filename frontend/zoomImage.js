function fullScreen(img) {
    // Создаем overlay для полноэкранного режима
    const overlay = document.createElement('div');
    overlay.classList.add('fullscreen-overlay');

    // Создаем копию изображения для полноэкранного режима
    const fullscreenImg = document.createElement('img');
    fullscreenImg.src = img.src;
    fullscreenImg.alt = img.alt;

    // Добавляем изображение в overlay
    overlay.appendChild(fullscreenImg);

    // Добавляем overlay на страницу
    document.body.appendChild(overlay);

    // Закрываем полноэкранный режим при клике на overlay
    overlay.addEventListener('click', () => {
        document.body.removeChild(overlay);
    });
}