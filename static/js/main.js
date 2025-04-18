// Mobile Menu Toggle
document.addEventListener("DOMContentLoaded", () => {
    const mobileMenuBtn = document.querySelector(".mobile-menu-btn");
    const nav = document.querySelector(".nav");
    const userActions = document.querySelector(".user-actions");
  
    if (mobileMenuBtn) {
      mobileMenuBtn.addEventListener("click", () => {
        nav.classList.toggle("active");
        userActions.classList.toggle("active");
        mobileMenuBtn.classList.toggle("active");
      });
    }
  
    // Set minimum date for date inputs to today
    const dateInputs = document.querySelectorAll('input[type="date"]');
    if (dateInputs.length > 0) {
      const today = new Date().toISOString().split("T")[0];
      dateInputs.forEach((input) => {
        input.setAttribute("min", today);
      });
    }
  
    // Initialize date inputs with default values if they exist
    const pickupDateInput = document.getElementById("pickup-date");
    const returnDateInput = document.getElementById("return-date");
  
    if (pickupDateInput && returnDateInput) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
  
      const todayFormatted = today.toISOString().split("T")[0];
      const tomorrowFormatted = tomorrow.toISOString().split("T")[0];
  
      pickupDateInput.value = todayFormatted;
      returnDateInput.value = tomorrowFormatted;
  
      // Ensure return date is always after pickup date
      pickupDateInput.addEventListener("change", function () {
        const pickupDate = new Date(this.value);
        const returnDate = new Date(returnDateInput.value);
  
        if (returnDate <= pickupDate) {
          const nextDay = new Date(pickupDate);
          nextDay.setDate(nextDay.getDate() + 1);
          returnDateInput.value = nextDay.toISOString().split("T")[0];
        }
      });
    }
  
    // Toggle password visibility
    const togglePasswordBtns = document.querySelectorAll(".toggle-password");
    if (togglePasswordBtns.length > 0) {
      togglePasswordBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
          const passwordInput = this.previousElementSibling;
          const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
          passwordInput.setAttribute("type", type);
          this.innerHTML = type === "password" ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
      });
    }
  
    // Close message alerts
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
      button.addEventListener('click', function() {
        this.parentElement.style.display = 'none';
      });
    });
  });