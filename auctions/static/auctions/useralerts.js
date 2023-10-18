document.addEventListener('DOMContentLoaded', () => {
    const notifier = document.querySelector('#alerts');

    async function getAlerts() {
        const resp = await fetch("/user/get_alerts");
        const alerts = await resp.json();
        notifier.innerHTML = `${alerts.num}`;
    }

    getAlerts();
})