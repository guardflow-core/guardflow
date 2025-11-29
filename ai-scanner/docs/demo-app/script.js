// Agilizia_AI Demo App - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize app
    initializeApp();
    
    // Setup event listeners
    setupEventListeners();
    
    // Start animations
    startAnimations();
    
    // Initialize ROI calculator
    initializeROICalculator();
});

function initializeApp() {
    console.log('🚀 Agilizia_AI Demo App initialized');
    
    // Add scroll reveal animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, observerOptions);
    
    // Observe all scroll-reveal elements
    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);
    });
}

function setupEventListeners() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // CTA button smooth scroll
    document.querySelector('.cta-button').addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('#demo').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
    
    // Contact form submission
    document.getElementById('contactForm').addEventListener('submit', handleContactForm);
}

function startAnimations() {
    // Animate hero features on load
    setTimeout(() => {
        document.querySelectorAll('.hero-feature').forEach((feature, index) => {
            setTimeout(() => {
                feature.style.opacity = '1';
                feature.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }, 500);
    
    // Animate scanned items
    animateScannedItems();
    
    // Start live demo simulation
    startLiveDemo();
}

function animateScannedItems() {
    const items = document.querySelectorAll('.scanned-item');
    items.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, (index + 1) * 1000);
    });
}

function startLiveDemo() {
    // Simulate scanning process
    setTimeout(() => {
        document.querySelector('.scanning-status').textContent = 'Produto identificado!';
        document.querySelector('.scanning-status').style.color = '#4ade80';
    }, 3000);
    
    // Add more items periodically
    setTimeout(() => {
        addScannedItem('🥕 Cenoura Orgânica', 'R$ 3,50');
    }, 5000);
    
    setTimeout(() => {
        addScannedItem('🍞 Pão Integral', 'R$ 4,20');
    }, 7000);
}

function addScannedItem(name, price) {
    const scannedItems = document.querySelector('.scanned-items');
    const newItem = document.createElement('div');
    newItem.className = 'scanned-item';
    newItem.style.opacity = '0';
    newItem.style.transform = 'translateX(-30px)';
    
    newItem.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <div class="scanned-item-info">
            <div class="scanned-item-name">${name}</div>
            <div class="scanned-item-price">${price}</div>
        </div>
    `;
    
    scannedItems.appendChild(newItem);
    
    // Animate in
    setTimeout(() => {
        newItem.style.opacity = '1';
        newItem.style.transform = 'translateX(0)';
        updateTotal();
    }, 100);
}

function updateTotal() {
    const items = document.querySelectorAll('.scanned-item-price');
    let total = 0;
    
    items.forEach(item => {
        const price = parseFloat(item.textContent.replace('R$ ', '').replace(',', '.'));
        total += price;
    });
    
    const totalElement = document.querySelector('.scanned-total');
    totalElement.textContent = `Total: R$ ${total.toFixed(2).replace('.', ',')}`;
    
    // Animate total update
    totalElement.style.transform = 'scale(1.05)';
    setTimeout(() => {
        totalElement.style.transform = 'scale(1)';
    }, 200);
}

function showDemo(demoType) {
    // Remove active class from all tabs and panels
    document.querySelectorAll('.demo-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.demo-panel').forEach(panel => panel.classList.remove('active'));
    
    // Add active class to selected tab and panel
    document.querySelector(`[onclick="showDemo('${demoType}')"]`).classList.add('active');
    document.getElementById(`${demoType}-demo`).classList.add('active');
    
    // Add animation to the active panel
    const activePanel = document.getElementById(`${demoType}-demo`);
    activePanel.style.opacity = '0';
    activePanel.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        activePanel.style.opacity = '1';
        activePanel.style.transform = 'translateY(0)';
    }, 100);
    
    // Special animations for specific demos
    if (demoType === 'cart') {
        animateCartItems();
    } else if (demoType === 'esg') {
        animateESGMetrics();
    } else if (demoType === 'payment') {
        animatePaymentProcess();
    }
}

function animateCartItems() {
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 200);
    });
}

function animateESGMetrics() {
    // Simulate ESG score animation
    const features = document.querySelectorAll('#esg-demo .demo-feature');
    features.forEach((feature, index) => {
        setTimeout(() => {
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, index * 300);
    });
}

function animatePaymentProcess() {
    // Simulate payment flow animation
    const features = document.querySelectorAll('#payment-demo .demo-feature');
    features.forEach((feature, index) => {
        setTimeout(() => {
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, index * 300);
    });
}

function updateQuantity(item, change) {
    const qtyElement = document.getElementById(`${item}-qty`);
    const currentQty = parseInt(qtyElement.textContent);
    const newQty = Math.max(0, currentQty + change);
    
    qtyElement.textContent = newQty;
    
    // Animate quantity change
    qtyElement.style.transform = 'scale(1.2)';
    qtyElement.style.color = '#4ade80';
    
    setTimeout(() => {
        qtyElement.style.transform = 'scale(1)';
        qtyElement.style.color = '#1e293b';
    }, 200);
    
    // Update cart total
    updateCartTotal();
}

function updateCartTotal() {
    const appleQty = parseInt(document.getElementById('apple-qty').textContent);
    const milkQty = parseInt(document.getElementById('milk-qty').textContent);
    
    const applePrice = 5.99;
    const milkPrice = 8.50;
    
    const total = (appleQty * applePrice) + (milkQty * milkPrice);
    
    const totalElement = document.getElementById('cart-total');
    totalElement.textContent = `Subtotal: R$ ${total.toFixed(2).replace('.', ',')}`;
    
    // Animate total update
    totalElement.style.transform = 'scale(1.05)';
    totalElement.style.background = 'linear-gradient(135deg, #4ade80, #22c55e)';
    
    setTimeout(() => {
        totalElement.style.transform = 'scale(1)';
        totalElement.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
    }, 300);
}

function initializeROICalculator() {
    const inputs = document.querySelectorAll('#roi input');
    inputs.forEach(input => {
        input.addEventListener('input', calculateROI);
    });
    
    // Initial calculation
    calculateROI();
}

function calculateROI() {
    const dailyTransactions = parseInt(document.getElementById('daily-transactions').value) || 0;
    const avgTime = parseInt(document.getElementById('avg-transaction-time').value) || 0;
    const hourlyWage = parseFloat(document.getElementById('hourly-wage').value) || 0;
    const abandonmentRate = parseFloat(document.getElementById('abandonment-rate').value) || 0;
    
    // Calculate savings
    const timeSavedPerTransaction = avgTime * 0.85; // 85% time reduction
    const dailyTimeSaved = dailyTransactions * timeSavedPerTransaction;
    const monthlyTimeSaved = dailyTimeSaved * 30;
    const monthlySavings = (monthlyTimeSaved / 60) * hourlyWage;
    
    // Calculate ROI
    const annualSavings = monthlySavings * 12;
    const implementationCost = 50000; // Estimated implementation cost
    const annualROI = ((annualSavings - implementationCost) / implementationCost) * 100;
    
    // Calculate payback period
    const paybackMonths = implementationCost / monthlySavings;
    
    // Update display
    document.getElementById('monthly-savings').textContent = `R$ ${monthlySavings.toLocaleString('pt-BR', {maximumFractionDigits: 0})}`;
    document.getElementById('annual-roi').textContent = `${Math.max(0, annualROI).toFixed(0)}%`;
    document.getElementById('payback').textContent = `${paybackMonths.toFixed(1)} meses`;
    
    // Animate results
    animateROIResults();
}

function animateROIResults() {
    const results = document.querySelectorAll('.roi-value');
    results.forEach((result, index) => {
        setTimeout(() => {
            result.style.transform = 'scale(1.1)';
            result.style.color = '#4ade80';
            
            setTimeout(() => {
                result.style.transform = 'scale(1)';
                result.style.color = '#1e293b';
            }, 200);
        }, index * 100);
    });
}

function handleContactForm(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    // Simulate form submission
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        submitBtn.textContent = 'Mensagem Enviada!';
        submitBtn.style.background = 'linear-gradient(135deg, #4ade80, #22c55e)';
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
            e.target.reset();
        }, 2000);
    }, 1500);
    
    // Log form data (in real app, this would be sent to server)
    console.log('📧 Contact form submitted:', data);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Performance optimization
const debouncedCalculateROI = debounce(calculateROI, 300);

// Update ROI calculator to use debounced function
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('#roi input');
    inputs.forEach(input => {
        input.addEventListener('input', debouncedCalculateROI);
    });
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Add scroll-based animations
window.addEventListener('scroll', debounce(function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero');
    const speed = scrolled * 0.5;
    
    if (parallax) {
        parallax.style.transform = `translateY(${speed}px)`;
    }
}, 10));

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// Add touch gestures for mobile
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
});

document.addEventListener('touchend', function(e) {
    if (!touchStartX || !touchStartY) return;
    
    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;
    
    const diffX = touchStartX - touchEndX;
    const diffY = touchStartY - touchEndY;
    
    if (Math.abs(diffX) > Math.abs(diffY)) {
        if (diffX > 50) {
            // Swipe left - next demo
            const activeTab = document.querySelector('.demo-tab.active');
            const nextTab = activeTab.nextElementSibling;
            if (nextTab && nextTab.classList.contains('demo-tab')) {
                nextTab.click();
            }
        } else if (diffX < -50) {
            // Swipe right - previous demo
            const activeTab = document.querySelector('.demo-tab.active');
            const prevTab = activeTab.previousElementSibling;
            if (prevTab && prevTab.classList.contains('demo-tab')) {
                prevTab.click();
            }
        }
    }
    
    touchStartX = 0;
    touchStartY = 0;
});

console.log('🎉 Agilizia_AI Demo App loaded successfully!');