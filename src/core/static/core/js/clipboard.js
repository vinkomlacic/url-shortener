$(document).ready(function () {
    $('.copy-to-clipboard').click(function (event) {
        const copyButton = $(this);

        const sourceId = copyButton.data('source');
        console.log(sourceId);

        const sourceElement = $(sourceId);
        console.log(sourceElement);

        const textToCopy = sourceElement.text().trim();
        console.log(textToCopy);

        navigator.clipboard.writeText(textToCopy).then(function () {
            // After text is written to the clipboard show a tooltip on the
            // clipboard button which says that the text has been copied.
            const tooltip = new bootstrap.Tooltip(
                copyButton, {title: 'Copied to clipboard!',}
            );
            tooltip.show();

            // After 1 second, remove the tooltip
            setTimeout(function() {tooltip.dispose()}, 1000);
        });
    });
});
