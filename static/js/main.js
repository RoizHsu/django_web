// Main JavaScript file for Django Web Application

document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Web Application loaded successfully!');

    // Handle contact form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };

            // Display success message
            alert(`感謝您的訊息！\n\n姓名：${formData.name}\n電子郵件：${formData.email}\n訊息：${formData.message}\n\n我們會盡快回覆您。`);
            
            // Reset form
            contactForm.reset();
        });
    }

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add active class to current nav link
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation || 
            (currentLocation === '/' && link.getAttribute('href').includes('home'))) {
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
        }
    });
});
