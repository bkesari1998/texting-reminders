  // Update hidden field when tab changes
  document.addEventListener('DOMContentLoaded', function() {
    const incompletTab = document.getElementById('incomplete-tab');
    const completedTab = document.getElementById('completed-tab');
    const hiddenField = document.getElementById('active-tab-redirect');

    incompletTab.addEventListener('shown.bs.tab', function() {
        hiddenField.value = 'incomplete';
    });

    completedTab.addEventListener('shown.bs.tab', function() {
        hiddenField.value = 'complete';
    });
});

async function toggleTaskCompletion(taskId) {
    try {
        const response = await fetch(`/toggle-completion/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();

            // Find the task element
            const taskElement = document.querySelector(`button[onclick="toggleTaskCompletion('${taskId}')"]`).closest('li');

            // Determine source and target lists
            let sourceList, targetList, newButtonText;
            if (data.completed) {
                // Moving from incomplete to completed
                sourceList = document.querySelector('#incomplete-tab-pane ul');
                targetList = document.querySelector('#completed-tab-pane ul');
                newButtonText = 'Reopen';
            } else {
                // Moving from completed to incomplete
                sourceList = document.querySelector('#completed-tab-pane ul');
                targetList = document.querySelector('#incomplete-tab-pane ul');
                newButtonText = 'Complete';
            }

            // Update the button text
            const toggleButton = taskElement.querySelector(`button[onclick="toggleTaskCompletion('${taskId}')"]`);
            toggleButton.textContent = newButtonText;

            // Move the element to the target list
            sourceList.removeChild(taskElement);
            targetList.appendChild(taskElement);

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
            // Find and remove the task element from the DOM
            const taskElement = document.querySelector(`button[onclick="deleteTask('${taskId}')"]`).closest('li');
            taskElement.remove();
        } else {
            console.error('Failed to delete task');
            alert('Failed to delete task. Please try again.');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('An error occurred. Please try again.');
    }
}