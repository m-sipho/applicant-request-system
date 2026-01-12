const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

// Send request to the backend with JWT Authentication
export async function fetchWithAuth(endpoint, getToken, options = {}) {
    const token = await getToken();

    if (!token) {
        console.error("No token found")
    }

    console.log(`[API] fetching ${endpoint} with token: ${token?.substring(0, 10)}...`);

    const response = await fetch(
        `${API_URL}${endpoint}`,
        {
            ...options,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
                ...options.headers
            }
        }
    )

    if (!response.ok) {
        const error = await response.json().catch(() => {});
        throw new Error(error.detail || "Request failed")
    }

    // Check if there's no content
    if (response.status === 204) {
        return null
    }

    return response.json()
}

export async function loginUser(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    return fetchWithAuth("/login", () => null, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    });
}

export async function registerUser(fullName, email, password) {
    return fetchWithAuth("/register", () => null, {
        method: "POST",
        body: JSON.stringify({
            name: fullName,
            email,
            password
        })
    });
}

export async function allRequests() {
    return fetchWithAuth("/request/all", () => (sessionStorage.getItem("token")), {
        method: "GET",
    })
}