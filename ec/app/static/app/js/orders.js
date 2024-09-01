document.addEventListener('DOMContentLoaded', () => {
    const cancelButtons = document.querySelectorAll('.cancel-btn');
    cancelButtons.forEach((button) => {
      const orderId = button.dataset.orderId;
      const cancelUrl = button.dataset.cancelUrl;
  
      // Fetch the cancellation status of each order from the server
      fetch(cancelUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.is_cancelled) {
            // If the order is already cancelled, update the UI with the cancellation message
            const col = button.closest('.col-sm-2');
            col.innerHTML = '<p class="text-muted">Order Cancelled!</p>';
          } else {
            // If the order is not cancelled, add the click event listener to the cancel button
            button.addEventListener('click', (e) => {
              e.preventDefault();
              cancelOrder(cancelUrl, orderId);
            });
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
  });
  
  const cancelOrder = (cancelUrl, orderId) => {
    fetch(cancelUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}',
      },
      body: JSON.stringify({ order_id: orderId }),
    })
      .then((response) => response.json())
      .then((data) => {
        // On successful cancellation, update the UI
        const col = document.querySelector(`.col-sm-2[data-order-id="${orderId}"]`);
        col.innerHTML = '<p class="text-muted">Order Cancelled!</p>';
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };
  