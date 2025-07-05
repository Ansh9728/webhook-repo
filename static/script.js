
const list = document.getElementById('event-list');
let seen = new Set();

async function fetchEvents() {
    console.log('Fetching events at:', new Date().toISOString());
    try {
        const res = await fetch('http://localhost:5000/webhook/event'); // Use localhost for consistency
        console.log('Fetch response status:', res.status, res.statusText);
        if (!res.ok) {
            console.error('Fetch failed with status:', res.status, res.statusText);
            list.innerHTML = '<li>Error loading events. Check console for details.</li>';
            return;
        }

        const events = await res.json();
        console.log('Received events:', events);
        console.log('Number of events:', events.length);

        if (!list) {
            console.error('Event list element not found in DOM');
            return;
        }

        list.innerHTML = ''; // Clear list
        console.log('Cleared event list');

        if (!Array.isArray(events)) {
            console.error('Events is not an array:', events);
            list.innerHTML = '<li>Invalid data format from server</li>';
            return;
        }

        if (events.length === 0) {
            console.warn('No events received from the server');
            list.innerHTML = '<li>No recent events found</li>';
            return;
        }

        const now = Date.now();
        events.forEach((evt, index) => {
            console.log(`Processing event ${index}:`, evt);
            if (!evt._id || !evt.type || !evt.author || !evt.to_branch) {
                console.error(`Invalid event data at index ${index}:`, evt);
                return;
            }

            // Skip duplicates
            if (seen.has(evt._id)) {
                console.log(`Skipping duplicate event ID: ${evt._id}`);
                return;
            }

            // Skip events older than 15s
            const evtTime = new Date(evt.timestamp).getTime();
            console.log(`Event timestamp: ${evt.timestamp}, Age: ${(now - evtTime) / 1000}s`);
            if (isNaN(evtTime)) {
                console.error(`Invalid timestamp for event ID ${evt._id}: ${evt.timestamp}`);
                return;
            }
            if (now - evtTime > 15000) {
                console.log(`Skipping old event ID ${evt._id}, age: ${(now - evtTime) / 1000}s`);
                return;
            }

            seen.add(evt._id);
            console.log(`Adding event ID ${evt._id} to seen set`);

            const li = document.createElement('li');
            li.setAttribute('data-event-type', evt.type);
            let text = '';
            if (evt.type === 'push') {
                text = `${evt.author} pushed to ${evt.to_branch} on ${new Date(evt.timestamp).toUTCString()}`;
            } else if (evt.type === 'pull_request') {
                text = `${evt.author} submitted a pull request from ${evt.from_branch} to ${evt.to_branch} on ${new Date(evt.timestamp).toUTCString()}`;
            } else if (evt.type === 'merge') {
                text = `${evt.author} merged branch ${evt.from_branch} to ${evt.to_branch} on ${new Date(evt.timestamp).toUTCString()}`;
            } else {
                console.warn(`Unknown event type for event ID ${evt._id}: ${evt.type}`);
                text = `Unknown event: ${JSON.stringify(evt)}`;
            }
            li.textContent = text;
            list.appendChild(li);
            console.log(`Appended event ${index} to list: ${text}`);
        });

        if (list.children.length === 0) {
            console.warn('No events were appended to the list');
            list.innerHTML = '<li>No valid events to display</li>';
        }
    } catch (err) {
        console.error('Error fetching events:', err.message, err.stack);
        list.innerHTML = '<li>Error loading events. Check console for details.</li>';
    }
}

console.log('Starting initial fetch');
fetchEvents();
setInterval(() => {
    console.log('Interval fetch triggered');
    fetchEvents();
}, 15000);