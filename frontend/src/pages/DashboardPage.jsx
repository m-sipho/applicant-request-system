import ApplicantDashboard from "./dashboard/ApplicantDashboard"
import { allRequests, user, createRequest } from "../services/api"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

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
                    // Check if the time has timezone
                    let utcTime = request.created_at.replace(' ', 'T');
                    const hasTimezone = utcTime.includes('+') || utcTime.endsWith('Z');
                    if (!hasTimezone) {
                        utcTime += 'Z';
                    }

                    const dateObject = new Date(utcTime);
                    const month = dateObject.toLocaleString("default", {month: "short"});
                    const day = dateObject.getDate();
                    const year = dateObject.getFullYear();

                    const hours = String(dateObject.getHours()).padStart(2, '0');
                    const minutes = String(dateObject.getMinutes()).padStart(2, '0');

                    request.created_at = `${month} ${day}, ${year} ${hours}:${minutes}`;

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
            const hasTimezone = utcTime.includes('+') || utcTime.endsWith('Z');
                if (!hasTimezone) {
                    utcTime += 'Z';
                }
            
            const dateObject = new Date(utcTime);
            const month = dateObject.toLocaleString("default", {month: "short"});
            const day = dateObject.getDate();
            const year = dateObject.getFullYear();

            const hours = String(dateObject.getHours()).padStart(2, '0');
            const minutes = String(dateObject.getMinutes()).padStart(2, '0');

            data.created_at = `${month} ${day}, ${year} ${hours}:${minutes}`;

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