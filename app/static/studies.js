window.addEventListener('scroll', function () {
    let currentPos = document.documentElement.scrollTop;
    let winHeight = window.innerHeight;
    let section_header_images = document.getElementsByClassName('section-header-image')
    for (let i=0; i < section_header_images.length; i++){
        if (section_header_images[i].getBoundingClientRect().bottom <= winHeight){
            section_header_images[i].classList.add('show')
        } else if (section_header_images[i].getBoundingClientRect().top > winHeight){
            section_header_images[i].classList.remove('show')
        }
    }
});