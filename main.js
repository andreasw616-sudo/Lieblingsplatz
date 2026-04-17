// Carousel Globals (für onclick-Zugriff)
let currentIndex = 0;
const images = [
    "groemitz/image00001.jpg",
    "groemitz/image00002.jpg",
    "groemitz/image00002_01.jpg",
    "groemitz/image00003.jpg",
    "groemitz/image00003_01.jpg",
    "groemitz/image00004.jpg",
    "groemitz/image00006.jpg",
    "groemitz/image00008.jpg",
    "groemitz/image00009_01.jpg",
    "groemitz/image00013_01.jpg",
    "groemitz/image00016.jpg",
    "groemitz/image00017-1.jpg",
    "groemitz/image00018_01-scaled.jpg",
    "groemitz/image00021_01-1.jpg",
    "groemitz/image00022_01.jpg",
    "groemitz/image00024.jpg",
    "groemitz/image00025_01.jpg",
    "groemitz/image00026_01.jpg",
    "groemitz/image00027.jpg",
    "groemitz/image00028-scaled.jpeg",
    "groemitz/image00030.jpg",
    "groemitz/image00032.jpg",
    "groemitz/image00033.jpg"
];

function showSlide(index) {
    const imgElement = document.getElementById('carousel-img');
    if (!imgElement) return;
    
    if (index < 0) index = images.length - 1;
    if (index >= images.length) index = 0;
    currentIndex = index;
    imgElement.src = images[index];
}

function nextSlide() {
    showSlide(currentIndex + 1);
}

function prevSlide() {
    showSlide(currentIndex - 1);
}

document.addEventListener('DOMContentLoaded', () => {
    // Touch/Swipe Logic
    const carousel = document.getElementById('carousel');
    if (carousel) {
        let touchStartX = 0;
        let touchEndX = 0;

        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        carousel.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            if (touchStartX - touchEndX > 50) nextSlide();
            if (touchEndX - touchStartX > 50) prevSlide();
        }, { passive: true });
    }

    // Mobile Navigation Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    if(mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            const nav = document.querySelector('.navbar-nav');
            if(nav) {
                if(nav.style.display === 'flex') {
                    nav.style.display = 'none';
                } else {
                    nav.style.display = 'flex';
                    nav.style.flexDirection = 'column';
                    nav.style.position = 'absolute';
                    nav.style.top = 'var(--navbar-height)';
                    nav.style.left = '0';
                    nav.style.width = '100%';
                    nav.style.backgroundColor = '#fff';
                    nav.style.padding = '1rem 0';
                    nav.style.boxShadow = '0 10px 10px rgba(0,0,0,0.1)';
                    nav.style.zIndex = '100';
                }
            }
        });
    }

    // Testimonials Logic
    const testiSlides = document.querySelectorAll('.testi-slide');
    const testiPrev = document.getElementById('testi-prev');
    const testiNext = document.getElementById('testi-next');
    let currentTesti = 0;

    if(testiSlides.length > 0 && testiPrev && testiNext) {
        const updateTesti = (index) => {
            testiSlides.forEach((slide, i) => {
                slide.style.display = i === index ? 'block' : 'none';
            });
        };

        testiPrev.addEventListener('click', () => {
            currentTesti = (currentTesti === 0) ? testiSlides.length - 1 : currentTesti - 1;
            updateTesti(currentTesti);
        });

        testiNext.addEventListener('click', () => {
            currentTesti = (currentTesti === testiSlides.length - 1) ? 0 : currentTesti + 1;
            updateTesti(currentTesti);
        });
    }

    // FAQ Accordion Logic
    const faqItems = document.querySelectorAll('.faq-item-new');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question-new');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all other items
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
                const otherAnswer = otherItem.querySelector('.faq-answer-new');
                if (otherAnswer) otherAnswer.style.display = 'none';
                const otherIcon = otherItem.querySelector('.faq-icon-new');
                if (otherIcon) otherIcon.textContent = '+';
            });
            
            // Toggle current item
            if (!isActive) {
                item.classList.add('active');
                const answer = item.querySelector('.faq-answer-new');
                if (answer) answer.style.display = 'block';
                const icon = item.querySelector('.faq-icon-new');
            }
        });
    });

    // Contact Form Logic
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success-new');

    if (contactForm && formSuccess) {
        contactForm.addEventListener('submit', (e) => {
            // Wir erlauben das standardmäßige Absenden via action="mailto:..."
            // Aber wir zeigen zusätzlich die Erfolgsmeldung an.
            
            setTimeout(() => {
                contactForm.style.display = 'none';
                formSuccess.style.display = 'block';
                formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 500);
        });
    }
});
