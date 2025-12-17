// Function to update visitor count
   async function updateVisitorCount() {
       try {
           // We'll replace this URL with our actual API Gateway URL later
           const response = await fetch('https://rexobk4bl55jefpfwoulwvcsbm0joqzf.lambda-url.us-east-2.on.aws/', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
               },
           });
           
           if (response.ok) {
               const data = await response.json();
               document.getElementById('visitor-count').textContent = data.visitor_count;
           } else {
               document.getElementById('visitor-count').textContent = 'Error loading count';
           }
       } catch (error) {
           console.error('Error:', error);
           document.getElementById('visitor-count').textContent = 'Error loading count';
       }
   }
   
   // Call the function when page loads
   document.addEventListener('DOMContentLoaded', updateVisitorCount);