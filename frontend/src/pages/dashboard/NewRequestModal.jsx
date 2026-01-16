import { X } from "lucide-react"
import { useState } from "react"

function NewRequestModal({ onClose }) {
    const [requestType, setRequestType] = useState(null);

    return (
        <div className="modal-layout">
            <div className="modal-container">
                <div className="modal-header">
                    <span>Create a request</span>
                    <X className="close" onClick={onClose} />
                </div>
                <form className="create-request-form">
                    <div>
                        <label>Request Type</label>
                        <select className="create-select" value={requestType} onChange={e => setRequestType(e.target.value)}>
                            <option disabled selected value="choose">Choose an option</option>
                            <option value="REMARKING SCRIPT">REMARKING SCRIPT</option>
                            <option value="refund">REFUND REQUEST</option>
                            <option value="AEGROTAT/SPECIAL EXAM">AEGROTAT/SPECIAL EXAM</option>
                        </select>
                    </div>

                    {requestType &&
                        <div>
                            <label>Student Number</label>
                            <input type="text" />
                        </div>
                    }

                    {(requestType === "REMARKING SCRIPT" || requestType === "AEGROTAT/SPECIAL EXAM") &&
                        <div>
                            <label>Module Code</label>
                            <input type="text" />
                        </div>
                    }

                    {requestType &&
                        <>
                            <div>
                                <label>Description</label>
                                <textarea name="" id="" cols="50" rows="10"></textarea>
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