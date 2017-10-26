$(document).ready(function(){

    //pagetop
    var topBtn = $('#topIcon');
    topBtn.click(function(){
        $('body,html').animate({
            scrollTop: 0
        }, 500);
        return false;
    });

    //header 固定
    $(function(){
        var $header = $('header');
        $(window).scroll(function(){
            if ($(window).scrollTop() > 350) {
                $header.addClass('fixed');
            }else {
                $header.removeClass('fixed');
            }
        });
    });

    //drawer
    $(function(){
        $('.drawer').drawer();
     });

     //bxslider
    $(function(){
        $('.bxslider').bxSlider({
            auto: true
        });
        $('.bxslider-fade').bxSlider({
            auto: true,
            mode: 'fade',
            speed: 1000
        });
        $('.bxslider-fade-sp').bxSlider({
            auto: true,
            mode: 'fade',
            speed: 1000
        });
    });

    //move section
    $(function(){
        $('.move-about').on('click', function(){
            var targetTop = $('#about').offset().top;
            $('html,body').animate({
                scrollTop: targetTop
            }, 500);
            return false;
        });
        $('.move-how').on('click', function(){
            var targetTop = $('#how').offset().top;
            $('html,body').animate({
                scrollTop: targetTop
            }, 500);
            return false;
        });
        $('.move-member').on('click', function(){
            var targetTop = $('#member').offset().top;
            $('html,body').animate({
                scrollTop: targetTop
            }, 500);
            return false;
        });
        $('.move-recruit').on('click', function(){
            var targetTop = $('#recruit').offset().top;
            $('html,body').animate({
                scrollTop: targetTop
            }, 500);
            return false;
        });
    });

    //enter submit
    function go(){
        //EnterキーならSubmit code: 13
        if(window.event.keyCode==13)document.formdx.submit();
    }
    //mobile
    var $win = $(window);
    $win.on('load resize', function(){
        var windowWidth = window.innerWidth;
        if (windowWidth > 960) {
            //fadein
            $(function(){
                $(window).scroll(function (){
                    $('.fadein').each(function(){
                        var elemPos = $(this).offset().top;
                        var scroll = $(window).scrollTop();
                        var windowHeight = $(window).height();
                        var windowWidth = $(window).width();
                        if (scroll > elemPos - windowHeight + 200) {
                            $(this).addClass('scrollin');
                        }
                    });
                });
            });
        }
    });
});
