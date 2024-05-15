console.log("Sanity check!");

// new
// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
    // console.log(data);
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    // console.log(stripe)
    // new
    // Event handler
    document.querySelector("#OrdersubmitBtn").addEventListener("click", () => {
        // Get Checkout Session ID
        fetch("/check-out/")
        .then((result) => { return result.json(); })
        .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
        console.log(res);
        });
    });
});