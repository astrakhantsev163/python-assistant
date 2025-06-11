document.addEventListener('DOMContentLoaded', function () {
    // Модальное окно для удаления
    const deleteModal = document.getElementById('delete-modal'); // Модальное окно для удаления
    const closeButtons = document.querySelectorAll('.close-btn'); // Все кнопки "крестик"
    const cancelDeleteBtn = deleteModal.querySelector('.cancel-btn'); // Кнопка "Отмена" в модалке удаления
    const deleteBtn = deleteModal.querySelector('.delete-btn'); // Кнопка "Удалить" в модалке удаления
    const deleteModalClose = deleteModal.querySelector('.close'); // Крестик для закрытия модалки удаления

    // Открытие модального окна при клике на "крестик"
    closeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // Предотвращаем распространение события
            deleteModal.style.display = 'block'; // Показываем модальное окно
            const cardToRemove = button.closest('.weather-card'); // Находим родительскую карточку
            deleteModal.dataset.target = cardToRemove.id; // Сохраняем ID карточки для удаления
        });
    });

    // Закрытие модального окна при клике на "Отмена" или крестик
    [cancelDeleteBtn, deleteModalClose].forEach(element => {
        element.addEventListener('click', function () {
            deleteModal.style.display = 'none'; // Скрываем модальное окно
        });
    });

    // Подтверждение удаления при клике на "Удалить"
    deleteBtn.addEventListener('click', function () {
        const targetCardId = deleteModal.dataset.target; // Получаем ID карточки для удаления
        if (targetCardId) {
            const cardToRemove = document.getElementById(targetCardId);
            if (cardToRemove) {
                cardToRemove.remove(); // Удаляем карточку
            }
        }
        deleteModal.style.display = 'none'; // Скрываем модальное окно
    });

    // Модальное окно для добавления врача
    const addDoctorModal = document.getElementById('modal-doctor'); // Модальное окно для добавления врача
    const addDoctorBtn = document.getElementById('add-doctor'); // Кнопка "Добавить врача"
    const addDoctorModalClose = addDoctorModal.querySelector('.close'); // Крестик для закрытия модалки добавления

    // Открытие модального окна при клике на "Добавить врача"
    if (addDoctorBtn && addDoctorModal) {
        addDoctorBtn.addEventListener('click', function () {
            addDoctorModal.style.display = 'block'; // Показываем модальное окно
        });
    }

    // Закрытие модального окна при клике на крестик
    if (addDoctorModalClose && addDoctorModal) {
        addDoctorModalClose.addEventListener('click', function () {
            addDoctorModal.style.display = 'none'; // Скрываем модальное окно
        });
    }

    // Закрытие модального окна при клике вне его области
    window.addEventListener('click', function (event) {
        if (event.target === addDoctorModal) {
            addDoctorModal.style.display = 'none';
        }
    });
});
