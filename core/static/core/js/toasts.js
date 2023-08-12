$(document).ready(function () {
    const toastElements = $('.toast').toArray();
    const toasts = toastElements.map(function (toastElement) {
        // Initialize each toast with default options
        return new bootstrap.Toast(toastElement);
    });

    // Immediately show all toasts
    toasts.forEach(toast => toast.show());
});
