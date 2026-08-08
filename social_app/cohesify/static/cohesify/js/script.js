function expand_side_bar() {
    document.querySelector('.content').classList.add('content-expanded-sidebar');
    document.querySelectorAll('.side-bar-button').forEach(function(btn) {
        btn.classList.add('side-bar-button-expanded')
    });
}

function collapse_side_bar() {
    document.querySelector('.content').classList.remove('content-expanded-sidebar');
    document.querySelectorAll('.side-bar-button').forEach(function(btn) {
        btn.classList.remove('side-bar-button-expanded')
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const side_bar = document.querySelector('#side-bar');
    side_bar.addEventListener('mouseenter', function() {
        expand_side_bar();
    });
    side_bar.addEventListener('mouseleave', function() {
        collapse_side_bar();
    });

    const home_button = document.querySelector('#home_button');
    const home_redirect_link = home_button.dataset.redirectLink;
    home_button.addEventListener('click', function() {
        window.location.href = home_redirect_link;
    });

    const logout_button = document.querySelector('#logout_button');
    const logout_url = logout_button.dataset.logoutUrl;
    logout_button.addEventListener('click', function() {
        window.location.href = logout_url;
    });

    const logo = document.querySelector('#logo');
    const logo_redirect_link = logo.dataset.redirectLink;
    logo.addEventListener('click', function() {
        window.location.href = logo_redirect_link;
    });

    const friends_button = document.querySelector('#friends_button');
    const friends_redirect_link = friends_button.dataset.redirectLink;
    friends_button.addEventListener('click', function() {
        window.location.href = friends_redirect_link;
    });

    const profile_button = document.querySelector('#profile_button');
    const profile_redirect_link = profile_button.dataset.redirectLink;
    profile_button.addEventListener('click', function() {
        window.location.href = profile_redirect_link;
    });

    const filter_form = document.querySelector('#filter_form');
    if (filter_form) {
        filter_form.addEventListener('change', function() {
            filter_form.submit();
        });
    }

    // Disable empty submissions in search bar
    const search_bar_keyword = document.querySelector('#search_bar_keyword');
    const search_bar_submit = document.querySelector('#search_bar_submit');
    search_bar_submit.disabled = true;
    search_bar_keyword.onkeyup = function() {
        if (search_bar_keyword.value.length > 0) {
            search_bar_submit.disabled = false;
        } else {
            search_bar_submit.disabled = true;
        }
    }

    // Disable empty submissions in comments
    const text_field = document.querySelector('#comment_text');
    const submit_button = document.querySelector('#comment_submit');
    if (text_field && submit_button) {
        submit_button.disabled = true;
        text_field.onkeyup = function() {
            if (text_field.value.length > 0) {
                submit_button.disabled = false;
            } else {
                submit_button.disabled = true;
            }
        }
    }

    document.querySelectorAll('.post_video').forEach( function(video) {
        video.addEventListener('click', function() {
            if (video.controls == true) {
                video.controls = false;
            } else {
                video.controls = true;
            }
            if (video.muted == true) {
                video.muted = false;
            } else {
                video.muted = true;
            }
            video.play();
        });
    });
});