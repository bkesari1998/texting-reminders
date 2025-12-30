async function toggleTaskCompletion(taskId) {
    try {
        const response = await fetch(`/toggle-completion/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Reload the page to show the updated task in the correct tab
            window.location.reload();
        } else {
            console.error('Failed to toggle task completion');
            alert('Failed to update task. Please try again.');
        }
    } catch (error) {
        console.error('Error toggling task completion:', error);
        alert('An error occurred. Please try again.');
    }
}