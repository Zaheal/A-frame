let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();

const bookButton = document.getElementById("calendar-button")

let selectedStartDate = null;
let selectedEndDate = null;

const day = document.querySelector(".calendar-dates");

const currdate = document.querySelector(".calendar-current-date");

const prenexIcons = document.querySelectorAll(".calendar-navigation span");

// Array of month names
const months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
];

// Function to generate the calendar
const manipulate = () => {
    day.innerHTML = ''

    // Get the first day of the month
    let dayone = new Date(year, month, 7).getDay();

    // Get the last date of the month
    let lastdate = new Date(year, month + 1, 0).getDate();

    // Get the day of the last date of the month
    let dayend = new Date(year, month, lastdate).getDay();

    // Get the last date of the previous month
    let monthlastdate = new Date(year, month, 0).getDate();

    // Декодирование HTML-энкодированных символов
    const decodedString = disabledDates
        .replace(/&#39;/g, "'") // Заменяем &#39; на '
        .replace(/&quot;/g, '"') // Заменяем &quot; на "
        .replace(/&amp;/g, '&') // Заменяем &amp; на &
        .replace(/&lt;/g, '<') // Заменяем &lt; на <
        .replace(/&gt;/g, '>'); // Заменяем &gt; на >

    // Заменяем одинарные кавычки на двойные
    const jsonString = decodedString.replace(/'/g, '"');
    
    // Преобразуем строку в объект
    const dataObject = JSON.parse(jsonString);

    // Loop to add the last dates of the previous month
    for (let i = dayone; i > 0; i--) {
        const dayElement = document.createElement('li')
        dayElement.textContent = monthlastdate - i + 1
        dayElement.classList.add('inactive')
        day.appendChild(dayElement)
    }

    // Loop to add the dates of the current month
    for (let i = 1; i <= lastdate; i++) {
        const newDate = new Date(year, month, i);
        const dateSrc = newDate.toLocaleDateString('ru-Ru', {year: 'numeric', month: 'numeric', day: 'numeric'})
        const dateString = dateSrc.split(".").reverse().join("-");

        const dayElement = document.createElement('li')
        // Check if the current date is today
        let isToday = i === date.getDate()
            && month === new Date().getMonth()
            && year === new Date().getFullYear()
            ? "active"
            : "day";
        dayElement.classList.add(isToday);
        dayElement.textContent = i;
        dayElement.dataset.date = dateString;

        newDate.setHours(newDate.getHours() + 3)
        dataObject.forEach(dates => {
            if (newDate > new Date(dates[0]) && newDate < new Date(dates[1])) {
                dayElement.classList.add('booked');
                dayElement.onclick = null; // Запретить клик на забронированные даты
            } else if (dateString === dates[0]) {
                if (dayElement.classList.contains('booked_end')) {
                    dayElement.classList.remove('booked_end')
                    dayElement.classList.add('booked');
                    dayElement.onclick = null; // Запретить клик на забронированные даты
                    return;
                }
                dayElement.classList.add("booked_start")
                dayElement.onclick = () => toggleDateSelection(dayElement)
            } else if (dateString === dates[1]) {
                dayElement.classList.add("booked_end")
                dayElement.onclick = () => toggleDateSelection(dayElement)
            } else if (newDate > new Date(selectedStartDate) && newDate < new Date(selectedEndDate)) {
                dayElement.classList.add("selected")
                dayElement.onclick = () => toggleDateSelection(dayElement)
            } else {
                dayElement.onclick = () => toggleDateSelection(dayElement);
            }
        })
        day.appendChild(dayElement);
    }

    // Loop to add the first dates of the next month
    for (let i = dayend; i < 6; i++) {
        const dayElement = document.createElement('li')
        dayElement.textContent = i - dayend + 1
        dayElement.classList.add('inactive')
        day.appendChild(dayElement)
    }

    // Update the text of the current date element 
    // with the formatted current month and year
    currdate.innerText = `${months[month]} ${year}`;
}

manipulate();

const activeData = document.querySelector(".active").dataset.date
const activeDate = new Date(activeData)

// Attach a click event listener to each icon
prenexIcons.forEach(icon => {

    // When an icon is clicked
    icon.addEventListener("click", () => {

        // Check if the icon is "calendar-prev"
        // or "calendar-next"
        month = icon.id === "calendar-prev" ? month - 1 : month + 1;

        // Check if the month is out of range
        if (month < 0 || month > 11) {

            // Set the date to the first day of the 
            // month with the new year
            date = new Date(year, month, new Date().getDate());

            // Set the year to the new year
            year = date.getFullYear();

            // Set the month to the new month
            month = date.getMonth();
        }

        else {

            // Set the date to the current date
            date = new Date();
        }

        // Call the manipulate function to 
        // update the calendar display
        manipulate();
    });
});


function toggleDateSelection(dayElement) {
    const data = dayElement.dataset.date

    if (!selectedStartDate && activeDate <= new Date(data)) {
        selectedStartDate = data;
        dayElement.classList.add('selected')
    } else if (!selectedEndDate && data > selectedStartDate) {
        selectedEndDate = data;
        dayElement.classList.add('selected');
        highlightRange(selectedStartDate, selectedEndDate);
    } else {
        resetSelection();
    }
}

// Функция для выделения диапазона дат
function highlightRange(start, end) {
    const days = document.querySelectorAll(".calendar-dates li")

    const startDate = new Date(start)
    const endDate = new Date(end)

    for (const day of days) {
        const item = day.dataset.date;
        const itemDate = new Date(item)
        if (( day.classList.contains("booked_start") && item === start )
            || ( day.classList.contains("booked_end") && item === end )
            || ( (day.classList.contains("booked") || day.classList.contains("booked_start") || day.classList.contains("booked_end")) && (itemDate > startDate && itemDate < endDate) )) {
            resetSelection();
            break
        } else if (item >= start && item <= end) {
            day.classList.add('selected');
        }
    };

    const message = document.getElementById("answer")

    const diffInTime = endDate - startDate
    const diffInDays = diffInTime / (1000 * 3600 * 24);
    message.textContent = `Стоимость: ${diffInDays * costDay}\u20BD`
}

// Функция для сброса выбора
function resetSelection() {
    selectedStartDate = null;
    selectedEndDate = null;
    
    const days = document.querySelectorAll('.calendar-dates li');
    days.forEach(day => day.classList.remove('selected'));
    const message = document.getElementById("answer")
    message.textContent = ""
}

bookButton.addEventListener('click', async function(e) {
    const startDate = new Date(selectedStartDate)
    const endDate = new Date(selectedEndDate)

    const diffInTime = endDate - startDate
    const diffInDays = diffInTime / (1000 * 3600 * 24);
    const item = {
        start: selectedStartDate,
        end: selectedEndDate,
        full_price: diffInDays * costDay,
        house_id: parseInt(window.location.pathname.split("/")[2]),
    }
    const message = document.getElementById("answer")

    if (selectedStartDate && selectedEndDate) {
        await fetch('/api/create/reservation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка сервера, не удалось зарезервировать домик!")
            }
            message.textContent = "Вы успешно зарезервировали домик! В скором времени с вами свяжутся. Можете отменить бронь у себя в профиле."
        })
        .catch(error => {
            console.error("Ошибка:", error)
            message.textContent = "Ошибка, попробуйте позже или позвоните по номеру на главной странице."
            message.style.color = "red"
        })
    } else {
        message.textContent = 'Пожалуйста, выберите даты для бронирования.'
    }
});