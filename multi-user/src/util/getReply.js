async function getReply(user, message) {
    try {
        const response = await fetch('http://localhost:8080/get_reply', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user, message })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Reply fetched successfully:', result);
        return result.reply;
    } catch (error) {
        console.error('Error fetching reply:', error);
        return null;
    }
}

export default getReply;