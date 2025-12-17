// Function to update visitor count
async function fetchViewCount() {
    try {
        const response = await fetch('https://bnrxyessa33pnmmqqzavgnbi4i0ngtfy.lambda-url.us-east-1.on.aws/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('visitor-count').textContent = data.views;  
        } else {
            document.getElementById('visitor-count').textContent = 'Error loading count';
        }
    } catch (error) {
        console.error('Error fetching view count:', error);
        document.getElementById('visitor-count').textContent = 'Error loading count';
    }
}


document.addEventListener('DOMContentLoaded', fetchViewCount);