/**
 * Main JavaScript for Elvis T. Harmon Portfolio
 */

document.addEventListener('DOMContentLoaded', function() {

    // ========================================
    // 1. Dark Mode Toggle
    // ========================================
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.className = 'fas fa-moon';
    }

    // Toggle theme
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            themeIcon.className = 'fas fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeIcon.className = 'fas fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    });

    // ========================================
    // 2. Smooth Scroll
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ========================================
    // 3. Navbar Active State
    // ========================================
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ========================================
    // 4. Navbar Shrink on Scroll
    // ========================================
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > 50) {
            navbar.style.boxShadow = '0 2px 20px var(--shadow-color)';
            navbar.style.padding = '10px 0';
        } else {
            navbar.style.boxShadow = '0 1px 3px var(--shadow-color)';
            navbar.style.padding = '16px 0';
        }

        lastScroll = currentScroll;
    });

    // ========================================
    // 5. Counter Animation (Enhanced)
    // ========================================
    const counters = document.querySelectorAll('.stat-number');

    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const startTime = performance.now();
        const startValue = 0;

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.round(easeOutQuart * target);

            counter.textContent = currentValue + (target > 0 ? '+' : '');

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + (target > 0 ? '+' : '');
            }
        };

        requestAnimationFrame(updateCounter);
    };

    // Intersection Observer for counters
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                animateCounter(counter);
                observer.unobserve(counter);
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });

    // ========================================
    // 6. Back to Top Button with Animation
    // ========================================
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.className = 'btn btn-primary btn-lg position-fixed';
    backToTop.style.cssText = `
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        z-index: 1000;
        padding: 0;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.3);
        transition: all 0.3s ease;
    `;
    document.body.appendChild(backToTop);

    // Add hover effect
    backToTop.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.05)';
        this.style.boxShadow = '0 8px 30px rgba(108, 99, 255, 0.4)';
    });

    backToTop.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
        this.style.boxShadow = '0 4px 20px rgba(108, 99, 255, 0.3)';
    });

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 500) {
            backToTop.style.display = 'block';
            backToTop.style.animation = 'fadeInUp 0.3s ease forwards';
        } else {
            backToTop.style.display = 'none';
        }
    });

    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ========================================
    // 7. Parallax Effect on Hero
    // ========================================
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            heroSection.style.backgroundPositionY = rate + 'px';
        });
    }

    // ========================================
    // 8. Card Hover Effect Enhancement    // ========================================
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ========================================
    // 9. Tech Badge Interactive Effect
    // ========================================
    document.querySelectorAll('.tech-badge').forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.1)';
        });
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    console.log('🚀 Elvis T. Harmon Portfolio loaded successfully!');
});

// ========================================
// 10. Form Validation Helpers
// ========================================
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    return alertDiv;
}

// ========================================
// 11. Intersection Observer for Fade Animations
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
                animationObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animateElements.forEach(el => {
        animationObserver.observe(el);
    });
});