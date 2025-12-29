async function toggleComplete(taskId) {
    const response = await fetch(`/toggle-completion/${taskId}`, {
        method: "PATCH",
    });

    if (!response.ok) {
        alert("Failed to update task");
    } else {
        window.location.href = "/";
    }
}