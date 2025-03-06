let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();

const bookButton = document.getElementById("calendar-button")
const modalButton = document.getElementById("modal-button")
const unButton = document.getElementById("unauthorized-button") 

let selectedStartDate = null;
let selectedEndDate = null;
let addSelected = false
let addPrice = 0;
let fullPrice = 0;

const day = document.querySelector(".calendar-dates");

const currdate = document.querySelector(".calendar-current-date");

const prenexIcons = document.querySelectorAll(".calendar-navigation span");

const checkbox = document.getElementById("checkAdd");

const message = document.getElementById("answer")

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


const manipulate = () => {
    day.innerHTML = ''

    let dayone = new Date(year, month, 7).getDay();

    let lastdate = new Date(year, month + 1, 0).getDate();

    let dayend = new Date(year, month, lastdate).getDay();

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

    for (let i = dayone; i > 0; i--) {
        const dayElement = document.createElement('li')
        dayElement.textContent = monthlastdate - i + 1
        dayElement.classList.add('inactive')
        day.appendChild(dayElement)
    }

    for (let i = 1; i <= lastdate; i++) {
        const newDate = new Date(year, month, i);
        const dateSrc = newDate.toLocaleDateString('ru-Ru', {year: 'numeric', month: 'numeric', day: 'numeric'})
        const dateString = dateSrc.split(".").reverse().join("-");

        const dayElement = document.createElement('li')

        let isToday = i === date.getDate()
            && month === new Date().getMonth()
            && year === new Date().getFullYear()
            ? "active"
            : "day";
        dayElement.classList.add(isToday);

        if (newDate.getDay() == 0 || newDate.getDay() == 6) {
            dayElement.classList.remove("day")
            dayElement.classList.add("weekend")
        }
        dayElement.textContent = i;
        dayElement.dataset.date = dateString;

        newDate.setHours(newDate.getHours() + 3)
        if (dataObject[year] == null) {
            dataObject[year] = [[]]
        }
        dataObject[year].forEach(dates => {
            if (newDate > new Date(dates[0]) && newDate < new Date(dates[1])) {
                dayElement.classList.add('booked');
                dayElement.onclick = null; // Запретить клик на забронированные даты
            } else if (dateString === dates[0]) {
                if (dayElement.classList.contains('booked_end')) {
                    dayElement.classList.remove('booked_end')
                    dayElement.classList.add('booked');
                    dayElement.onclick = null;
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

    for (let i = dayend; i < 6; i++) {
        const dayElement = document.createElement('li')
        dayElement.textContent = i - dayend + 1
        dayElement.classList.add('inactive')
        day.appendChild(dayElement)
    }

    currdate.innerText = `${months[month]} ${year}`;
}

manipulate();

const activeData = document.querySelector(".active").dataset.date
const activeDate = new Date(activeData)

prenexIcons.forEach(icon => {

    icon.addEventListener("click", () => {

        month = icon.id === "calendar-prev" ? month - 1 : month + 1;

        if (month < 0 || month > 11) {

            date = new Date(year, month, new Date().getDate());

            year = date.getFullYear();

            month = date.getMonth();
        }

        else {

            date = new Date();
        }

        manipulate();
    });
});

// Выбраны ли доп услуги
checkbox.addEventListener("change", function() {
    if (this.checked) {
        addSelected = true
        addPrice = 3000
        if (selectedStartDate && selectedEndDate) {
            fullPrice += addPrice
            message.textContent = `Стоимость: ${fullPrice}\u20BD`
        }
    } else {
        addSelected = false
        addPrice = 0
        if (selectedStartDate && selectedEndDate) {
            fullPrice -= 3000
            message.textContent = `Стоимость: ${fullPrice}\u20BD`
        }
    }
})


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
    
    let counterWeekend = 0

    for (const day of days) {
        const item = day.dataset.date;
        const itemDate = new Date(item)
        if (( day.classList.contains("booked_start") && item === start )
            || ( day.classList.contains("booked_end") && item === end )
            || ( (day.classList.contains("booked") || day.classList.contains("booked_start") || day.classList.contains("booked_end")) && (itemDate > startDate && itemDate < endDate) )) {
            resetSelection();
            return
        } else if (item >= start && item <= end) {
            if (itemDate.getDay() == 5 || itemDate.getDay() == 6) {
                const nextDate = new Date(itemDate)
                nextDate.setDate(nextDate.getDate() + 1)
                if ((nextDate.getDay() == 6 || nextDate.getDay() == 0) && nextDate <= endDate) {
                    counterWeekend += 1000
                }
            }
            day.classList.add('selected');
        }
    };

    const diffInTime = endDate - startDate
    const diffInDays = diffInTime / (1000 * 3600 * 24);
    fullPrice = diffInDays * costDay + counterWeekend + addPrice
    message.textContent = `Стоимость: ${fullPrice}\u20BD`
}

// Функция для сброса выбора
function resetSelection() {
    selectedStartDate = null;
    selectedEndDate = null;
    
    const days = document.querySelectorAll('.calendar-dates li');
    days.forEach(day => day.classList.remove('selected'));
    message.textContent = ""
}

if (bookButton) {
    bookButton.addEventListener('click', async function(e) {
        e.preventDefault()

        if (selectedStartDate && selectedEndDate) {
            const items = {
                start: selectedStartDate,
                end: selectedEndDate,
                full_price: fullPrice,
                house_id: parseInt(window.location.pathname.split("/")[2]),
                add: addSelected,
            }

            await fetch('/api/create/reservation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(items)
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
                resetSelection()
            })
        } else {
            message.textContent = "Пожалуйста, выберите даты для бронирования"
        }
    });
}

function openModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.classList.add('active');
}


function closeModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.classList.remove('active');
}

if (unButton) {
    unButton.addEventListener('click', function (e) {
        e.preventDefault()

        if (selectedStartDate && selectedEndDate) {
            openModal()
        } else {
            message.textContent = "Пожалуйста, выберите даты для бронирования"
        }
    })
}


modalButton.addEventListener('click', async function (event) {
    event.preventDefault();
    const modalMessage = document.getElementById("modal-answer")

    if (selectedStartDate && selectedEndDate) {

        const items = {
            start: selectedStartDate,
            end: selectedEndDate,
            full_price: fullPrice,
            house_id: parseInt(window.location.pathname.split("/")[2]),
            add: addSelected,
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            number: document.getElementById("number").value,
        }
        console.log(items)
        await fetch('/api/create/temporary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(items)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка сервера, не удалось зарезервировать домик!")
            }
            alert("Вы успешно зарезервировали домик! В скором времени с вами свяжутся. Можете отменить бронь у себя в профиле.")
            location.reload()
        })
        .catch(error => {
            console.error("Ошибка:", error)
            alert("Ошибка, попробуйте позже или позвоните по номеру на главной странице.")
        })
    } else {
        modalMessage.textContent = "Пожалуйста, выберите даты для бронирования"
    }
});