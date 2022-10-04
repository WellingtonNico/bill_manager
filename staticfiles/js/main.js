if (navLinkIndex!=undefined){
    document.getElementsByClassName('nav-link')[navLinkIndex].classList.add('active')
}

function cleanFilters(){
    var filterForm = document.querySelector('#filter_form')
    for(var input of filterForm.getElementsByTagName('input')){
        input.value = ''
    }
    // for(var input of filterForm.getElementsByTagName('select')){
    //     input.value = ''
    // }
}