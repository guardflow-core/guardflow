// GuardFlow SaaS - Interactive JavaScript

// DOM Elements
const header = document.getElementById('header');
const navLinks = document.querySelectorAll('.nav-link');
const roiCalculator = document.getElementById('roi-calculator');
const roiResult = document.getElementById('roi-result');

// Smooth scrolling for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        if (targetId.startsWith('#')) {
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Header scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ROI Calculator Enhanced
function calculateROI() {
    const revenue = parseFloat(document.getElementById('revenue').value) || 0;
    const checkouts = parseInt(document.getElementById('checkouts').value) || 0;
    const employees = parseInt(document.getElementById('employees').value) || 0;
    const salary = parseFloat(document.getElementById('salary').value) || 0;
    
    // Calculate savings
    const monthlySalaryCost = checkouts * employees * salary;
    const annualSalaryCost = monthlySalaryCost * 12;
    const savings = annualSalaryCost * 0.4; // 40% reduction in operational costs
    
    // Calculate additional revenue from increased conversion
    const conversionIncrease = revenue * 0.25; // 25% increase in conversion
    const annualConversionIncrease = conversionIncrease * 12;
    
    // Total ROI
    const totalROI = savings + annualConversionIncrease;
    
    // Update result
    roiResult.textContent = `R$ ${totalROI.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    
    // Update breakdown
    const salarySavings = document.getElementById('salary-savings');
    const revenueIncrease = document.getElementById('revenue-increase');
    const totalROIElement = document.getElementById('total-roi');
    
    if (salarySavings) {
        salarySavings.textContent = `R$ ${savings.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
    
    if (revenueIncrease) {
        revenueIncrease.textContent = `R$ ${annualConversionIncrease.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
    
    if (totalROIElement) {
        totalROIElement.textContent = `R$ ${totalROI.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
    
    // Add animation
    roiResult.style.transform = 'scale(1.1)';
    setTimeout(() => {
        roiResult.style.transform = 'scale(1)';
    }, 200);
    
    // Track ROI calculation for analytics
    gtag('event', 'roi_calculated', {
        'event_category': 'engagement',
        'event_label': 'roi_calculator',
        'value': totalROI
    });
}

// ROI Calculator event listeners
if (roiCalculator) {
    const inputs = roiCalculator.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', calculateROI);
    });
    
    // Initial calculation
    calculateROI();
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fadeInUp');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.card, .feature-card, .testimonial-card, .pricing-card').forEach(el => {
    observer.observe(el);
});

// Demo video interaction
const demoVideo = document.querySelector('.demo-video');
if (demoVideo) {
    demoVideo.addEventListener('click', () => {
        // Add demo interaction logic here
        demoVideo.innerHTML = `
            <div class="demo-content">
                <h3 class="text-2xl font-bold mb-4">Demo Interativa</h3>
                <p class="mb-4">Simulação do GuardFlow em ação:</p>
                <div class="demo-steps">
                    <div class="step">
                        <i class="fas fa-qrcode text-primary-500"></i>
                        <span>1. Cliente escaneia produtos</span>
                    </div>
                    <div class="step">
                        <i class="fas fa-brain text-success"></i>
                        <span>2. IA valida e calcula preço</span>
                    </div>
                    <div class="step">
                        <i class="fas fa-leaf text-secondary-500"></i>
                        <span>3. ESG score automático</span>
                    </div>
                    <div class="step">
                        <i class="fas fa-credit-card text-accent-500"></i>
                        <span>4. Pagamento instantâneo</span>
                    </div>
                </div>
            </div>
        `;
    });
}

// Market Capture Form - Advanced Lead Scoring
const marketForm = document.querySelector('#market-form');
if (marketForm) {
    marketForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(marketForm);
        const data = Object.fromEntries(formData);
        
        // Validate required fields
        const requiredFields = ['name', 'position', 'email', 'phone', 'company', 'segment', 'stores', 'revenue', 'checkouts', 'urgency'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            showNotification('Por favor, preencha todos os campos obrigatórios.', 'error');
            return;
        }
        
        // Advanced Lead Scoring Algorithm
        let leadScore = 0;
        let leadCategory = 'low';
        let priority = 'low';
        
        // Revenue scoring (0-40 points)
        const revenueScores = {
            '0-100k': 5,
            '100k-500k': 10,
            '500k-1M': 20,
            '1M-5M': 30,
            '5M-10M': 35,
            '10M+': 40
        };
        leadScore += revenueScores[data.revenue] || 0;
        
        // Store count scoring (0-20 points)
        const storeScores = {
            '1': 5,
            '2-5': 10,
            '6-20': 15,
            '21-50': 18,
            '50+': 20
        };
        leadScore += storeScores[data.stores] || 0;
        
        // Checkout count scoring (0-15 points)
        const checkoutScores = {
            '1-5': 5,
            '6-10': 8,
            '11-20': 12,
            '21-50': 14,
            '50+': 15
        };
        leadScore += checkoutScores[data.checkouts] || 0;
        
        // Urgency scoring (0-15 points)
        const urgencyScores = {
            'immediate': 15,
            'short': 10,
            'medium': 5,
            'long': 2
        };
        leadScore += urgencyScores[data.urgency] || 0;
        
        // Position scoring (0-10 points)
        const positionScores = {
            'ceo': 10,
            'cto': 8,
            'operations': 6,
            'finance': 5,
            'marketing': 4,
            'other': 2
        };
        leadScore += positionScores[data.position] || 0;
        
        // Budget scoring (0-10 points)
        const budgetScores = {
            '5k-10k': 2,
            '10k-25k': 4,
            '25k-50k': 6,
            '50k-100k': 8,
            '100k+': 10,
            'discuss': 5
        };
        leadScore += budgetScores[data.budget] || 0;
        
        // Challenge count bonus (0-10 points)
        const challenges = formData.getAll('challenges');
        leadScore += Math.min(challenges.length * 2, 10);
        
        // Determine lead category and priority
        if (leadScore >= 80) {
            leadCategory = 'high';
            priority = 'immediate';
        } else if (leadScore >= 60) {
            leadCategory = 'medium';
            priority = 'high';
        } else if (leadScore >= 40) {
            leadCategory = 'medium';
            priority = 'medium';
        } else {
            leadCategory = 'low';
            priority = 'low';
        }
        
        // Create comprehensive lead data
        const leadData = {
            // Personal info
            name: data.name,
            position: data.position,
            email: data.email,
            phone: data.phone,
            
            // Company info
            company: data.company,
            cnpj: data.cnpj,
            segment: data.segment,
            stores: data.stores,
            current_system: data.current_system,
            
            // Commercial info
            revenue: data.revenue,
            checkouts: data.checkouts,
            urgency: data.urgency,
            budget: data.budget,
            challenges: challenges,
            
            // Lead scoring
            leadScore: leadScore,
            leadCategory: leadCategory,
            priority: priority,
            
            // Additional info
            source: data.source,
            message: data.message || '',
            timestamp: new Date().toISOString(),
            formType: 'market_capture'
        };
        
        // Store lead data
        const existingLeads = JSON.parse(localStorage.getItem('guardflow_leads') || '[]');
        existingLeads.push(leadData);
        localStorage.setItem('guardflow_leads', JSON.stringify(existingLeads));
        
        // Track advanced analytics
        gtag('event', 'market_lead_generated', {
            'event_category': 'conversion',
            'event_label': 'market_capture_form',
            'value': leadScore,
            'custom_parameters': {
                'company': data.company,
                'segment': data.segment,
                'revenue_range': data.revenue,
                'lead_category': leadCategory,
                'priority': priority,
                'challenges_count': challenges.length
            }
        });
        
        // Show success message with detailed feedback
        let successMessage = `Lead ${leadCategory.toUpperCase()} qualificado! `;
        if (leadCategory === 'high') {
            successMessage += 'Nossa equipe entrará em contato em até 2 horas.';
        } else if (leadCategory === 'medium') {
            successMessage += 'Entraremos em contato em até 24 horas.';
        } else {
            successMessage += 'Entraremos em contato em até 48 horas.';
        }
        
        showNotification(successMessage, 'success');
        marketForm.reset();
        
        // Track conversion with lead score
        gtag('event', 'conversion', {
            'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
            'value': leadScore,
            'currency': 'BRL'
        });
        
        // Track form completion
        trackEngagement('market_form_completed', `score_${leadScore}_category_${leadCategory}`);
    });
}

// Enhanced Form validation and submission with lead scoring
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // Validate form
        if (!data.name || !data.email || !data.company) {
            showNotification('Por favor, preencha todos os campos obrigatórios.', 'error');
            return;
        }
        
        // Calculate lead score based on revenue
        let leadScore = 0;
        const revenue = data.revenue;
        if (revenue === '1M-5M') leadScore = 80;
        else if (revenue === '5M+') leadScore = 100;
        else if (revenue === '500k-1M') leadScore = 60;
        else if (revenue === '100k-500k') leadScore = 40;
        else leadScore = 20;
        
        // Track lead generation
        gtag('event', 'lead_generated', {
            'event_category': 'conversion',
            'event_label': 'contact_form',
            'value': leadScore,
            'custom_parameters': {
                'company': data.company,
                'revenue_range': revenue
            }
        });
        
        // Store lead data locally (in real implementation, send to CRM)
        const leadData = {
            name: data.name,
            email: data.email,
            company: data.company,
            revenue: revenue,
            message: data.message || '',
            leadScore: leadScore,
            timestamp: new Date().toISOString(),
            source: 'landing_page'
        };
        
        // Store in localStorage for demo purposes
        const existingLeads = JSON.parse(localStorage.getItem('guardflow_leads') || '[]');
        existingLeads.push(leadData);
        localStorage.setItem('guardflow_leads', JSON.stringify(existingLeads));
        
        // Show success message with lead score
        showNotification(`Lead qualificado com score ${leadScore}! Entraremos em contato em breve.`, 'success');
        contactForm.reset();
        
        // Track conversion
        gtag('event', 'conversion', {
            'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
            'value': leadScore,
            'currency': 'BRL'
        });
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');

if (mobileMenuToggle && mobileMenu) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Typing animation for hero title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing animation when page loads
window.addEventListener('load', () => {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        typeWriter(heroTitle, originalText, 50);
    }
});

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Animate counters when they come into view
const statNumbers = document.querySelectorAll('.stat-number');
const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.textContent.replace(/[^\d]/g, ''));
            animateCounter(entry.target, target);
            statObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

statNumbers.forEach(stat => {
    statObserver.observe(stat);
});

// Pricing card hover effects
const pricingCards = document.querySelectorAll('.pricing-card');
pricingCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
});

// Feature card hover effects
const featureCards = document.querySelectorAll('.feature-card');
featureCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px)';
        card.style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.25)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
    });
});

// Lazy loading for images
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
        }
    });
});

images.forEach(img => {
    imageObserver.observe(img);
});

// Performance monitoring
const performanceObserver = new PerformanceObserver((list) => {
    list.getEntries().forEach(entry => {
        if (entry.entryType === 'navigation') {
            console.log('Page load time:', entry.loadEventEnd - entry.loadEventStart, 'ms');
        }
    });
});

performanceObserver.observe({ entryTypes: ['navigation'] });

// Error handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    // You could send this to an error tracking service
});

// Service Worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Initialize all animations and interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add loading states
    document.body.classList.add('loaded');
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', (e) => {
            const tooltipText = e.target.dataset.tooltip;
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'tooltip';
            tooltipElement.textContent = tooltipText;
            tooltipElement.style.cssText = `
                position: absolute;
                background: #1f2937;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 14px;
                z-index: 1000;
                pointer-events: none;
            `;
            document.body.appendChild(tooltipElement);
            
            const rect = e.target.getBoundingClientRect();
            tooltipElement.style.left = rect.left + rect.width / 2 - tooltipElement.offsetWidth / 2 + 'px';
            tooltipElement.style.top = rect.top - tooltipElement.offsetHeight - 8 + 'px';
        });
        
        tooltip.addEventListener('mouseleave', () => {
            const tooltipElement = document.querySelector('.tooltip');
            if (tooltipElement) {
                tooltipElement.remove();
            }
        });
    });
});

// Lead Management and Analytics
function getLeadStats() {
    const leads = JSON.parse(localStorage.getItem('guardflow_leads') || '[]');
    const stats = {
        total: leads.length,
        highValue: leads.filter(l => l.leadScore >= 80).length,
        mediumValue: leads.filter(l => l.leadScore >= 40 && l.leadScore < 80).length,
        lowValue: leads.filter(l => l.leadScore < 40).length,
        totalValue: leads.reduce((sum, l) => sum + l.leadScore, 0)
    };
    return stats;
}

// Track user engagement
function trackEngagement(action, element) {
    gtag('event', 'engagement', {
        'event_category': 'user_interaction',
        'event_label': action,
        'value': 1
    });
    
    // Store engagement data
    const engagement = {
        action: action,
        element: element,
        timestamp: new Date().toISOString(),
        page: window.location.pathname
    };
    
    const existingEngagements = JSON.parse(localStorage.getItem('guardflow_engagement') || '[]');
    existingEngagements.push(engagement);
    localStorage.setItem('guardflow_engagement', JSON.stringify(existingEngagements));
}

// Track scroll depth
let maxScrollDepth = 0;
window.addEventListener('scroll', () => {
    const scrollDepth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    if (scrollDepth > maxScrollDepth) {
        maxScrollDepth = scrollDepth;
        if (maxScrollDepth >= 25 && maxScrollDepth < 50) {
            trackEngagement('scroll_25', 'page');
        } else if (maxScrollDepth >= 50 && maxScrollDepth < 75) {
            trackEngagement('scroll_50', 'page');
        } else if (maxScrollDepth >= 75) {
            trackEngagement('scroll_75', 'page');
        }
    }
});

// Track time on page
let startTime = Date.now();
window.addEventListener('beforeunload', () => {
    const timeOnPage = Math.round((Date.now() - startTime) / 1000);
    gtag('event', 'time_on_page', {
        'event_category': 'engagement',
        'event_label': 'page_time',
        'value': timeOnPage
    });
});

// Track button clicks
document.addEventListener('click', (e) => {
    if (e.target.matches('a[href^="#"]')) {
        trackEngagement('internal_link_click', e.target.href);
    } else if (e.target.matches('.btn')) {
        trackEngagement('button_click', e.target.textContent.trim());
    } else if (e.target.matches('.nav-link')) {
        trackEngagement('navigation_click', e.target.textContent.trim());
    }
});

// Track form interactions
document.addEventListener('input', (e) => {
    if (e.target.matches('.form-input')) {
        trackEngagement('form_input', e.target.name || 'unknown');
    }
});

// Track demo interactions
const demoVideo = document.querySelector('.demo-video');
if (demoVideo) {
    demoVideo.addEventListener('click', () => {
        trackEngagement('demo_click', 'demo_video');
    });
}

// Track ROI calculator usage
if (roiCalculator) {
    const inputs = roiCalculator.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            trackEngagement('roi_calculator_input', input.id);
        });
    });
}

// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const body = document.body;

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
body.setAttribute('data-theme', currentTheme);

// Force apply theme styles
function applyTheme(theme) {
    body.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    
    // Force repaint
    body.style.display = 'none';
    body.offsetHeight; // Trigger reflow
    body.style.display = '';
}

// Update theme icon based on current theme
function updateThemeIcon(theme) {
    if (theme === 'dark') {
        themeIcon.className = 'fas fa-sun';
    } else {
        themeIcon.className = 'fas fa-moon';
    }
}

// Initialize theme
applyTheme(currentTheme);
updateThemeIcon(currentTheme);

// Theme toggle event listener
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Update theme
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        updateThemeIcon(newTheme);
        
        // Track theme change
        trackEngagement('theme_toggle', newTheme);
        
        // Add smooth transition
        body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            body.style.transition = '';
        }, 300);
    });
}

// Export functions for external use
window.AgiliziaAI = {
    calculateROI,
    showNotification,
    typeWriter,
    animateCounter,
    getLeadStats,
    trackEngagement
};