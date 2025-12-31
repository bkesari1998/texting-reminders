async function toggleTaskCompletion(taskId) {
    try {
        const response = await fetch(`/toggle-completion/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {

            const url = new URL(window.location.href);
            const incomplete_tab = document.getElementById("incomplete-tab")

            if (incomplete_tab.classList.contains("active")) {
                url.searchParams.set('active_tab', 'incomplete');
            } else {
                url.searchParams.set('active_tab', 'complete');
            }

            window.location.href = url.toString();
        } else {
            console.error('Failed to toggle task completion');
            alert('Failed to update task. Please try again.');
        }
    } catch (error) {
        console.error('Error toggling task completion:', error);
        alert('An error occurred. Please try again.');
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`/delete-task/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {

            const url = new URL(window.location.href);
            const incomplete_tab = document.getElementById("incomplete-tab")

            if (incomplete_tab.classList.contains("active")) {
                url.searchParams.set('active_tab', 'incomplete');
            } else {
                url.searchParams.set('active_tab', 'complete');
            }

            window.location.href = url.toString();
        } else {
            console.error('Failed to toggle task completion');
            alert('Failed to update task. Please try again.');
        }
    } catch (error) {
        console.error('Error toggling task completion:', error);
        alert('An error occurred. Please try again.');
    }
}