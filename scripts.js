function toggleBlur(isBlur) {
    const body = document.querySelector('body');
    if (isBlur) {
        body.classList.add('blur');
    } else {
        body.classList.remove('blur');
    }
}
