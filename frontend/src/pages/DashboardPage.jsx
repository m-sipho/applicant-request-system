import ApplicantDashboard from "./dashboard/applicantDashboard"
import { allRequests, user } from "../services/api"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function DashboardPage() {
    const [requests, setRequests] = useState([])
    const [currentUser, setCurrentUser] = useState("")

    const navigate = useNavigate();
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await allRequests();
                const getUser = await user();

                setCurrentUser(getUser);

                // Change ISO format date to local time
                data.map(request => {
                    const utcTime = request.created_at.replace(' ', 'T') + 'Z'
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
            }
        };
        fetchData();
    }, [])

    async function handleLogOut(e) {
        e.preventDefault();

        sessionStorage.removeItem("token");
        navigate("/login")
    }

    return (
        currentUser.role === "applicant" &&
            <ApplicantDashboard user={currentUser} requests={requests} onLogout={handleLogOut} />
    )
}

export default DashboardPage