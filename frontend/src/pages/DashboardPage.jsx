import ApplicationDashboard from "./dashboard/applicantDashboard"
import { allRequests, fetchWithAuth } from "../services/api"
import { useState, useEffect } from "react";
import { use } from "react";

function DashboardPage() {
    const [requests, setRequests] = useState([])
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await allRequests();

                // Change ISO format date to local time
                data.map(request => {
                    const dateObject = new Date(request.created_at);
                    const month = dateObject.toLocaleString("default", {month: "short"});
                    const day = dateObject.getDate();
                    const year = dateObject.getFullYear();

                    const hours = String(dateObject.getHours()).padStart(2, '0');
                    const minutes = String(dateObject.getMinutes()).padStart(2, '0');

                    request.created_at = `${month} ${day}, ${year} ${hours}:${minutes}`;

                })

                console.log("[API] returns", data);
                console.log(data.length)

                setRequests(data);
            } catch (err) {
                console.error("Failed to fetch requests", err)
            }
        };
        fetchData();
    }, [])
    return (
        <ApplicationDashboard role="Applicant" username="mthokozisisipho17@gmail.com" requests={requests}/>
    )
}

export default DashboardPage