import { X } from "lucide-react"
import { useState } from "react"

function NewRequestModal({ onClose, requestCreation }) {
    const [requestType, setRequestType] = useState("");
    const [studentNumber, setStudentNumber] = useState("");
    const [moduleCode, setModuleCode] = useState("");
    const [description, setDescription] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();

        onClose()

        await requestCreation({
            requestType: requestType,
            description: description,
            studentNumber: studentNumber,
            moduleCode: moduleCode
        })
    }

    return (
        <div className="modal-layout">
            <div className="modal-container">
                <div className="modal-header">
                    <span>Create a request</span>
                    <X className="close" onClick={onClose} />
                </div>
                <form className="create-request-form" onSubmit={handleSubmit}>
                    <div>
                        <label>Request Type</label>
                        <select className="create-select" value={requestType} onChange={e => setRequestType(e.target.value)}>
                            <option disabled value="">Choose an option</option>
                            <option value="REMARKING SCRIPT">REMARKING SCRIPT</option>
                            <option value="REFUND REQUEST">REFUND REQUEST</option>
                            <option value="AEGROTAT/SPECIAL EXAM">AEGROTAT/SPECIAL EXAM</option>
                        </select>
                    </div>

                    {requestType &&
                        <div>
                            <label>Student Number</label>
                            <input type="text" placeholder="e.g 12345678" required value={studentNumber} onChange={e => setStudentNumber(e.target.value)} />
                        </div>
                    }

                    {(requestType === "REMARKING SCRIPT" || requestType === "AEGROTAT/SPECIAL EXAM") &&
                        <div>
                            <label>Module Code</label>
                            <input type="text" placeholder="MAT2613" required value={moduleCode} onChange={e => setModuleCode(e.target.value)} />
                        </div>
                    }

                    {requestType &&
                        <>
                            <div>
                                <label>Description</label>
                                <textarea placeholder="Leave your message here..." required cols="50" rows="10" value={description} onChange={e => setDescription(e.target.value)}></textarea>
                            </div>
                            <div className="btns">
                                <button type="button" className="cancel-btn" onClick={onClose}>Cancel</button>
                                <button type="submit" className="create-btn">Create</button>
                            </div>
                        </>
                    }
                </form>
            </div>
        </div>
    )
}

export default NewRequestModal