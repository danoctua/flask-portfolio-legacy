// let startpoint = 0;
// let startScrollPosition = 0;
// let currentDivPos = 0;
let lastScrollTop = 0;
// let scrollingByFunction = false;

const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
}


window.onload = function () {


    // const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    //
    //
    // if (currentTheme === 'dark') {
    //     toggleSwitch.checked = true;
    // }
    //
    //
    // function switchTheme(e) {
    //     if (e.target.checked) {
    //         document.documentElement.setAttribute('data-theme', 'dark');
    //         localStorage.setItem('theme', 'dark');
    //     } else {
    //         document.documentElement.setAttribute('data-theme', 'light');
    //         localStorage.setItem('theme', 'light');
    //     }
    // }
    //
    // toggleSwitch.addEventListener('change', switchTheme, false);
    // hideHelp();

    let actions = ["click", "tap"];
    for (let i = 0; i < actions.length; i++) {

        let tab_links = document.getElementsByClassName("tab-link");
        for (let j = 0; j < tab_links.length; j++) {
            tab_links[j].addEventListener(actions[i], function (event) {
                switchTab(event.target)
            })
        }
        if (tab_links) {
            initialTabSwitch();
        }
    }


    let login_div = document.getElementById('login-div');
    let login_content_div = document.getElementById('login-content-div');

    login_div.addEventListener('click', function (event) {
        let targ = event.target;
        while (targ) {
            if (targ === login_content_div) {
                return
            }
            targ = targ.parentNode;
        }

        hideLogin();
    }, false);

    // let main = document.getElementById('main');
    // let sideNavBar = document.getElementById('mySidenav');
    // main.addEventListener('click', function (event) {
    //     let targ = event.target;
    //     while (targ) {
    //         if (targ === sideNavBar) {
    //             return
    //         }
    //         targ = targ.parentNode;
    //     }
    //     closeNav();
    // }, false);

    function showNotification(wrapper) {
        let notification_content = wrapper.getElementsByClassName('notification-content');
        if (notification_content && notification_content.length > 0) {
            notification_content = notification_content[0]
        }
        let notification_timer = document.getElementsByClassName('notification-timer');
        if (notification_timer && notification_timer.length > 0) {
            notification_timer = notification_timer[0]
        }
        let frame_length = Math.max(notification_content.innerText.length / 10, 7) * 10;
        wrapper.classList.add("show");

        let width = 100;
        let current_state = setInterval(frame, frame_length);

        function frame() {
            if (width <= 0) {
                hideNotification(wrapper);
                clearInterval(current_state);
            } else {
                width--;
                notification_timer.style.width = width + '%';
            }
        }


    }

    let notification_wrappers = document.getElementsByClassName('notification-wrapper');
    for (let i = 0; i < notification_wrappers.length; i++) {
        showNotification(notification_wrappers[i])
    }


    function navHighlight() {
        var url = window.location.href.split('/')[window.location.href.split('/').length - 1];
        let ls = document.getElementsByClassName('nav-item');
        for (let i = 0; i < ls.length; i++) {
            if (ls[i].id.split('-')[1] === url) {
                ls[i].classList.add('active');
                return
            }
        }
    }

    navHighlight();


    let coll = document.getElementsByClassName("collapsible-btn");
    let i, j;

    function collapseAll(this_object = null) {
        for (j = 0; j < coll.length; j++) {
            if (this_object !== coll[j]) {

                if (coll[j].classList.contains('active')) {
                    coll[j].classList.remove('active');
                    let content = document.getElementById(coll[j].getAttribute('data-placeholder'));
                    if (content.style.maxHeight) {
                        content.style.maxHeight = null;
                        content.style.padding = null;
                    }
                }
            }
        }
    }

    let collcancel = document.getElementsByClassName('confirm-action-btn btn-cancel');

    for (let k = 0; k < collcancel.length; k++) {
        collcancel[k].addEventListener('click', function (event) {
            collapseAll()
        })

    }

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            collapseAll(this);
            this.classList.toggle("active");
            let content = document.getElementById(this.getAttribute('data-placeholder'));
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                content.style.padding = null;
            } else {
                content.style.padding = '5px';
                content.style.maxHeight = content.scrollHeight + "px";
                let ls_child = content.getElementsByClassName('input-group');
                for (j = 0; j < ls_child.length; j++) {
                    let inputs = ls_child[j].getElementsByTagName('input');
                    for (let k = 0; k < inputs.length; k++) {
                        inputFocus(inputs[k]);
                    }
                }
                setTimeout(function () {
                    content.style.maxHeight = 'fit-content';
                }, 300)
            }
        });
    }


    (function (d) {
        var
            ce = function (e, n) {
                var a = document.createEvent("CustomEvent");
                a.initCustomEvent(n, true, true, e.target);
                e.target.dispatchEvent(a);
                a = null;
                return false
            },
            nm = true,
            sp = {
                x: 0,
                y: 0
            },
            ep = {
                x: 0,
                y: 0
            },
            touch = {
                touchstart: function (e) {
                    sp = {
                        x: e.touches[0].clientX,
                        y: e.touches[0].clientY
                    }
                },
                touchmove: function (e) {
                    nm = false;
                    ep = {
                        x: e.touches[0].clientX,
                        y: e.touches[0].clientY
                    }
                },
                touchend: function (e) {
                    if (nm) {
                        ce(e, 'fc')
                    } else {
                        var x = ep.x - sp.x,
                            xr = Math.abs(x),
                            y = ep.y - sp.y,
                            yr = Math.abs(y);
                        try {
                            let helpnav = document.getElementById('help-nav').getBoundingClientRect();

                            if (sp.x / window.screen.availWidth >= 0.7 && xr / yr > 2 && sp.y >= helpnav.top - 20 && sp.y <= helpnav.bottom + 20) {
                                if (xr / x > 0) {
                                    hideHelp()
                                } else {
                                    showHelp()
                                }
                            }
                        } catch (e) {
                        }

                        if (xr / yr > 2 && xr > 120) {
                            ce(e, (x < 0 ? 'swl' : 'swr'))
                        } else if (yr / xr > 2) {
                            ce(e, (y < 0 ? 'swd' : 'swu'))
                        }
                    }
                    ;
                    nm = true
                },
                touchcancel: function (e) {
                    nm = false
                }
            };
        for (var a in touch) {
            d.addEventListener(a, touch[a], false);
        }
    })(document);


    if (document.getElementById("leftswipe") !== null) {
        document.body.addEventListener('swl', swipeLeft, false);
        document.body.addEventListener('swr', swipeRight, false);
    }
};


$(document).ready(function () {

});

$('#main').on('click', function () {
    closeNav();
})

function switchTab(target) {
    if (target) {
        if (target.classList.contains("active")) {
            return
        }
        let tab_links = document.getElementsByClassName("tab-link");
        for (let i = 0; i < tab_links.length; i++) {
            if (tab_links[i].classList.contains("active")) {
                closeTab(tab_links[i])
            }
        }
        showTab(target)
    }
}

function closeTab(target) {
    target.classList.remove("active");
    let child = document.getElementById(target.dataset.target);
    if (child) {
        child.classList.remove("show");
    }
}

function showTab(target) {
    let target_child = document.getElementById(target.dataset.target);
    if (target_child) {
        target.classList.add("active");
        target_child.classList.add("show");
    }
}

function initialTabSwitch() {
    let tab_links = document.getElementsByClassName("tab-link");
    if (tab_links && tab_links.length > 0) {
        switchTab(tab_links[0]);
    }
}


window.onscroll = function () {
    closeNav();
    let winWidth = window.innerWidth;
    let winHeight = window.innerHeight;
    let container_div = document.getElementById('container');
    let arrow_div = document.getElementById('arrow-up-nav');
    let blur_header = document.getElementById('blur-header');
    let container_up_arrow = document.getElementById('container_up_arrow');
    let notification_bar = document.getElementById('notification-div');
    let header_div = document.getElementById('header');
    let position = container_div.getBoundingClientRect().top;
    let currentPos = document.documentElement.scrollTop;
    var st = window.pageYOffset || document.documentElement.scrollTop;

    function animateScrolling(container, header, forward, container_position, page_position) {
        if (container_position > 0) {
            let coof = 0.3;
            let header_margin, container_margin;
            if (page_position < 0) {
                header_margin = '0';
                container_margin = '-50px';
            } else {
                header_margin = page_position * coof + 'px';
                container_margin = -50 - page_position * coof + 'px';
            }
            header.style.paddingTop = header_margin;
            container.style.marginTop = container_margin;
        }
    }

    // animateScrolling(container_div, header_div, lastScrollTop < st, position, currentPos);


    if (position <= 0 && !arrow_div.classList.contains('header_div')) {
        blur_header.classList.remove('hide');
        try {
            container_div.style.paddingTop = '50px';
        } catch (e) {

        }
        arrow_div.classList.add('smaller');
        arrow_div.classList.add('header_div');
        if (notification_bar) {
            notification_bar.classList.add('stick');
        }
    } else if (position >= 0 && arrow_div.classList.contains('header_div')) {
        blur_header.classList.add('hide');
        try {

            container_div.style.paddingTop = '0';
        } catch (e) {

        }
        arrow_div.classList.remove('header_div');
        arrow_div.classList.remove('smaller');
        if (notification_bar) {
            notification_bar.classList.remove('stick');
        }
    }
    if (position <= winHeight / 2) {
        if (container_up_arrow.classList.contains('reverse')) {
            container_up_arrow.classList.remove('reverse')
        }
    } else {
        if (!container_up_arrow.classList.contains('reverse')) {
            container_up_arrow.classList.add('reverse')
        }
    }

    if (currentPos <= 70 && document.getElementById('help-nav')) {
        showHelp()
    }

    checkHelp(lastScrollTop < st);
    lastScrollTop = st;


}


function checkHelp(forward) {
    let currentPos = document.documentElement.scrollTop;
    let helpnav = document.getElementById('help-nav');
    if (helpnav === null) {
        return
    }
    if (currentPos <= 70) {
        showHelp()
    } else if (helpnav.classList.contains('show')) {
        hideHelp()
    }
    let ls = document.getElementsByClassName('section');
    let current = header;
    let coof = 0.3;
    if (forward) {
        coof = 0.7;
    }
    for (let i = 0; i < ls.length; i++) {
        if (ls[i].getBoundingClientRect().top <= window.screen.availHeight * coof) {
            current = ls[i]
        }
    }
    lightONbutton(current);
}


function lightONbutton(element) {
    let ls = document.body.getElementsByClassName("help-nav-item");
    for (let i = 0; i < ls.length; i++) {
        if (element.id.split('-')[0] === ls[i].id) {
            if (!ls[i].classList.contains('active')) {
                ls[i].classList.add('active')
            }
        } else {
            if (ls[i].classList.contains('active')) {
                ls[i].classList.remove('active')
            }
        }

    }
}


function resizeTop() {
    let winHeight = window.innerHeight;
    let winWidth = window.innerWidth;
    if (winWidth <= 900) {
        document.getElementById('header').style.height = winHeight.toString() + 'px';
        // document.getElementById('header-text').style.lineHeight = (winHeight - 30).toString() + 'px';
    } else {
        document.getElementById('header').style.height = (winHeight * 0.7).toString() + 'px';
        // document.getElementById('header-text').style.lineHeight = (winHeight * 0.7).toString() + 'px';
    }
}

function hideHelp() {
    let helpnav = document.getElementById('help-nav');
    let winWidth = window.innerWidth;
    if (winWidth <= 900) {
        helpnav.style.marginRight = '-50px';
    }
    if (helpnav.classList.contains('show')) {
        helpnav.classList.remove('show')
    }
}

function showHelp() {
    let helpnav = document.getElementById('help-nav');
    if (helpnav.classList.contains('show')) {
        return
    }
    helpnav.style.marginRight = '0';
    helpnav.classList.add('show')

}

document.addEventListener("DOMContentLoaded", resizeTop);


function openNav() {
    let toogler = document.getElementById('nav-toogler');
    if (toogler.classList.contains('close')) {
        return
    } else {
        toogler.classList.add('close')
    }
    let mySidenav = document.getElementById("mySidenav");
    mySidenav.classList.add('show');
}

function closeNav() {
    let toogler = document.getElementById('nav-toogler');
    if (!toogler.classList.contains('close')) {
        return
    } else {
        toogler.classList.remove('close')
    }
    let mySidenav = document.getElementById("mySidenav");
    if (mySidenav.classList.contains('show')) {
        mySidenav.classList.remove('show')
    }
}

function toTheTop() {
    let reverse = document.getElementById('container_up_arrow').classList.contains('reverse');
    // console.log((window.innerHeight - document.documentElement.scrollTop)*0.3);
    if (!reverse) {
        $('html, body').animate({
            scrollTop: 0
        }, 300);
    } else {
        $('html, body').animate({
            scrollTop: $('#container').offset().top - (window.innerHeight - document.documentElement.scrollTop) * 0.2
        }, 300);
    }
}

function scrollToSection(id) {
    let targetPosition = $('#' + id).offset().top;
    $('html, body').animate({
        scrollTop: targetPosition - 40
    }, 300);
}


function filter_list(obj) {
    // close all open div
    let ls_obj = document.getElementsByClassName('table-data-full');
    for (let i = 0; i < ls_obj.length; i++) {
        let elem = ls_obj[i];
        if (elem.classList.contains('show')) {
            elem.classList.remove('show')
        }
    }
    let value = obj.value.toLowerCase();
    let selection_obj = document.getElementById('search-category');
    let category = selection_obj.options[selection_obj.selectedIndex].value;
    let ls_elements = document.getElementsByClassName('teacher-' + category);
    if (value !== "") {
        document.getElementById('table-teachers').style.display = 'table';
    } else {
        document.getElementById('table-teachers').style.display = 'none';
        document.getElementById('no-result').style.display = 'block';
        return
    }
    let find = false;
    for (let i = 1; i < ls_elements.length; i++) {
        let elem = ls_elements[i];
        if ((value === "") || !elem.innerText.toLowerCase().includes(value)) {
            let parent = elem.parentElement;
            parent.parentElement.style.display = 'none';
        } else {
            let parent = elem.parentElement;
            parent.parentElement.style.display = 'table-row';
            find = true;
        }
    }
    if (!find) {
        document.getElementById('no-result').style.display = 'block';
    } else {
        document.getElementById('no-result').style.display = 'none';
    }
}


function findOptionInput(elem) {
    let obj_id = elem.id;
    elem.parentElement.classList.add('bad');
    try {
        let ls_child = elem.parentElement.parentElement.getElementsByClassName('submit-btn');
        for (let i = 0; i < ls_child.length; i++) {
            ls_child[i].disabled = true;
        }
    } catch (e) {

    }
    let obj_value = elem.value.toLowerCase();
    if (obj_value === "") {
        obj_value = "lafdkjsdlfsdkjfsd;fdlkfjsdsl;dfksdjsdl;fsdkf";
    }
    let ls = document.getElementsByClassName('option-list-option');
    for (let i = 0; i < ls.length; i++) {
        if (ls[i].id.includes(obj_id)) {
            if (ls[i].textContent.toLowerCase().includes(obj_value)) {
                ls[i].classList.add('show');
            } else {
                ls[i].classList.remove('show');
            }
        }
    }
}


function hideAllOptionInput(className) {
    let ls = document.getElementsByClassName(className);
    for (let i = 0; i < ls.length; i++) {
        ls[i].classList.remove('show');
    }
}

function fillNewInput(elem) {

    let obj_id = elem.id;
    let value = elem.innerText;
    let teacher_id = obj_id.split('-')[obj_id.split('-').length - 1];
    let input_user = obj_id.split('-').slice(0, obj_id.split('-').length - 2).join('-');
    let input_hidden = input_user + '-hidden';
    document.getElementById(input_hidden).value = teacher_id;
    document.getElementById(input_user).value = value;
    document.getElementById(input_user).parentElement.classList.remove('bad');
    let ls_child = elem.parentElement.parentElement.getElementsByClassName('submit-btn');
    for (let i = 0; i < ls_child.length; i++) {
        ls_child[i].disabled = false;
    }
    hideAllOptionInput(elem.classList[0])

}


function showAdditionalInfo(obj) {
    let recieving_obj = document.getElementById(obj.id + '-additional');
    let ls_obj = document.getElementsByClassName('table-data-full');
    if (!recieving_obj.classList.contains('show')) {
        recieving_obj.classList.add('show');
        for (let i = 0; i < ls_obj.length; i++) {
            let elem = ls_obj[i];
            if (elem.id === recieving_obj.id) {
                continue
            }
            if (elem.classList.contains('show')) {
                elem.classList.remove('show')
            }
        }

    } else {
        recieving_obj.classList.remove('show');
    }
}

function showLogin() {
    let loginDiv = document.getElementById('login-div');
    if (!loginDiv.classList.contains('show')) {
        document.body.style.overflow = 'hidden';
        loginDiv.classList.add('show');
        setTimeout(function () {
            let loginContentDiv = document.getElementById('login-content-div');
            if (!loginContentDiv.classList.contains('show')) {
                loginContentDiv.classList.add('show');
            }
        }, 50);

    }
}


function hideLogin() {

    let loginContentDiv = document.getElementById('login-content-div');
    if (loginContentDiv.classList.contains('show')) {
        loginContentDiv.classList.remove('show');
        setTimeout(function () {
            let loginDiv = document.getElementById('login-div');
            if (loginDiv.classList.contains('show')) {
                document.body.removeAttribute('style');
                loginDiv.classList.remove('show');
            }
        }, 300);
    }

}

function hideCloseNav(elem) {
    if (elem.classList.contains('close')) {
        closeNav()
    } else {
        openNav()
    }
}

function hideNotification(wrapper) {
    wrapper.classList.remove("show");
    wrapper.classList.add("hide");
    setTimeout(function () {
        wrapper.parentNode.removeChild(wrapper)
    }, 1000);
}

function showTeacher(id) {
    let ls_elements = document.getElementsByClassName('teacher-data');
    for (let i = 0; i < ls_elements.length; i++) {
        ls_elements[i].style.display = 'none';
    }
    document.getElementById('table-teachers').style.display = 'table';
    document.getElementById('teacher-' + id).style.display = 'table-row';
    scrollToSection('teacher-' + id);
}

function inputFocus(elem) {
    elem.classList.add('focus');
}

function inputBlur(elem) {
    if (elem.value === "") {
        elem.classList.remove('focus');
    }
}

function changePlaceholder(elem) {
    document.getElementById('search-field-placeholder').setAttribute('data-placeholder', elem.options[elem.selectedIndex].innerText);
    filter_list(document.getElementById('search-field'))
}

function showIt(elem) {
    if (typeof elem === 'string') {
        elem = document.getElementById(elem)
    }
    if (elem.classList.contains('show')) {
        elem.classList.remove('show')
    } else {
        elem.classList.add('show')
    }
}