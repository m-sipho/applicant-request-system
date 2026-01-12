import { LogOut } from "lucide-react"

function Header({ user }) {
    return (
        <header className="header-wrapper">
            <h2 className="header-title">Dashboard</h2>
            <div className="header-right">
                <div className="sub-left">
                    <div className="username">{user.email}</div>
                    <div className="role">{user.role ? (user.role.charAt(0).toUpperCase() + user.role.slice(1)) : ""}</div>
                </div>
                <div className="logout-container">
                    <LogOut className="logout" size={30} ><title>Logout</title></LogOut>
                </div>
            </div>
        </header>
    )
}

export default Header