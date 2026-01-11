import { LogOut } from "lucide-react"

function Header({ role, username }) {
    return (
        <header className="header-wrapper">
            <h2 className="header-title">Dashboard</h2>
            <div className="header-right">
                <div className="sub-left">
                    <div className="username">{username}</div>
                    <div className="role">{role}</div>
                </div>
                <div className="logout-container">
                    <LogOut className="logout" size={30} ><title>Logout</title></LogOut>
                </div>
            </div>
        </header>
    )
}

export default Header