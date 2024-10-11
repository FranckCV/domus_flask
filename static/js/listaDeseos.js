let $square = $('.square'),
$span = $('.circle-expand'),
$modal = $('.modal'),
$close = $('.close')

var shape = new mojs.Shape({
  shape: 'circle',
  isShowStart:  true,
  fill: '#9DC3C2',
  opacity: {0:1},
  stroke: '#FFF',
  strokeWidth:  0,
  duration: 300,
  delay: 0
}).then({
  scale: { 0.5 : 40 },
  duration: 500,
});


$square.click((e) => {
  $square.addClass('active');        
  shape.play();
  $modal.addClass('active')
})

$close.click(function() {
  $modal.removeClass('active');
  shape.playBackward();
  $square.removeClass('active');  
})