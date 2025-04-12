
document.addEventListener('DOMContentLoaded', function() {
    // Получаем ссылки на элементы формы
    const intervalContainer = document.getElementById('intervals-container');
    const addIntervalButton = document.getElementById('add-interval');
    const intervalTemplate = document.getElementById('interval-template');

    // Счетчик для уникальных индексов интервалов
    let intervalCount = 0;

    // Функция добавления нового интервала
    function addInterval() {
        // Клонируем шаблон
        const newInterval = document.importNode(intervalTemplate.content, true);

        // Устанавливаем правильные имена полей с учетом индекса
        const placeSelect = newInterval.querySelector('.place-select');
        const startTime = newInterval.querySelector('.start-time');
        const endTime = newInterval.querySelector('.end-time');

        placeSelect.name = `interval[${intervalCount}][place]`;
        startTime.name = `interval[${intervalCount}][start_time]`;
        endTime.name = `interval[${intervalCount}][end_time]`;

        // Добавляем обработчик для кнопки удаления
        const removeButton = newInterval.querySelector('.remove-interval');
        removeButton.addEventListener('click', function() {
            // Проверяем, не является ли этот интервал единственным
            const intervalBlocks = intervalContainer.querySelectorAll('.interval-block');
            if (intervalBlocks.length > 1) {
                this.closest('.interval-block').remove();

                // Обновляем индексы оставшихся интервалов
                updateIntervalIndices();
            }
        });

        // Скрываем кнопку удаления, если это первый интервал
        if (intervalCount === 0) {
            removeButton.style.display = 'none';
        }

        // Добавляем новый интервал в контейнер
        intervalContainer.appendChild(newInterval);

        // Увеличиваем счетчик
        intervalCount++;
    }

    // Функция для обновления индексов полей после удаления интервала
    function updateIntervalIndices() {
        const intervalBlocks = intervalContainer.querySelectorAll('.interval-block');

        intervalBlocks.forEach((block, index) => {
            const placeSelect = block.querySelector('.place-select');
            const startTime = block.querySelector('.start-time');
            const endTime = block.querySelector('.end-time');
            const removeButton = block.querySelector('.remove-interval');

            // Обновляем имена полей
            placeSelect.name = `interval[${index}][place]`;
            startTime.name = `interval[${index}][start_time]`;
            endTime.name = `interval[${index}][end_time]`;

            // Скрываем кнопку удаления на единственном интервале
            if (intervalBlocks.length === 1) {
                removeButton.style.display = 'none';
            } else {
                removeButton.style.display = 'block';
            }
        });

        // Сбрасываем счетчик на текущее количество блоков
        intervalCount = intervalBlocks.length;
    }

    // Добавляем обработчик клика для кнопки добавления интервала
    addIntervalButton.addEventListener('click', addInterval);

    // Добавляем первый интервал по умолчанию
    addInterval();
});
