document.addEventListener('DOMContentLoaded', () => {
    // Carousel Logic
    const carouselTrack = document.getElementById('image-carousel');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');

    if(carouselTrack && prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            const width = carouselTrack.clientWidth;
            carouselTrack.scrollBy({ left: -width, behavior: 'smooth' });
        });

        nextBtn.addEventListener('click', () => {
            const width = carouselTrack.clientWidth;
            carouselTrack.scrollBy({ left: width, behavior: 'smooth' });
        });
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
