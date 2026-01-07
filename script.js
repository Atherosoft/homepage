document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#contact') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Simple scroll reveal animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.feature-card, .hero-text, .section-header').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });

    // Modal functionality
    const modal = document.getElementById('contactModal');
    const closeBtn = document.getElementById('closeModal');
    const contactForm = document.getElementById('contactForm');
    const formSuccess = document.getElementById('formSuccess');

    // Close modal when clicking X or outside
    closeBtn.addEventListener('click', closeContactModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeContactModal();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeContactModal();
        }
    });

    // About page navigation active state
    const aboutNavLinks = document.querySelectorAll('.about-nav-link');
    if (aboutNavLinks.length > 0) {
        const sections = ['team', 'publications', 'history'];
        
        function updateActiveNav() {
            const scrollPosition = window.scrollY + 150;
            
            sections.forEach((sectionId, index) => {
                const section = document.getElementById(sectionId);
                if (section) {
                    const sectionTop = section.offsetTop;
                    const sectionBottom = sectionTop + section.offsetHeight;
                    const link = aboutNavLinks[index];
                    
                    if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                        aboutNavLinks.forEach(l => l.classList.remove('active'));
                        link.classList.add('active');
                    }
                }
            });
        }
        
        window.addEventListener('scroll', updateActiveNav);
        updateActiveNav(); // Initial check
    }

    // Form submission
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(contactForm);

        try {
            const response = await fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                contactForm.style.display = 'none';
                formSuccess.style.display = 'block';

                setTimeout(() => {
                    closeContactModal();
                    contactForm.style.display = 'block';
                    formSuccess.style.display = 'none';
                    contactForm.reset();
                }, 3000);
            } else {
                alert('Oops! There was a problem submitting your form. Please try again.');
            }
        } catch (error) {
            alert('Oops! There was a problem submitting your form. Please try again.');
        }
    });
});

// Global functions for modal control
function openContactModal() {
    const modal = document.getElementById('contactModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeContactModal() {
    const modal = document.getElementById('contactModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}
