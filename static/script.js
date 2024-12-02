document.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("todo-list");
    let draggedItem = null;

    list.addEventListener("dragstart", (e) => {
        if (e.target.tagName === "LI") {
            draggedItem = e.target;
            e.target.style.opacity = 0.5;
        }
    });

    list.addEventListener("dragend", (e) => {
        if (e.target.tagName === "LI") {
            e.target.style.opacity = "";
        }
        saveOrder(); // Save the order after the drag ends
    });

    list.addEventListener("dragover", (e) => {
        e.preventDefault(); // Allow drop
        const afterElement = getDragAfterElement(list, e.clientY);
        if (afterElement == null) {
            list.appendChild(draggedItem);
        } else {
            list.insertBefore(draggedItem, afterElement);
        }
    });

    function getDragAfterElement(container, y) {
        const draggableElements = [
            ...container.querySelectorAll(".task:not([draggable='false'])"),
        ];

        return draggableElements.reduce(
            (closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;
                if (offset < 0 && offset > closest.offset) {
                    return { offset: offset, element: child };
                } else {
                    return closest;
                }
            },
            { offset: Number.NEGATIVE_INFINITY }
        ).element;
    }

    function saveOrder() {
        const taskOrder = [...list.children].map((li) => li.dataset.id);

        fetch("/save-order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ order: taskOrder }),
        })
        .then((response) => {
            if (response.ok) {
                console.log("Order saved successfully!");
            } else {
                console.error("Failed to save order");
            }
        })
        .catch((error) => {
            console.error("Error saving order:", error);
        });
    }
});