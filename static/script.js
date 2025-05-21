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

document.addEventListener('DOMContentLoaded', function() {
    // Элементы пользовательского интерфейса
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const checkAvailabilityBtn = document.getElementById('checkAvailability');
    const backBtn = document.getElementById('backBtn');
    const availableTimesList = document.getElementById('availableTimes');
    const reservationForm = document.getElementById('reservationForm');

    // Обработчик кнопки поиска доступного времени
    checkAvailabilityBtn.addEventListener('click', function() {
        const dateInput = document.getElementById('res-date');
        const sizeInput = document.getElementById('res-size');
        const timeInput = document.getElementById('res-time');
        
        // Проверка заполнения всех полей
        if (!dateInput.value || !sizeInput.value || !timeInput.value) {
            alert('Please fill in all fields');
            return;
        }
        
        // Отправка запроса на сервер
        fetch('/check_availability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: dateInput.value,
                time: timeInput.value,
                party_size: sizeInput.value
            })
        })
        .then(response => response.json())
        .then(data => {
            // Очищаем список доступных времен
            availableTimesList.innerHTML = '';
            
            if (data.times && data.times.length > 0) {
                // Отображаем доступные времена
                data.times.forEach(timeSlot => {
                    const timeItem = document.createElement('li');
                    timeItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                    
                    // Создаем контейнер для времени и бейджа
                    const timeInfo = document.createElement('div');
                    
                    // Добавляем время
                    const timeText = document.createElement('strong');
                    timeText.textContent = timeSlot.time;
                    timeInfo.appendChild(timeText);
                    
                    // Если это изначально выбранное время, добавляем бейдж
                    if (timeSlot.is_original) {
                        const badge = document.createElement('span');
                        badge.className = 'badge bg-success ms-2';
                        badge.textContent = 'Your selected time';
                        timeInfo.appendChild(badge);
                    }
                    
                    // Добавляем время в элемент списка
                    timeItem.appendChild(timeInfo);
                    
                    // Создаем кнопку бронирования
                    const bookBtn = document.createElement('a');
                    bookBtn.className = 'modal-window-book-button btn btn-sm';
                    bookBtn.textContent = 'Book';
                    bookBtn.href = `/confirm_reservation/${dateInput.value}/${timeSlot.time}/${sizeInput.value}`;
                    timeItem.appendChild(bookBtn);
                    
                    // Добавляем элемент в список
                    availableTimesList.appendChild(timeItem);
                });
                
                // Переключаемся на шаг 2
                step1.style.display = 'none';
                step2.style.display = 'block';
            } else {
                // Если нет доступных времен
                const noTimeItem = document.createElement('li');
                noTimeItem.className = 'list-group-item text-center';
                noTimeItem.textContent = 'No available times found. Please try different date or time.';
                availableTimesList.appendChild(noTimeItem);
                
                // Переключаемся на шаг 2
                step1.style.display = 'none';
                step2.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error checking availability:', error);
            alert('Error checking availability. Please try again.');
        });
    });
    
    // Обработчик кнопки "Назад"
    backBtn.addEventListener('click', function() {
        // Возвращаемся на шаг 1
        step2.style.display = 'none';
        step1.style.display = 'block';
    });
});