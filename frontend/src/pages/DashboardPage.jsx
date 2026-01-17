import ApplicantDashboard from "./dashboard/ApplicantDashboard"
import { allRequests, user, createRequest } from "../services/api"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function convertTimeToLocal(utc) {
    // Check if the time has timezone
    const hasTimezone = utc.includes('+') || utc.endsWith('Z');
    if (!hasTimezone) {
        utc += 'Z';
    }

    const dateObject = new Date(utc);
    const month = dateObject.toLocaleString("default", {month: "short"});
    const day = dateObject.getDate();
    const year = dateObject.getFullYear();

    const hours = String(dateObject.getHours()).padStart(2, '0');
    const minutes = String(dateObject.getMinutes()).padStart(2, '0');

    return `${month} ${day}, ${year} ${hours}:${minutes}`;
}

function DashboardPage() {
    const [requests, setRequests] = useState([])
    const [currentUser, setCurrentUser] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const navigate = useNavigate();
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true)
                const data = await allRequests();
                const getUser = await user();

                setCurrentUser(getUser);

                // Change ISO format date to local time
                data.map(request => {
                    let utcTime = request.created_at.replace(' ', 'T');
                    request.created_at = convertTimeToLocal(utcTime);

                })

                setRequests(data);
            } catch (err) {
                console.error("Failed to fetch requests", err)
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [])

    async function handleCreateRequest(formData) {
        setLoading(true);
        setError("");

        try {
            console.log("Sending request...")
            const data = await createRequest(formData.requestType, formData.description, formData.studentNumber, formData.moduleCode);
            console.log("Here is the data:", data)

            // Convert time to local
            let utcTime = data.created_at.replace(' ', 'T');
            data.created_at = convertTimeToLocal(utcTime);

            let copyOfRequests = [...requests];
            copyOfRequests.push(data)
            setRequests(copyOfRequests)
        } catch(err) {
            console.error("API error:", err);
            setError(err.message || "Failed to create request")
        } finally {
            setLoading(false)
        }
    }

    async function handleLogOut(e) {
        e.preventDefault();

        sessionStorage.removeItem("token");
        navigate("/login")
    }

    return (
        currentUser.role === "applicant" &&
            <ApplicantDashboard user={currentUser} requests={requests} onLogout={handleLogOut} onCreateRequest={handleCreateRequest} />
    )
}

export default DashboardPage