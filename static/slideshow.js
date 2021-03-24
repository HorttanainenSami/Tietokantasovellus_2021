<script>
var slideIndex = [];
var slideId = [];
for(i = 1; i<={{images|length}};i++){
    slideIndex.push(1);
    slideId.push("mySlides"+i)
    showSlides(1,i-1);
  }
function plusSlides(n, no) {
  showSlides(slideIndex[no] += n, no);
}

function showSlides(n, no) {
  var i;
  var x = document.getElementsByClassName(slideId[no]);
  if (n > x.length) {slideIndex[no] = 1}    
  if (n < 1) {slideIndex[no] = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
  }
  if(x.length ==0){
    return;
  }
  x[slideIndex[no]-1].style.display = "block";  
}
</script>
