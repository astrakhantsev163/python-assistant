document.addEventListener("DOMContentLoaded", function () {
    const weatherData = [
        { day: "Понедельник", temperature: "22°C", humidity: "60%" },
        { day: "Вторник", temperature: "24°C", humidity: "55%" },
        { day: "Среда", temperature: "20°C", humidity: "70%" },
        { day: "Четверг", temperature: "18°C", humidity: "75%" },
        { day: "Пятница", temperature: "21°C", humidity: "65%" },
        { day: "Суббота", temperature: "23°C", humidity: "60%" },
        { day: "Воскресенье", temperature: "25°C", humidity: "50%" },
    ];

    const weatherContainer = document.getElementById("weather-container");

    weatherData.forEach((data) => {
        const card = document.createElement("div");
        card.className = "weather-card";

        card.innerHTML = `
            <h3>${data.day}</h3>
            <p>Температура: ${data.temperature}</p>
            <p>Влажность: ${data.humidity}</p>
        `;

        weatherContainer.appendChild(card);
    });
});