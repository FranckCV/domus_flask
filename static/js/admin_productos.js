document.getElementById('toggleBtn').addEventListener('click', function() {
    const aside = document.getElementById('myAside');
    const section = document.getElementById('mainSection');
    aside.classList.toggle('active'); 
    section.classList.toggle('shift'); 
});