
document.addEventListener('DOMContentLoaded', function() {
    const intervalContainer = document.getElementById('intervals-container');
    const addIntervalButton = document.getElementById('add-interval');
    const intervalTemplate = document.getElementById('interval-template');

    let intervalCount = 0;

    function addInterval() {
        const newInterval = document.importNode(intervalTemplate.content, true);

        const placeSelect = newInterval.querySelector('.place-select');
        const startTime = newInterval.querySelector('.start-time');
        const endTime = newInterval.querySelector('.end-time');

        placeSelect.name = `interval[${intervalCount}][place]`;
        startTime.name = `interval[${intervalCount}][start_time]`;
        endTime.name = `interval[${intervalCount}][end_time]`;

        const removeButton = newInterval.querySelector('.remove-interval');
        removeButton.addEventListener('click', function() {
            const intervalBlocks = intervalContainer.querySelectorAll('.interval-block');
            if (intervalBlocks.length > 1) {
                this.closest('.interval-block').remove();

                updateIntervalIndices();
            }
        });

        if (intervalCount === 0) {
            removeButton.style.display = 'none';
        }

        intervalContainer.appendChild(newInterval);

        intervalCount++;
    }

    function updateIntervalIndices() {
        const intervalBlocks = intervalContainer.querySelectorAll('.interval-block');

        intervalBlocks.forEach((block, index) => {
            const placeSelect = block.querySelector('.place-select');
            const startTime = block.querySelector('.start-time');
            const endTime = block.querySelector('.end-time');
            const removeButton = block.querySelector('.remove-interval');

            placeSelect.name = `interval[${index}][place]`;
            startTime.name = `interval[${index}][start_time]`;
            endTime.name = `interval[${index}][end_time]`;

            if (intervalBlocks.length === 1) {
                removeButton.style.display = 'none';
            } else {
                removeButton.style.display = 'block';
            }
        });

        intervalCount = intervalBlocks.length;
    }

    addIntervalButton.addEventListener('click', addInterval);

    addInterval();
});
