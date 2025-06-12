// Custom JavaScript for Math Problems application

document.addEventListener('DOMContentLoaded', function() {
    // Handle choice selection for MCQ/SCQ problems
    const choiceItems = document.querySelectorAll('.choice-item');
    
    choiceItems.forEach(item => {
        item.addEventListener('click', function() {
            const problemType = this.closest('form').dataset.problemType;
            const choiceInput = this.querySelector('input');
            
            if (problemType === 'scq') {
                // For SCQ, deselect all other choices
                choiceItems.forEach(otherItem => {
                    otherItem.classList.remove('selected');
                    otherItem.querySelector('input').checked = false;
                });
                
                // Select this choice
                this.classList.add('selected');
                choiceInput.checked = true;
            } else if (problemType === 'mcq') {
                // For MCQ, toggle this choice
                this.classList.toggle('selected');
                choiceInput.checked = !choiceInput.checked;
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle filter form submission
    const filterForm = document.getElementById('problem-filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Remove empty filter values before submitting
            const inputs = this.querySelectorAll('input, select');
            inputs.forEach(input => {
                if (input.value === '') {
                    input.disabled = true;
                }
            });
        });
    }
    
    // Auto-resize textarea for open-ended questions
    const answerTextarea = document.getElementById('answer-text');
    if (answerTextarea) {
        answerTextarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Initial resize
        answerTextarea.style.height = 'auto';
        answerTextarea.style.height = (answerTextarea.scrollHeight) + 'px';
    }
});