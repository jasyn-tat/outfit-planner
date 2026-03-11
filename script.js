async function askAI() {
    // Grab all the values from your HTML inputs
    const vibe = document.getElementById('vibeInput').value;
    const age = document.getElementById('ageInput').value;
    const brand = document.getElementById('brandInput').value;
    const gender = document.getElementById('genderInput').value;

    // Check if they filled everything out
    if (!vibe || !age || !brand || !gender) return alert("Please fill out all fields!");

    const inputPage = document.getElementById('input-page');
    const loadingScreen = document.getElementById('loading-screen');
    const resultPage = document.getElementById('result-page');
    const resultDiv = document.getElementById('result');

    inputPage.style.display = "none";
    loadingScreen.style.display = "block";

    try {
        const response = await fetch('http://127.0.0.1:5001/get-outfit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // Send ALL the data to Python
            body: JSON.stringify({
                vibe: vibe,
                age: age,
                brand: brand,
                gender: gender
            })
        });

        const data = await response.json();

        loadingScreen.style.display = "none";
        resultPage.style.display = "block";

        // Use innerHTML instead of textContent so the links the AI sends actually work!
        resultDiv.innerHTML = data.outfit.replace(/\n/g, '<br>');

    } catch (error) {
        alert("Error: Python code is not working...!");
        goBack();
    }
}

function goBack() {
    document.getElementById('input-page').style.display = "block";
    document.getElementById('result-page').style.display = "none";
    document.getElementById('loading-screen').style.display = "none";
    document.getElementById('vibeInput').value = ""; // Clear input
}