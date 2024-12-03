$(document).ready(function() {
    $('.section-2__slider-infinity').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        infinity: true,
        centerMode: true,
        centerPadding: '152px',
    });
    $('.slick-prev').text('');
    $('.slick-next').text('');
});


const buttons = document.querySelectorAll('.section-4__maintext-block_button');

buttons.forEach((button, index) => {
  button.addEventListener('click', () => {
    const hiddenText = document.querySelector(`.section-4__hidden-text-${index + 1}`);
    hiddenText.classList.toggle('show_hidden-text');
    const buttonStyle = document.getElementById(`button${index+1}`)
    buttonStyle.classList.toggle('button-style_active')
  });
});