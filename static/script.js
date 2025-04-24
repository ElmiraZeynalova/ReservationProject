document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector("#header");

    function updateHeader() {
        if (window.scrollY > 10) { 
            header.classList.add("header-scrolled");
        } else {
            header.classList.remove("header-scrolled");
        }
    }

    window.addEventListener("scroll", updateHeader);
    updateHeader();

});

document.addEventListener('DOMContentLoaded', () => {
    const checkBtn = document.getElementById('checkAvailability');
    const backBtn = document.getElementById('backBtn');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const timesList = document.getElementById('availableTimes');

    checkBtn.addEventListener('click', async () => {
        const date = document.getElementById('res-date').value;
        const time = document.getElementById('res-time').value;
        const size = document.getElementById('res-size').value;

        const res = await fetch('/check_availability', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date: date, time: time, party_size: size })
        });

        const data = await res.json();

        // Очистить список
        timesList.innerHTML = '';

        // Отобразить доступное или альтернативные времена
        if (data.times.length > 0) {
            data.times.forEach(alt => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = `${alt}`;
                const button = document.createElement('button');
                button.className = 'alternative-time-btn btn btn-primary'; // Изменен стиль кнопки
                button.setAttribute('data-time', alt);
                button.setAttribute('data-table-id', data.table_id || '1'); // Убедимся, что table_id передается
                button.textContent = 'Book';
                li.appendChild(button);
                timesList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.className = 'list-group-item text-danger';
            li.textContent = 'No available times found.';
            timesList.appendChild(li);
        }

        step1.style.display = 'none';
        step2.style.display = 'block';
    });

    backBtn.addEventListener('click', () => {
        step2.style.display = 'none';
        step1.style.display = 'block';
    });

    // Делегирование событий для кнопок с альтернативными временами
    document.getElementById('availableTimes').addEventListener('click', function (event) {
        if (event.target.classList.contains('alternative-time-btn')) {
            const selectedTime = event.target.getAttribute('data-time');
            const timeField = document.querySelector("#bookingModal select[name='time']");
            if (timeField) {
                timeField.value = selectedTime; // Устанавливаем выбранное время в поле формы
                // alert(`You selected ${selectedTime} as your reservation time.`); // Удалено уведомление
            }
        }
    });

    document.getElementById('availableTimes').addEventListener('click', function (event) {
        if (event.target.classList.contains('alternative-time-btn')) {
            const tableId = event.target.getAttribute('data-table-id');
            const selectedTime = event.target.getAttribute('data-time');
            const date = document.getElementById('res-date').value;

            if (!tableId) {
                alert('Invalid table ID.');
                return;
            }

            // Перенаправляем на страницу подтверждения
            window.location.href = `/confirm_reservation?table_id=${tableId}&date=${date}&time=${selectedTime}`;
        }
    });
});

