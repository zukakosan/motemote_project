$(document).ready(function(){
//pagetop
    var topBtn = $('#topIcon');
    topBtn.click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 500);
        return false;
    });
});
//ジャンル移動
$(function(){
    $('#move_genre').on('click', function(){
        var targetTop = $('#top_form').offset().top;
        $('html,body').animate({
            scrollTop: targetTop
        }, 500);
        return false;
    });
});

$(document).ready(function() {
  $(".drawer").drawer();
});

$(function(){
  $('.content_box .content_txt, .content_box .en_box').css("opacity","0");
  $(window).scroll(function (){
    $(".content_box").each(function(){
      var imgPos = $(this).offset().top;
      var scroll = $(window).scrollTop();
      var windowHeight = $(window).height();
      if (scroll > imgPos - windowHeight + windowHeight/1.5){
        $(".en_box, .content_txt",this).css("opacity","1" );
        $(".en_box",this).css({
          "font-size": "100px",
          "padding": "0 20px 40px"
        });
      }
    });
  });
});

$(function(){
    $('.fade').hide();
});

var i = 0;
var int=0;

$(window).bind("load", function() {
    var int=setInterval("doFade(i)",200);
});

function doFade() {
    var list = $('.fade').length;
    if (i >= list) {
        clearInterval(int);
    }
    $('.fade').eq(i).fadeIn(1500);
        i++;
}
