document.querySelectorAll('.button').forEach(function(button) {
    button.addEventListener('mouseenter', function() {
        // Воспроизводим звук
        document.getElementById('buttonSound').play();
    });
    button.addEventListener('mouseleave', function() {
        // Останавливаем звук, если нужно
        document.getElementById('buttonSound').currentTime = 0;
        document.getElementById('buttonSound').pause();
    });
});