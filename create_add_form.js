document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".work-park-checkbox").forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            let hoursInput = this.closest("li").querySelector(".work-hours");
            let minutesInput = this.closest("li").querySelector(".work-minutes");

            hoursInput.disabled = !this.checked;
            minutesInput.disabled = !this.checked;
        });
    });

    document.querySelectorAll(".reserve-section-checkbox").forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            let hoursInput = this.closest("li").querySelector(".reserve-hours");
            let minutesInput = this.closest("li").querySelector(".reserve-minutes");

            hoursInput.disabled = !this.checked;
            minutesInput.disabled = !this.checked;
        });
    });
});