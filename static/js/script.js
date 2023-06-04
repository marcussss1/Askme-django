(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // Для этих методов токен не будет подставляться в заголовок
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    bsCustomFileInput.init();
    $('.toast').toast();
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    });

    ----------------------- ПРЕДПРОСМОТР АВЫ -----------------------------------
    $("#id_avatar").on('change',function(){
        var input = $(this)[0];
        var reader = new FileReader();
        reader.readAsDataURL(input.files[0]);
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
        }
    });

    ----------------------------- ПОСТ ----------------------------------------
    $(".rating button").on('click', function(){
        let b = $(this);
        const id = b.attr('id').substr(1);
        const vote = b.attr('id')[0] === 'l' ? 1 : -1;

        $(b).prop('disabled', true);

        $.ajax({
            url : "/like/",
            type : "POST",
            data : { id : id,
                     action: vote },

            success : function(json) {
                $('#q' + id).text(json['new_rating']);

                let sibling_btn = vote > 0 ? 'd' + id : 'l' + id;
                $('#' + sibling_btn).prop('disabled', false);
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $(b).prop('disabled', false);
            }
        });
    });

    // ----------------------------- КОММЕНТ ----------------------------------------
    $(".сrating button").on('click', function(){
        let b = $(this);
        const id = b.attr('id').substr(1);
        const vote = b.attr('id')[0] === 'l' ? 1 : -1;

        $(b).prop('disabled', true);

        $.ajax({
            url : "/clike/",
            type : "POST",
            data : { id : id,
                     action: vote },

            success : function(json) {
                $('#c' + id).text(json['new_rating']);

                let sibling_btn = vote > 0 ? 'd' + id : 'l' + id;
                $('#' + sibling_btn).prop('disabled', false);
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $(b).prop('disabled', false);
            }
        });
    });

    // ----------------------------- ВЕРНЫЙ КОММЕНТ ----------------------------------------
    $(".correct-answer ").on('change', 'input[type="checkbox"]', function(){
        $('.correct-answer input').each(function () {
            $(this).prop('disabled', true)
        });

        const com_id = $(this).attr('id').replace('CorrectAnswer', '');
        const post_id = $("[id^='q']").attr('id').substr(1);

        $.ajax({
            url : "/ransw/",
            type : "POST",
            data : { question_id : post_id,
                     answer_id: com_id },

            success : function(json) {
                $('.correct-answer #CorrectAnswer' + com_id).parent().parent().parent().addClass('right-comment').html();
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $('.correct-answer input').each(function () {
                    $(this).prop('disabled', false)
                });
            }
        });
    });


    $('form').submit(function () {
        $('.spinner-border').show();
        $('input[type="submit"]').attr('disabled', true);
        return true;
    })
});




(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // Для этих методов токен не будет подставляться в заголовок
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    bsCustomFileInput.init();
    $('.toast').toast();
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    });

    ----------------------- ПРЕДПРОСМОТР АВЫ -----------------------------------
    $("#id_avatar").on('change',function(){
        var input = $(this)[0];
        var reader = new FileReader();
        reader.readAsDataURL(input.files[0]);
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
        }
    });

    ----------------------------- ПОСТ ----------------------------------------
    $(".rating button").on('click', function(){
        let b = $(this);
        const id = b.attr('id').substr(1);
        const vote = b.attr('id')[0] === 'l' ? 1 : -1;

        $(b).prop('disabled', true);

        $.ajax({
            url : "/like/",
            type : "POST",
            data : { id : id,
                     action: vote },

            success : function(json) {
                $('#q' + id).text(json['new_rating']);

                let sibling_btn = vote > 0 ? 'd' + id : 'l' + id;
                $('#' + sibling_btn).prop('disabled', false);
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $(b).prop('disabled', false);
            }
        });
    });

    // ----------------------------- КОММЕНТ ----------------------------------------
    $(".сrating button").on('click', function(){
        let b = $(this);
        const id = b.attr('id').substr(1);
        const vote = b.attr('id')[0] === 'l' ? 1 : -1;

        $(b).prop('disabled', true);

        $.ajax({
            url : "/clike/",
            type : "POST",
            data : { id : id,
                     action: vote },

            success : function(json) {
                $('#c' + id).text(json['new_rating']);

                let sibling_btn = vote > 0 ? 'd' + id : 'l' + id;
                $('#' + sibling_btn).prop('disabled', false);
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $(b).prop('disabled', false);
            }
        });
    });

    // ----------------------------- ВЕРНЫЙ КОММЕНТ ----------------------------------------
    $(".correct-answer ").on('change', 'input[type="checkbox"]', function(){
        $('.correct-answer input').each(function () {
            $(this).prop('disabled', true)
        });

        const com_id = $(this).attr('id').replace('CorrectAnswer', '');
        const post_id = $("[id^='q']").attr('id').substr(1);

        $.ajax({
            url : "/ransw/",
            type : "POST",
            data : { question_id : post_id,
                     answer_id: com_id },

            success : function(json) {
                $('.correct-answer #CorrectAnswer' + com_id).parent().parent().parent().addClass('right-comment').html();
            },

            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                $('.toast').filter('.error').toast('show');
                $('.correct-answer input').each(function () {
                    $(this).prop('disabled', false)
                });
            }
        });
    });


    $('form').submit(function () {
        $('.spinner-border').show();
        $('input[type="submit"]').attr('disabled', true);
        return true;
    })
});



