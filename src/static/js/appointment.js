function downloadFile(url) {
    is_downloaded = document.querySelector("#is_downloaded")
    console.log(is_downloaded.value);
    if(is_downloaded.checked == false) {
        is_downloaded.checked = true;
        is_downloaded.value = true
    }
}