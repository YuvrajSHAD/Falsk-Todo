let tasks = [];
let editingTaskId = null;

// Safe fetch helper
async function safeFetch(url, options = {}) {
  const res = await fetch(url, options);
  if (res.status === 401) {
    window.location.href = '/login';
    return null;
  }
  return res;
}

function createTaskElement(task) {
  const taskEl = document.createElement('div');
  taskEl.classList.add('task');
  if (task.done) taskEl.classList.add('done');
  taskEl.style.left = task.pos_x + 'px';
  taskEl.style.top = task.pos_y + 'px';
  taskEl.dataset.id = task.id;
  taskEl.dataset.page = task.page;
  taskEl.textContent = task.content;

  // --- Restore draggable behavior
  taskEl.draggable = true;
  taskEl.addEventListener('dragstart', dragStart);

  // Three dots menu
  const dots = document.createElement('div');
  dots.className = 'three-dots';
  dots.innerHTML = '&#8942;';
  taskEl.appendChild(dots);

  const menu = document.createElement('div');
  menu.className = 'menu';
  menu.innerHTML = `
    <button class="edit-btn">Edit</button>
    <button class="delete-btn">Delete</button>
    <button class="done-btn">${task.done ? 'Mark Undone' : 'Mark Done'}</button>
  `;
  taskEl.appendChild(menu);

  dots.onclick = (e) => {
    e.stopPropagation();
    closeAllMenus();
    menu.style.display = 'block';
  };

  menu.querySelector('.edit-btn').onclick = (e) => {
    e.stopPropagation();
    closeAllMenus();
    openEditPrompt(task);
  };

  menu.querySelector('.delete-btn').onclick = (e) => {
    e.stopPropagation();
    closeAllMenus();
    deleteTask(task.id);
  };

  menu.querySelector('.done-btn').onclick = (e) => {
    e.stopPropagation();
    closeAllMenus();
    toggleDone(task);
  };

  return taskEl;
}

function closeAllMenus() {
  document.querySelectorAll('.menu').forEach(m => m.style.display = 'none');
}

function openEditPrompt(task) {
  const newContent = prompt('Edit task content:', task.content);
  if (newContent !== null && newContent.trim() !== '') {
    updateTask(task.id, { content: newContent.trim() });
  }
}

async function deleteTask(id) {
  const res = await safeFetch(`/tasks/${id}`, { method: 'DELETE' });
  if (!res) return;
  tasks = tasks.filter(t => t.id !== id);
  renderTasks();
}

async function toggleDone(task) {
  await updateTask(task.id, { done: !task.done });
}

async function updateTask(id, fields) {
  const res = await safeFetch(`/tasks/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(fields)
  });
  if (!res) return;
  const task = tasks.find(t => t.id === id);
  if (task) Object.assign(task, fields);
  renderTasks();
}

function renderTasks() {
  // Only render in the Tasks page area
  const page2 = document.querySelector('.tasks-page .tasks-lines');
  if (page2) {
    page2.innerHTML = "";
    tasks.forEach(t => {
      if (t.page === 2) {
        const el = createTaskElement(t);
        page2.appendChild(el);
      }
    });
  }
}

// --- Drag and drop handlers for tasks
let draggedTask = null;
let dragOffsetX = 0;
let dragOffsetY = 0;

function dragStart(e) {
  draggedTask = e.target;
  dragOffsetX = e.offsetX;
  dragOffsetY = e.offsetY;
}

document.addEventListener('DOMContentLoaded', function () {
  // Enable drag/drop only in the Tasks page lines container
  const linesEl = document.querySelector('.tasks-page .tasks-lines');
  if (linesEl) {
    linesEl.addEventListener('dragover', e => e.preventDefault());
    linesEl.addEventListener('drop', async e => {
      e.preventDefault();
      if (draggedTask) {
        let newX = e.clientX - linesEl.getBoundingClientRect().left - dragOffsetX;
        let newY = e.clientY - linesEl.getBoundingClientRect().top - dragOffsetY;
        newX = Math.max(0, Math.min(newX, linesEl.clientWidth - draggedTask.clientWidth));
        newY = Math.max(0, Math.min(newY, linesEl.clientHeight - draggedTask.clientHeight));
        const taskId = parseInt(draggedTask.dataset.id);
        await updateTask(taskId, { pos_x: newX, pos_y: newY, page: 2 });
        draggedTask.style.left = newX + 'px';
        draggedTask.style.top = newY + 'px';
        draggedTask = null;
      }
    });
  }

  document.body.onclick = closeAllMenus;

  // Add task button/input handlers
  document.getElementById('add-task-btn').onclick = async () => {
    const input = document.getElementById('new-task-input');
    let content = input.value.trim();
    if (!content) {
      alert('Enter task content first');
      return;
    }
    const res = await safeFetch('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, pos_x: 40, pos_y: 50, page: 2 })
    });
    if (!res) return;
    const data = await res.json();
    if (data.id) {
      tasks.push({ id: data.id, content, done: false, pos_x: 40, pos_y: 50, page: 2 });
      renderTasks();
      input.value = '';
    } else {
      alert('Error adding task');
    }
  };

  // Initial load
  fetchTasks();
});

async function fetchTasks() {
  const res = await safeFetch('/tasks');
  if (!res) return;
  tasks = await res.json();
  renderTasks();
}
