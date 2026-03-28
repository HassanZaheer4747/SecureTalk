// SecureTalk - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Flash message auto-dismiss
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Password strength meter
    const passwordInput = document.getElementById('password');
    const strengthMeter = document.getElementById('password-strength-meter');
    
    if (passwordInput && strengthMeter) {
        passwordInput.addEventListener('input', function() {
            const password = passwordInput.value;
            const strength = calculatePasswordStrength(password);
            
            // Update the strength meter
            strengthMeter.value = strength;
            
            // Update the strength text
            const strengthText = document.getElementById('password-strength-text');
            if (strengthText) {
                if (strength < 2) {
                    strengthText.textContent = 'Weak';
                    strengthText.className = 'text-danger';
                } else if (strength < 3) {
                    strengthText.textContent = 'Medium';
                    strengthText.className = 'text-warning';
                } else if (strength < 4) {
                    strengthText.textContent = 'Strong';
                    strengthText.className = 'text-success';
                } else {
                    strengthText.textContent = 'Very Strong';
                    strengthText.className = 'text-success';
                }
            }
        });
    }
    
    // Calculate password strength (0-4)
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        // Length check
        if (password.length >= 8) {
            strength += 1;
        }
        
        // Uppercase check
        if (/[A-Z]/.test(password)) {
            strength += 1;
        }
        
        // Lowercase check
        if (/[a-z]/.test(password)) {
            strength += 1;
        }
        
        // Number check
        if (/[0-9]/.test(password)) {
            strength += 1;
        }
        
        // Special character check
        if (/[^A-Za-z0-9]/.test(password)) {
            strength += 1;
        }
        
        return Math.min(strength, 4);
    }
    
    // Session timeout warning
    let sessionTimeoutWarning = 25 * 60 * 1000; // 25 minutes
    let sessionTimeout = 30 * 60 * 1000; // 30 minutes
    let warningTimer;
    let timeoutTimer;
    
    function startSessionTimers() {
        warningTimer = setTimeout(function() {
            // Show warning modal
            const warningModal = new bootstrap.Modal(document.getElementById('session-timeout-warning'));
            if (warningModal) {
                warningModal.show();
            }
        }, sessionTimeoutWarning);
        
        timeoutTimer = setTimeout(function() {
            // Redirect to logout
            window.location.href = '/auth/logout';
        }, sessionTimeout);
    }
    
    function resetSessionTimers() {
        clearTimeout(warningTimer);
        clearTimeout(timeoutTimer);
        startSessionTimers();
    }
    
    // Start session timers if user is logged in
    if (document.querySelector('.logout-link')) {
        startSessionTimers();
        
        // Reset timers on user activity
        document.addEventListener('click', resetSessionTimers);
        document.addEventListener('keypress', resetSessionTimers);
        document.addEventListener('scroll', resetSessionTimers);
        document.addEventListener('mousemove', resetSessionTimers);
    }
    
    // Keep session alive button
    const keepAliveBtn = document.getElementById('keep-session-alive');
    if (keepAliveBtn) {
        keepAliveBtn.addEventListener('click', function() {
            // Reset session timers
            resetSessionTimers();
            
            // Hide the warning modal
            const warningModal = bootstrap.Modal.getInstance(document.getElementById('session-timeout-warning'));
            if (warningModal) {
                warningModal.hide();
            }
        });
    }
});