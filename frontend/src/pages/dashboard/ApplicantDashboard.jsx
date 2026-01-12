import Header from "../../components/Header";
import { Plus, Inbox, FileText, MoveRight, Clock8, Eye, CircleCheckBig, CircleX } from "lucide-react";

function ApplicationDashboard({role, username, requests}) {
    const statusContent = (status) => {
        if (status === "SUBMITTED") {
            return (
                <div className={status}>
                    <Clock8 size={14} />
                    <span>{status}</span>
                </div>
            )
        }

        if (status === "UNDER-REVIEW") {
            return (
                <div className={status}>
                    <Eye size={14} />
                    <span>{status}</span>
                </div>
            )
        }

        if (status === "APPROVED") {
            return (
                <div className={status}>
                    <CircleCheckBig size={14} />
                    <span>{status}</span>
                </div>
            )
        }

        if (status === "REJECTED") {
            return (
                <div className={status}>
                    <CircleX size={14} />
                    <span>{status}</span>
                </div>
            )
        }
    }

    return (
        <>
            <Header role={role} username={username} />
            <div className="layout-container">
                <div className="layout-header">
                    <h2>My Requests</h2>
                    <button className="btn-request"><Plus className="add-plus" /><span className="new-request-btn">New Request</span></button>
                </div>
                {requests && requests.length > 0 ? (
                    <div className="table-container">
                        <table className="request-table">
                            <thead>
                                <tr id="table-head">
                                    <th>SUBJECT</th>
                                    <th>DATE SUBMITTED</th>
                                    <th>ASSIGNEE</th>
                                    <th>STATUS</th>
                                    <th>ACTION</th>
                                </tr>
                            </thead>
                            <tbody>
                                {requests.map(request => (
                                    <tr key={request.id} id="table-content">
                                        <td className="subject-container">
                                            <div className="file-icon"><FileText size={15} /></div>
                                            <div className="subject-content">
                                                <span className="subject">{request.type}</span>
                                                <span className="muted">ID: #{request.id}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div className="time-container">
                                                <div>{request.created_at}</div>
                                                {request.updated_at === null ? <></> : <div className="muted">Updated: {request.updated_at}</div>}
                                            </div>
                                        </td>
                                        <td>{request.assignee_id}</td>
                                        {/* <td>{request.status}</td> */}
                                        <td>
                                            {statusContent(request.status)}
                                        </td>
                                        <td>
                                            <div className="move-right muted">
                                                <MoveRight size={15} />
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className="not-found">
                        <Inbox size={70} />
                        No requests found
                    </div>
                )}
            </div>
        </>
    )
}

export default ApplicationDashboard