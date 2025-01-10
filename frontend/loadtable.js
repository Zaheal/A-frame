async function loadUsers() {
    const response = await fetch("/admin/users/")
    const users = await response.json()
    let tableHTML = `
        <thead class="section-2__table_thead">
            <th class="section-2__table_thead-item _name_column" data-type="string" onclick="sortTable(0)">
                Имя
            </th>
            <th class="section-2__table_thead-item _email_column" data-type="string" onclick="sortTable(0)">
                Почта
            </th>
            <th class="section-2__table_thead-item _number_column" data-type="number" onclick="sortTable(2)">
                Номер
            </th>
            <th class="section-2__table_thead-item _telegram_column" data-type="number" onclick="sortTable(2)">
                Телеграм
            </th>
            <th class="section-2 _delete_column" data-type="string">
                Удалить
            </th>
        </thead>
        <tbody class="section-2__table_body">`;        
    users.forEach(user => {
        tableHTML += `
        <tr class="section-2__table_body-row">
            <td class="section-2__table_body-item">
                ${ user.name }
            </td>
            <td class="section-2__table_body-item">
                ${ user.email }
            </td>
            <td class="section-2__table_body-item">
                ${ user.number }
            </td>
            <td class="section-2__table_body-item">
                ${ user.tg_id }
            </td>
            <td class="section-2__table_body-item">
                <form action="/admin/delete/user/${ user.id }" method="post" onsubmit="window.location.reload()">
                    <button type="submit"><img style="cursor: pointer;" src="${pathTrash}"></button>
                </form>
            </td>
        </tr>`;
    })
    tableHTML += `</tbody>`
    document.getElementById("counter-people").innerHTML = users.length
    document.getElementById("table").innerHTML = tableHTML
};
async function loadReservations() {
    const response = await fetch("/admin/reservations")
    const reservations = await response.json()
    let tableHTML = `
        <thead class="section-2__table_thead">
            <th class="section-2__table_thead-item _house-name_column" data-type="string" onclick="sortTable(0)">
                Название дома
            </th>
            <th class="section-2__table_thead-item _rental-date_column" data-type="string" onclick="sortTable(1)">
                Дата аренды
            </th>
            <th class="section-2__table_thead-item _price_column" data-type="number" onclick="sortTable(2)">
                Сумма
            </th>
            <th class="section-2 _bool_column" data-type="bool">
                Задаток
            </th>
            <th class="section-2__table_thead-item _name_column" data-type="string" onclick="sortTable(0)">
                Имя
            </th>
            <th class="section-2__table_thead-item _number_reserv_column" data-type="string">
                Номер
            </th>
            <th class="section-2" data-type="string">
                Удалить
            </th>
        </thead>
        <tbody class="section-2__table_body">`;
    reservations.forEach(reserv => {
        tableHTML += `
        <tr class="section-2__table_body-row">
            <td class="section-2__table_body-item">
                ${ reserv.house.style }
            </td>
            <td class="section-2__table_body-item">
                ${ reserv.start } - ${ reserv.end }
            </td>
            <td class="section-2__table_body-item">
                ${ reserv.full_price }&#8381;
            </td>
            <td class="section-2__table_body-item">
                <label class="switch">
                    <input type="checkbox" onclick="updateReservation(this)" id="${reserv.id}" ${reserv.was_paid ? 'checked' : ''}>
                    <span class="slider round"></span>
                </label>
            </td>
            <td class="section-2__table_body-item">
                ${ reserv.user.name }
            </td>
            <td class="section-2__table_body-item">
                ${ reserv.user.number }
            </td>
            <td class="section-2__table_body-item">
                <form action="/admin/delete/reservation/${ reserv.id }" method="post" onsubmit="window.location.reload()">
                    <button type="submit"><img style="cursor: pointer;" src="${pathTrash}"></button>
                </form>
            </td>
        </tr>`;
    })
    tableHTML += `</tbody>`
    document.getElementById("counter-reservations").innerHTML = reservations.length
    document.getElementById("table").innerHTML = tableHTML
}

document.getElementById("show-users").addEventListener('click', loadUsers)
document.getElementById("show-reservations").addEventListener('click', loadReservations)

loadReservations();


async function updateReservation(checkbox) {
    const isChecked = checkbox.checked;

    await fetch(`/admin/update/reservation/${checkbox.id}`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({was_paid: isChecked})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Успех:', data);
    })
    .catch((error) => {
        console.error('Ошибка:', error);
    });
}