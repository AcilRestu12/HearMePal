function typeEffect(element, speed, callback) {
    var text = element.innerHTML;
    element.innerHTML = "";

    var i = 0;
    var timer = setInterval(function() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
            if (callback) {
                callback(); // Call the next animation if provided
            }
        }
    }, speed);
}

function animateElements(elements, speed) {
    if (elements.length === 0) return; // No more elements to animate

    var element = elements[0];
    var delay = 20 * speed + speed;

    setTimeout(function() {
        element.style.display = "inline-block";
        typeEffect(element, speed, function() {
            // Animate the next element after the current one finishes
            animateElements(elements.slice(1), speed);
        });
    }, delay);
}

document.addEventListener('DOMContentLoaded', function() {
    var speed = 75;
    var elements = Array.from(document.querySelectorAll('.type-effect'));

    animateElements(elements, speed);
});




// Original
// function typeEffect(element, speed) {
//     var text = element.innerHTML;
//     element.innerHTML = "";

//     var i = 0;
//     var timer = setInterval(function() {
//         if (i < text.length) {
//             element.append(text.charAt(i));
//             i++;
//         } else {
//             clearInterval(timer);
//         }
//     }, speed);
// }

// var speed = 75;
// var p = document.querySelector('.type-effect');
// var delay = 20 * speed + speed;

// setTimeout(function() {
//     p.style.display = "inline-block";
//     typeEffect(p, speed);
// }, delay);




